import sqlite3

class DB_Manager():
    @staticmethod
    def _getConn():
        return sqlite3.connect('database.db')
    
    
    @staticmethod
    def execute(sql):
        #print(sql)
        cur = DB_Manager._getConn().cursor()
        cur.execute(sql)
        return cur.fetchall()
        
    def safeExecute(sql):
        pass
        
        
        
        
        
        
        
        
        
        
        