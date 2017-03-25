# -*- encoding=utf-8 -*-

import MySQLdb

class MySQLIf(object):
    def __init__(self):
        self.host = '127.0.0.1'
        self.port = 3306
        self.user = 'root'
        self.passwd = '12345678'
        self.db = ''
        return
    
    def connect(self, host, port, user, passwd, db):
        if host != '':
            self.host = host
            
        if port != 0:
            self.port = port
            
        if user == '':
            return
        self.user = user
            
        if passwd == '':
            return
        self.passwd = passwd
        
        if db == '':
            return
        self.db = db
        
        self.conn = MySQLdb.connect(host = self.host, port = port, user = user, passwd = passwd, db = db, charset = 'utf8')
    
    def close(self):
        self.conn.close()
        
    def begin_routine(self):
        self.cur = self.conn.cursor()
        return
        
    def commit_routine(self):
        self.cur.close()
        self.conn.commit()
        
    def insert_data(self, sqlstr, datalist):
        self.cur.excutemany(sqlstr, datalist)
        
    def select_data(self, sqlstr):
        count = self.cur.execute(sqlstr)
        return self.cur.fetchmany(count)
        
    def update_data(self, sqlstr):
        self.cur.execute(sqlstr)
        
    def excuse_sql(self, strsql):
        return self.cur.execute(strsql)