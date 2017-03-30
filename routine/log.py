# -*- encoding=utf-8 -*-
from __builtin__ import file
import os
import datetime

class Log(object):
    def __init__(self):
        self._openfile()
        self.level = 0
       
    def __del__(self):
        if self.fd != None:
            self.fd.close()
            
    def _openfile(self):
        path = os.getcwd()
        path = path + "/log/"
        print "path = ", path
        if not os.path.exists(path):
            os.makedirs(path)
            
        self.file = path + datetime.datetime.now().strftime('%Y-%m-%d') + ".log";
        self.fd = open(self.file, "a+")
          
    def reopen(self):
        self.close()
        self._openfile()
        
    def setlevel(self, level):
        self.level = level
        
    def write(self, strlog, level = 0):
        if self.level > level:
            return
        
        strmsg = datetime.datetime.now().strftime(u'[%Y-%m-%d %HH:%MM:%SS] ')
        strmsg = strmsg + strlog
        print strmsg
        self.fd.write((strmsg + u"\n").encode('utf-8'))
        self.fd.flush()
        
        return strmsg
        
    def close(self):
        if self.fd != None:
            self.fd.close()
            self.fd = None