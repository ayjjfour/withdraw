# -*- encoding=utf-8 -*-

import sqlite3
import types

class Sqlite3If(object):
    def __init__(self):
        self.db = ""
        return
    
    def connect(self, db):
        
        if db == '':
            return
        self.db = db
        
        self.conn = sqlite3.connect(db)
    
    def close(self):
        self.conn.close()    
    
    def begin_routine(self):
        return
        
    def commit_routine(self):
        self.conn.commit()
        
    def insert_data(self, strsql):
        try:
            self.conn.execute(strsql)
        except:
            print 'insert_data except'
        
    def select_data(self, strsql):
        data = []
        try:
            cursor = self.conn.execute(strsql)
        except:
            print "select_data excpt"
            return
        
        for row in cursor:
            rows = []
            for i in range(len(row)):
                if type(row[i]) is types.StringType:
                    rows.append(row[i].decode('ascii').encode('utf-8'))
                else:
                    rows.append(row[i])
            data.append(rows)
        return data
        
    def update_data(self, strsql):
        try:
            self.conn.execute(strsql)
        except:
            print 'update_data except'
        
    def execute_sql(self, strsql):
        try:
            self.conn.execute(strsql)
        except:
            print 'execute_sql except'
