# -*- encoding=utf-8 -*-

from HTMLParser import HTMLParser
import urllib
import requests

import checknum

class MyHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.links = []
        self.maps = {"__VIEWSTATE":"", "__EVENTVALIDATION":""}
        self.flag = False
        self.pflag = False
        self.moneyflag = False
        self.pmoneyflag = False
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
        
        if tag == "p":
            self.pflag = True
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
                self.flag = False
                return
            
            if mydata == "现金余额：":
                #print "label = ", mydata
                self.moneyflag = True
            #print "td = ", self.index, mydata
            #self.text = data
            
        if self.pflag == True:
            if self.pmoneyflag == True:
                self.money = int(float(mydata.encode("utf-8")))
                self.pmoneyflag = False
                #print "money = ", self.money
                self.flag = False
                return
            
            if mydata == "现金：":
                #print "label = ", mydata
                self.pmoneyflag = True
            #print "p = ", self.index, mydata
        
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
        
        _pwd_err_VIEWSTATE = "/wEPDwUINzc3NzY4NTYPZBYCAgEPZBYCAgsPDxYCHgRUZXh0BT08c2NyaXB0PmFsZXJ0KCfmgqjnmoTmtojotLnogIVJROWvhueggeS4jeato+ehru+8gScpPC9zY3JpcHQ+ZGQYAQUeX19Db250cm9sc1JlcXVpcmVQb3N0QmFja0tleV9fFgEFB0J1dHRvbjEVlT6Bq1o4H72vcDF8jATgRd6ikDNzQr5cRYRoW3uJKw=="
        _pwd_err_EVENTVALIDATION = "/wEWBQKU4q/KBwKE6PygBALyveCRDwLy1ffTCgKM54rGBhcz5tXSHx+VSq7eWnbRF8j0okB8QWDCxkYNN/ZwDbgD"
        _chk_err_VIEWSTATE = "/wEPDwUINzc3NzY4NTYPZBYCAgEPZBYCAgsPDxYCHgRUZXh0BTs8c2NyaXB0PmFsZXJ0KCfmgqjovpPlhaXnmoTpqozor4HnoIHkuI3mraPnoa7vvIEnKTwvc2NyaXB0PmRkGAEFHl9fQ29udHJvbHNSZXF1aXJlUG9zdEJhY2tLZXlfXxYBBQdCdXR0b24xrZt0kYV0TlSCJbV22ac8OoTPrgn1wI1iFuGoyt8v35U="
        _chk_err_EVENTVALIDATION = "/wEWBQL9zdrUBAKE6PygBALyveCRDwLy1ffTCgKM54rGBvBLCGpFwL8IKXKP5lVGWe8gbScxXGwRlGE/1ch/xEOO"
        
        r = s.post("http://www.sjhy2016.com", headers=headers, data=payload)
        parser = self._parse_html(r.text)
        
        if (parser.maps["__VIEWSTATE"] == _chk_err_VIEWSTATE) and (parser.maps["__EVENTVALIDATION"] == _chk_err_EVENTVALIDATION):
            return -2
        elif (parser.maps["__VIEWSTATE"] == _pwd_err_VIEWSTATE) and (parser.maps["__EVENTVALIDATION"] == _pwd_err_EVENTVALIDATION):
            return -1
        elif parser.money < 100:
            self.set_leftmoney(8000 + parser.money)
            return 1
        else:   # 继续提取现金
            return 0

    def step1_login(self, s, url):
        print "step1_login begin"
        maps = self._fetch_html(s, url)
        self._start_download(1, s)
        maps["verifycode"] = checknum.check_num()
        errorcode = self._send_login(maps, s)
        
        return errorcode
    
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
        errorcode = 0
        if parser.money == -1:
            errorcode = -1
          
        return parser.maps, parser.money, errorcode
    
    def step2_get_money(self, s, url):
        print "step2_getmoney begin"
        maps, money, errorcode = self._step2_throw_into_web(s, url)
        
        return maps, money, errorcode
    
    def _step3_post_fetch_money(self, s, maps, money, url):
        money_int = (money / 100) * 100
        money_str = str(money_int  + 20)
        
        if money_int <= 0:
            self.set_leftmoney(8000 + money)
            return 1
        
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
        parser = self._parse_html(r.text)
        
        errcode = 0
        if parser.money >= 100:
            errcode = -1
        
        self.set_leftmoney(parser.money)
        
        return errcode
        
    def step3_fetch_money(self, s, maps, money, url):
        print "step3_fetch_money begin"
        return self._step3_post_fetch_money(s, maps, money, url)
        
        #return self.get_leftmoney()

        
