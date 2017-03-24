# -*- encoding=utf-8 -*-

import urllib
import requests

from classdef import *
import checknum

user = UserInfo()

def _save_to_file(r, htmlfile):
    if htmlfile != "":
        filepath = htmlfile
    else:
        filepath = "d:\\pic\\xx.html"

    file_object = open(filepath, 'wb')
    for chunk in r.iter_content():
        file_object.write(chunk)
    file_object.close( )
    #print "_debug_for_post = Ok" #, r.text 
   
            
def _fetch_html(ss, url):
    parser = MyHTMLParser()
    
    r = ss.get(url)
    #print "r.text = ", r.text
    
    parser.feed(r.text)
    #print "parser.map = ", parser.map
    return parser.maps

def _parse_html(strhtml):
    parser = MyHTMLParser()
    parser.feed(strhtml)
    
    return parser
    
def _start_download(count, ss):
    imgurl = 'http://www.sjhy2016.com/createImg.aspx'
    #print 'Downloading...'  
    for i in range(count):
        savepath = 'd:\pic\createImg_%d.jpg' %i
        r = ss.get(imgurl)
        _save_to_file(r, savepath)
        #print "ok download"
        #print "r.text = ", r.text
        
        #urllib.urlretrieve(imgurl, savepath)
    
    return

def _send_login(maps, s):
    maps["nickname"] = user.get_nickname()
    maps["password"] = user.get_password()
    maps["Button1.x"] = "59"
    maps["Button1.y"] = "13"
    #print "maps = ", maps
    
    payload = urllib.urlencode(maps)
                                
    headers = {"Content-Type": "application/x-www-form-urlencoded",
               "Accept":"text/html, application/xhtml+xml, */*",
               "Referer":"http://www.sjhy2016.com/",
               "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",
               "DNT":"1",
               "Accept-Language":"zh-CN",
               "Cache-Control":"no-cache"
               }
    
    r = s.post("http://www.sjhy2016.com", headers=headers, data=payload)
    
    return r.text

def step1_login(s, url):
    print "step1_login begin"
    maps = _fetch_html(s, url)
    _start_download(1, s)
    maps["verifycode"] = checknum.check_num()
    htmltext = _send_login(maps, s)
    
    return htmltext

def _step2_throw_into_web(s, url):
    maps = _fetch_html(s, url)
    maps['ctl00$ContentPlaceHolder1$pass3'] = user.get_secondpwd()
    maps['ctl00$ContentPlaceHolder1$Hidpdex'] = ""
    maps['ctl00$ContentPlaceHolder1$submit'] = '\xCC\xE1\xBD\xBB'
    maps['ctl00$ContentPlaceHolder1$hidurl'] = "usergetmoney.aspx"
    
    #print "_step2_throw_into_web maps = ", maps
    
    payload = urllib.urlencode(maps)
                                
    headers = {"Content-Type": "application/x-www-form-urlencoded",
               "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
               "Referer":"http://www.sjhy2016.com/client/3login.aspx?url=usergetmoney.aspx",
               "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",
               "Accept-Language":"zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
               "Upgrade-Insecure-Requests":"1"
               }
    
    r = s.post(url, headers=headers, data=payload)
    
    parser = _parse_html(r.text)
    
    return parser.maps, parser.money

def step2_get_money(s, url):
    print "step2_getmoney begin"
    maps, money = _step2_throw_into_web(s, url)
    
    return maps, money
    """
    file_object = open("d:\\pic\\xx.html", 'wb')
    for chunk in r.iter_content():
        file_object.write(chunk)
    file_object.close( )
    print "r.text = Ok" #, r.text 
    return
    """

def _step3_post_fetch_money(s, maps, money, url):
    money_int = (money / 100) * 100
    money_str = str(money_int)
    
    if money_int <= 0:
        user.set_leftmoney(money)
        return
    
    #print "_step2_post_fetch_money money_str = ", money_str
    
    maps["__EVENTTARGET"] = ""
    maps["__EVENTARGUMENT"] = ""
    maps["ctl00$ContentPlaceHolder1$TxtMoney"] = money_str
    maps["ctl00$ContentPlaceHolder1$txtopenpwd"] = "888999"
    maps["ctl00$ContentPlaceHolder1$TxtNote"] = ""
    maps["ctl00$ContentPlaceHolder1$Btnsub"] = "\xCC\xE1\xBD\xBB\xC9\xEA\xC7\xEB"
    maps["ctl00$ContentPlaceHolder1$Txtpageno"] = "1"
    maps["ctl00$ContentPlaceHolder1$HidPageno"] = "1"
    maps["ctl00$ContentPlaceHolder1$HidPagesize"] = "15"
    maps["ctl00$ContentPlaceHolder1$HidListcount"] = "28"
    maps["ctl00$ContentPlaceHolder1$HidCondition"] = ""
    #print "_step2_post_fetch_money maps = ", maps
    
    payload = urllib.urlencode(maps)
                                
    headers = {"Content-Type": "application/x-www-form-urlencoded",
               "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
               "Referer":"http://www.sjhy2016.com/client/usergetmoney.aspx",
               "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",
               "Accept-Language":"zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
               "Upgrade-Insecure-Requests":"1"
               }
    
    r = s.post(url, headers=headers, data=payload)
    #_save_to_file(r, "")
    parser = _parse_html(r.text)
    user.set_leftmoney(parser.money)
    
def step3_fetch_money(s, maps, money, url):
    print "step3_fetch_money begin"
    _step3_post_fetch_money(s, maps, money, url)
    
    if user.get_leftmoney() != -1:
        print "fetch_OK nickname = %s left = %d" % (user.get_nickname(), user.get_leftmoney())
    else:
        print "fetch_failed nickname = %s" % user.get_nickname()
    
def Start():
    s = requests.session()
    
    info = [["yjj881", "555666", "888999", -1], ["yjj882", "555666", "888999", -1], ["yjj883", "555666", "888999", -1],
            ["yjj884", "555666", "888999", -1], ["yjj885", "555666", "888999", -1], ["yjj886", "555666", "888999", -1]]
    
    for i in range(len(info)):
        user.set_info(info[i][0], info[i][1], info[i][2], info[i][3])
        print "\n\nstart to fetch %s's money" % user.get_nickname()
        
        #Step1 login
        step1_login(s, 'http://www.sjhy2016.com')
        
        #Step2 Get Current Money
        maps, money = step2_get_money(s, 'http://www.sjhy2016.com/client/3login.aspx?url=usergetmoney.aspx')
            
        #Step3 Fetch Money
        step3_fetch_money(s, maps, money, 'http://www.sjhy2016.com/client/usergetmoney.aspx')
        
        #Close session
        s.close()
    
Start();