# -*- encoding=utf-8 -*-


import requests

from classdef import *

from time import sleep, ctime 
import threading


def routine_run(info):
    s = requests.session()
    user = UserInfo()
    
    user.set_info(info[0], info[1], info[2], info[3])
    print "\n\nstart to fetch %s's money" % user.get_nickname()
        
    #Step1 login
    user.step1_login(s, 'http://www.sjhy2016.com')
        
    #Step2 Get Current Money
    maps, money = user.step2_get_money(s, 'http://www.sjhy2016.com/client/3login.aspx?url=usergetmoney.aspx')
            
    #Step3 Fetch Money
    user.step3_fetch_money(s, maps, money, 'http://www.sjhy2016.com/client/usergetmoney.aspx')
        
    #Close session
    s.close()
    
def Start():
        
    info = [["yjj880", "555666", "888999", -1], ["yjj882", "555666", "888999", -1], ["yjj883", "555666", "888999", -1],
            ["yjj884", "555666", "888999", -1], ["yjj885", "555666", "888999", -1], ["yjj886", "555666", "888999", -1]]
    threads = []
    
    for i in range(len(info)):
        t = threading.Thread(target=routine_run,args=(info[i],))
        threads.append(t)

    for i in range(len(info)):
        threads[i].start()
        
    for i in range(len(info)):
        threads[i].join()
    
Start();