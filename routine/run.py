# -*- encoding=utf-8 -*-

import requests
from db.sqliteif import *
from classdef import *
from PyQt4.Qt import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import Queue
import time

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

    def release(self):
        self.dbif.close()

    def _routine_run(self, info):
        s = requests.session()
        user = UserInfo()
        
        user.set_info(info[0], info[1], info[2], info[3])
        print "\n\nstart to fetch %s's money" % user.get_nickname()
        
        update_sql = "update user_info set fetch_flag = '%d' where nickname = '%s'" 
        
        strerr = ""
        errcode = 0
        cycle = 0
        while cycle < 1:
            cycle = 1
            #Step1 login
            errcode = user.step1_login(s, 'http://www.sjhy2016.com')
            if 0 != errcode:
                strerr = "fetch step1_login[%s] nickname = %s" %(self.error_msg[errcode], user.get_nickname())
                #self.ui.update("log", strerr)
                self.dbif.update_data(update_sql % (errcode, user.get_nickname()))
                break
                
            #Step2 Get Current Money
            maps, money, errcode = user.step2_get_money(s, 'http://www.sjhy2016.com/client/3login.aspx?url=usergetmoney.aspx')
            self.dbif.update_data(update_sql % (errcode, user.get_nickname()))
            if 0 != errcode:
                strerr = "fetch step2_get_money[%s] nickname = %s" %(self.error_msg[errcode], user.get_nickname())
                #self.ui.update("log", strerr)
                break
                    
            #Step3 Fetch Money
            errcode = user.step3_fetch_money(s, maps, money, 'http://www.sjhy2016.com/client/usergetmoney.aspx')
            if 0 != errcode:
                strerr = "fetch step3_fetch_money[%s] nickname = %s" %(self.error_msg[errcode], user.get_nickname())
                #self.ui.update("log", strerr)
                break
        
        if strerr != "":
            self.emit(SIGNAL("SIG_add_log(QString)"), QString(strerr))
            
        info[3] = errcode
        print "emit SIG_update_state"
        self.emit(SIGNAL("SIG_update_state(QString, int)"), QString(info[0]), errcode)
        #Close session
        s.close()

    g_info = [["yjj881", "555666", "888999", -1], ["yjj882", "555666", "888999", -1], ["yjj883", "555666", "888999", -1],
              ["yjj884", "555666", "888999", -1], ["yjj885", "555666", "888999", -1], ["yjj886", "555666", "888999", -1]]

    def _create_table(self):
        create_table_sql = """CREATE TABLE IF NOT EXISTS `user_info` (`nickname` VARCHAR(64) NOT NULL,`password` VARCHAR(45) NOT NULL,`secondpwd` VARCHAR(45) NOT NULL,
                            `fetch_date` DATE NULL,`fetch_flag` INT NOT NULL DEFAULT 0,PRIMARY KEY (`nickname`) )"""
        self.dbif.execute_sql(create_table_sql)

    def insert_data(self):
        insert_sql = ["""insert into user_info (nickname, password, secondpwd, fetch_flag) values('yjj881', '555666', '888999', '0')""",
                     """insert into user_info (nickname, password, secondpwd, fetch_flag) values('yjj882', '555666', '888999', '0')""",
                     """insert into user_info (nickname, password, secondpwd, fetch_flag) values('yjj883', '555666', '888999', '0')""",
                     """insert into user_info (nickname, password, secondpwd, fetch_flag) values('yjj884', '555666', '888999', '0')""",
                     """insert into user_info (nickname, password, secondpwd, fetch_flag) values('yjj885', '555666', '888999', '0')""",
                     """insert into user_info (nickname, password, secondpwd, fetch_flag) values('yjj886', '555666', '888999', '0')"""]
        
        for i in range(len(insert_sql)):
            self.dbif.insert_data(insert_sql[i])
        
        self.dbif.commit_routine()

    def update_flag(self, flag):
        update_sql = "update user_info set fetch_flag = %d" % flag
        self.dbif.begin_routine()
        self.dbif.execute_sql(update_sql)
        self.dbif.commit_routine()

    def load_user_info(self):
        strsql = "select nickname, password, secondpwd, fetch_flag from user_info"
        info = self.dbif.select_data(strsql)
        return info

    def fetch_money_start(self):
        strsql = "select nickname, password, secondpwd, -1 from user_info where fetch_flag < 0"
        info = self.dbif.select_data(strsql)
        print "info = ", info
    
        for i in range(len(info)):
            self.dbif.begin_routine()
            self._routine_run(info[i])
            self.dbif.commit_routine()
        
        print "\nFinish!"
        
    def run(self):
        self.dbif = Sqlite3If()
        self.dbif.connect('withdraw.db')
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
                self.update_flag(-9999)
            elif task[0] == "start":
                self.fetch_money_start()
            elif task[0] == "load":
                print "_Load_data"
                self.list_info = self.load_user_info()
                self.emit(SIGNAL("SIG_load_data()"))
            elif task[0] == "stop":
                self.thread_stop = True
            
            
                
