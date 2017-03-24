# -*- encoding=utf-8 -*-

from HTMLParser import HTMLParser
import urllib
import requests

import checknum

class MyHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.links = []
        self.maps = {}
        self.flag = False
        self.moneyflag = False
        self.money = -1
        self.index = 0
        
    def handle_starttag(self, tag, attrs):
        #print "Encountered the beginning of a %s tag" % tag
        if tag == "input":
            if len(attrs) == 0:
                pass
            else:
                key = ""
                for (variable, value) in attrs:
                    if value == "__VIEWSTATE" or value == "__EVENTVALIDATION":
                        key = value.encode("utf-8")
                        break;
                    
                if key == "":
                    return
                
                for (variable, value) in attrs:
                    if variable == "value":
                        self.maps[key] = value.encode("utf-8")
                        return
        
        if tag == "td":
            self.flag = True
            self.index = self.index + 1
            return
    
    def handle_data(self,data):
        #��������
        mydata = data
        mydata = mydata.strip()
        mydata = mydata.encode("utf-8")
        
        if self.flag == True :
            if self.moneyflag == True:
                self.money = int(float(mydata.encode("utf-8")))
                self.moneyflag = False
                #print "money = ", self.money
                return
                

            if mydata == "现金余额：":
                #print "label = ", mydata
                self.moneyflag = True
            #print "td = ", self.index, mydata
            #self.text = data
        
class UserInfo(object):
    def __init__(self):
        self.nickname = ""
        self.password = ""
        self.secondpwd = ""
        self.leftmoney = -1
    
    def set_info(self, nickname, password, secondpwd, leftmoney):
        self.set_nickname(nickname)
        self.set_password(password)
        self.set_secondpwd(secondpwd)
        self.set_leftmoney(leftmoney)
    
    def set_nickname(self, nickname):
        self.nickname = nickname
            
    def set_password(self, password):
        self.password = password
            
    def set_secondpwd(self, secondpwd):
        self.secondpwd = secondpwd
            
    def set_leftmoney(self, leftmoney):
        self.leftmoney = leftmoney
            
    def get_nickname(self):
        return self.nickname
            
    def get_password(self):
        return self.password
            
    def get_secondpwd(self):
        return self.secondpwd
            
    def get_leftmoney(self):
        return self.leftmoney
    
    def _save_to_file(self, r, htmlfile):
        if htmlfile != "":
            filepath = htmlfile
        else:
            filepath = "d:\\pic\\xx.html"
    
        file_object = open(filepath, 'wb')
        for chunk in r.iter_content():
            file_object.write(chunk)
        file_object.close( )
        #print "_debug_for_post = Ok" #, r.text 
   
    def _fetch_html(self, ss, url):
        parser = MyHTMLParser()
        
        r = ss.get(url)
        #print "r.text = ", r.text
        
        parser.feed(r.text)
        #print "parser.map = ", parser.map
        return parser.maps
    
    def _parse_html(self, strhtml):
        parser = MyHTMLParser()
        parser.feed(strhtml)
        
        return parser
        
    def _start_download(self, count, ss):
        imgurl = 'http://www.sjhy2016.com/createImg.aspx'
        #print 'Downloading...'  
        for i in range(count):
            savepath = 'd:\pic\createImg_%d.jpg' %i
            r = ss.get(imgurl)
            self._save_to_file(r, savepath)
            #print "ok download"
            #print "r.text = ", r.text
            
            #urllib.urlretrieve(imgurl, savepath)
        
        return

    def _send_login(self, maps, s):
        maps["nickname"] = self.get_nickname()
        maps["password"] = self.get_password()
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

    def step1_login(self, s, url):
        print "step1_login begin"
        maps = self._fetch_html(s, url)
        self._start_download(1, s)
        maps["verifycode"] = checknum.check_num()
        htmltext = self._send_login(maps, s)
        
        return htmltext
    
    def _step2_throw_into_web(self, s, url):
        maps = self._fetch_html(s, url)
        maps['ctl00$ContentPlaceHolder1$pass3'] = self.get_secondpwd()
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
        
        parser = self._parse_html(r.text)
        
        return parser.maps, parser.money
    
    def step2_get_money(self, s, url):
        print "step2_getmoney begin"
        maps, money = self._step2_throw_into_web(s, url)
        
        return maps, money
        """
        file_object = open("d:\\pic\\xx.html", 'wb')
        for chunk in r.iter_content():
            file_object.write(chunk)
        file_object.close( )
        print "r.text = Ok" #, r.text 
        return
        """
    
    def _step3_post_fetch_money(self, s, maps, money, url):
        money_int = (money / 100) * 100
        money_str = str(money_int)
        
        if money_int <= 0:
            self.set_leftmoney(money)
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
        parser = self._parse_html(r.text)
        self.set_leftmoney(parser.money)
        
    def step3_fetch_money(self, s, maps, money, url):
        print "step3_fetch_money begin"
        self._step3_post_fetch_money(s, maps, money, url)
        
        if self.get_leftmoney() != -1:
            print "fetch_OK nickname = %s left = %d" % (self.get_nickname(), self.get_leftmoney())
        else:
            print "fetch_failed nickname = %s" % self.get_nickname()
        
