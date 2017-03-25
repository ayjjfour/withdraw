# -*- encoding=utf-8 -*-


import requests
from classdef import *
from mysqlif import *
from sqliteif import *

error_msg = {'step1':{-2:"check code error",
                      -1:"password error", 
                       0:"ok", 
                       1:"money has been fetched"},
             
             'step2':{-1:"second password error",
                       0:"ok"},
             
             'step3':{ -1:"fetch money failed", 
                       0:"ok", 
                       1:"money has been fetched"}}

def routine_run(info, dbif):
    s = requests.session()
    user = UserInfo()
    
    user.set_info(info[0], info[1], info[2], info[3])
    print "\n\nstart to fetch %s's money" % user.get_nickname()
    
    update_sql = "update user_info set fetch_flag = '%d' where nickname = '%s'" 
    
    step = ''
    errcode = 0
    cycle = 0
    while cycle < 1:
        cycle = 1
        #Step1 login
        step = 'step1'
        errcode = user.step1_login(s, 'http://www.sjhy2016.com')
        print "fetch step1_login[%s] nickname = %s" %(error_msg[step][errcode], user.get_nickname())
        if 0 != errcode:
            dbif.update_data(update_sql % (errcode, user.get_nickname()))
            break
            
        #Step2 Get Current Money
        step = 'step2'
        maps, money, errcode = user.step2_get_money(s, 'http://www.sjhy2016.com/client/3login.aspx?url=usergetmoney.aspx')
        dbif.update_data(update_sql % (errcode, user.get_nickname()))
        if 0 != errcode:
            print "fetch step2_get_money[%s] nickname = %s" %(error_msg[step][errcode], user.get_nickname())
            break
                
        #Step3 Fetch Money
        step = 'step3'
        errcode = user.step3_fetch_money(s, maps, money, 'http://www.sjhy2016.com/client/usergetmoney.aspx')
        if 0 != errcode:
            print "fetch step3_fetch_money[%s] nickname = %s" %(error_msg[step][errcode], user.get_nickname())
            break
        
    #Close session
    s.close()
    
g_info = [["yjj881", "555666", "888999", -1], ["yjj882", "555666", "888999", -1], ["yjj883", "555666", "888999", -1],
          ["yjj884", "555666", "888999", -1], ["yjj885", "555666", "888999", -1], ["yjj886", "555666", "888999", -1]]
    
def _create_table(dbif):
    create_table_sql = """CREATE TABLE IF NOT EXISTS `user_info` (`nickname` VARCHAR(64) NOT NULL,`password` VARCHAR(45) NOT NULL,`secondpwd` VARCHAR(45) NOT NULL,
                        `fetch_date` DATE NULL,`fetch_flag` INT NOT NULL DEFAULT 0,PRIMARY KEY (`nickname`) )"""
    dbif.excuse_sql(create_table_sql)
    
def _insert_data(dbif):
    insert_sql = ["""insert into user_info (nickname, password, secondpwd, fetch_flag) values('yjj881', '555666', '888999', '0')""",
                 """insert into user_info (nickname, password, secondpwd, fetch_flag) values('yjj882', '555666', '888999', '0')""",
                 """insert into user_info (nickname, password, secondpwd, fetch_flag) values('yjj883', '555666', '888999', '0')""",
                 """insert into user_info (nickname, password, secondpwd, fetch_flag) values('yjj884', '555666', '888999', '0')""",
                 """insert into user_info (nickname, password, secondpwd, fetch_flag) values('yjj885', '555666', '888999', '0')""",
                 """insert into user_info (nickname, password, secondpwd, fetch_flag) values('yjj886', '555666', '888999', '0')"""]
    
    for i in range(len(insert_sql)):
        dbif.insert_data(insert_sql[i])
    
    dbif.commit_routine()
    
def _update_flag(dbif, flag):
    update_sql = "update user_info set fetch_flag = %d" % flag
    dbif.execute_sql(update_sql)
    dbif.commit_routine()
    
def Start():
    """
    dbif = MySQLIf()
    dbif.connect('127.0.0.1', 3306, 'yuanjj', "12345678", "withdraw")
    """
    dbif = Sqlite3If()
    dbif.connect('withdraw.db')
    dbif.begin_routine()
    
    # 创建表
    #_create_table(dbif)
    
    # 插入数据
    #_insert_data(dbif)
    
    # 更新标志
    _update_flag(dbif, -99)
    
    strsql = "select nickname, password, secondpwd, -1 from user_info where fetch_flag < 0"
    info = dbif.select_data(strsql)
    print "info = ", info

    for i in range(len(info)):
        routine_run(info[i], dbif)
        dbif.commit_routine()
    
    dbif.close()
    
    print "\nFinish!"
    
Start();