# -*- encoding=utf-8 -*-

from HTMLParser import HTMLParser

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
