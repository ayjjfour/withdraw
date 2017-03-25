# -*- encoding=utf-8 -*-

import sqlite3

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
        
    def insert_data(self, sqlstr):
        self.conn.execute(sqlstr)
        
    def select_data(self, sqlstr):
        data = []
        cursor = self.conn.execute(sqlstr)
        for row in cursor:
            rows = []
            for i in range(len(row)):
                rows.append(row[i])
            data.append(rows)
        return data
        
    def update_data(self, sqlstr):
        self.conn.execute(sqlstr)
        
    def execute_sql(self, strsql):
        return self.conn.execute(strsql)
