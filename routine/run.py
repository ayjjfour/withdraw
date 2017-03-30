# -*- encoding=utf-8 -*-

import requests
from db.sqliteif import *
from classdef import *
from PyQt4.Qt import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import traceback
import Queue
import time
import log
import os

class Run(QThread):
    error_msg = {
            -9999:  u"未执行",
            -1002:  u"校验码错误",
            -1001:  u"密码错误", 
            0:      u"完成", 
            1001:   u"已经提取完毕",
            -2001:  u"二级密码错误",
            -3001:  u"提取金额不正确", 
            3001:   u"已经提取完毕"}

    def __init__(self, ui, queue):
        QThread.__init__(self)
        self.ui = ui
        self.queue = queue
        self.log = log.Log()
        self.path = os.getcwd()
        
    def _write_log(self, log, level = 0):
        strlog = self.log.write(log, level)
        self.emit(SIGNAL("SIG_add_log(QString)"), QString(strlog))

    def release(self):
        self.dbif.close()

    def _update_user_fetch_flag(self, user, flag):
        update_sql = "update user_info set fetch_flag = '%d' where nickname = '%s'"
        self.dbif.update_data(update_sql % (flag, user.get_nickname()))

    def _routine_run(self, s, info):
        user = UserInfo()
        user.set_info(info[0], info[1], info[2], info[3])
        
        strerr = ""
        errcode = 0
        cycle = 0
        while cycle < 1:
            cycle = 1
            #Step1 login
            self._write_log(u"用户[%s]开始登录" % info[0])
            errcode, money = user.step1_login(s, 'http://www.sjhy2016.com')
            if 0 != errcode:
                strerr = u"用户[%s]登录后，终止提现[现金：%d, 原因：%s]" %(user.get_nickname(), money, self.error_msg[errcode])
                break

            #Step2 Get Current Money
            self._write_log(u"用户[%s]开始查询现金" % info[0])
            maps, money, errcode = user.step2_get_money(s, 'http://www.sjhy2016.com/client/3login.aspx?url=usergetmoney.aspx')
            self._write_log(u"用户[%s]的现金是：￥%d" % (info[0], money))
            if 0 != errcode:
                strerr = u"用户[%s]查询结果后，终止提现[原因：%s]" %(user.get_nickname(), money, self.error_msg[errcode])
                break

            #Step3 Fetch Money
            self._write_log(u"用户[%s]开始提取现金" % info[0])
            errcode, money = user.step3_fetch_money(s, maps, money, 'http://www.sjhy2016.com/client/usergetmoney.aspx')
            if 0 != errcode:
                strerr = u"用户[%s]提取现金[%s]失败[原因：%s]" %(user.get_nickname(), money, self.error_msg[errcode])
                break
            self._write_log(u"用户[%s]提取现金[%s]成功" %(user.get_nickname(), money))

        self._update_user_fetch_flag(user, errcode)
        if strerr != "":
            self._write_log(strerr)

        info[3] = errcode
        print "emit SIG_update_state"
        self.emit(SIGNAL("SIG_update_state(QString, int)"), QString(info[0]), errcode)
        
        return errcode

    def _create_table(self):
        create_table_sql = """CREATE TABLE IF NOT EXISTS `user_info` (`nickname` VARCHAR(64) NOT NULL,`password` VARCHAR(45) NOT NULL,`secondpwd` VARCHAR(45) NOT NULL,
                            `fetch_date` DATE NULL,`fetch_flag` INT NOT NULL DEFAULT 0,PRIMARY KEY (`nickname`) )"""
        self.dbif.execute_sql(create_table_sql)

    def _delete_user_info(self, info):
        if info == None:
            strsql = "delete from user_info;"
        else:
            strsql = "delete from user_info where nickname = '%s';" % info[0]
            
        print "_delete_user_info strsql = ", strsql
        self.dbif.execute_sql(strsql)
        self.dbif.commit_routine()
            
    def _insert_user_info(self, list_info):
        insert_sql = []
        for i in range(len(list_info)):
            info = list_info[i]
            strsql = "insert into user_info (nickname, password, secondpwd, fetch_flag) values('%s', '%s', '%s', '%d')" %(info[0], info[1], info[2], info[3])
            insert_sql.append(strsql)
        
        for i in range(len(insert_sql)):
            self.dbif.insert_data(insert_sql[i])
        
        self.dbif.commit_routine()

    def save_user_info(self, list_info):
        self.dbif.begin_routine()
        
        self._delete_user_info(None)
        self._insert_user_info(list_info)

    def update_user_flag(self, flag):
        update_sql = "update user_info set fetch_flag = %d" % flag
        self.dbif.begin_routine()
        
        self.dbif.execute_sql(update_sql)
        
        self.dbif.commit_routine()

    def load_user_info(self):
        strsql = "select nickname, password, secondpwd, fetch_flag from user_info"
        info = self.dbif.select_data(strsql)
        return info

    def fetch_money_start(self):
        self.routine_stop = False
        strsql = "select nickname, password, secondpwd, fetch_flag from user_info where fetch_flag < 0"
        info = self.dbif.select_data(strsql)
        print "info = ", info
    
        for i in range(len(info)):
            (SIGNAL("SIG_update_state(QString, int)"), QString(info[i][0]), -9999)
    
        tryagain = 1
        while tryagain != 0:
            tryagain = 0

            for i in range(len(info)):
                    
                if info[i][3] >= 0:
                    continue
                    
                if self.thread_stop == True or self.routine_stop == True:
                    self._write_log(u"批量作业被中断!")
                    return
                self.dbif.begin_routine()
                s = requests.session()
                    
                errcode = 0
                try:
                    errcode = self._routine_run(s, info[i])
                except BaseException:
                    msg = traceback.format_exc()
                    self._write_log(msg)
                    self._write_log(u"提现过程发生异常，请查看日志")
                    info[i][3] = -9999
                    errcode = -9999
                        
                s.close()
                self.dbif.commit_routine()
                    
                if errcode < 0:
                    tryagain = 1    
        
        self.routine_stop = True
        self._write_log(u"完成一次批量操作!")
        
    def run(self):
        self.dbif = Sqlite3If()
        self.dbif.connect(self.path + '/db/withdraw.db')
        self.thread_stop = False
        #创建表
        self._create_table()
        
        while not self.thread_stop:
            try:  
                task = self.queue.get(block=True, timeout=20) #接收消息  
            except Queue.Empty:  
                print("Nothing to do!")
                continue
            
            if task[0] == "reset":
                self.update_user_flag(-9999)
            elif task[0] == "start":
                self.fetch_money_start()
                self.emit(SIGNAL('SIG_set_button_enable(bool)'), True)
            elif task[0] == "load":
                print "_Load_data"
                self.list_info = self.load_user_info()
                self.emit(SIGNAL("SIG_load_data()"))
            elif task[0] == "save":
                print "save = ", task[1]
                self.save_user_info(task[1])
            elif task[0] == "stop":
                self.thread_stop = True
            
            
                
