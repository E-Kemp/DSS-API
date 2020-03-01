import sqlite3

class DB_Manager():
    @staticmethod
    def _getConn():
        return sqlite3.connect('database.db')
    
    
    @staticmethod
    def execute(sql):
        #print(sql)
        conn = DB_Manager._getConn()
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
        return cur.fetchall()
        
    def safeExecute(sql):
        pass
        
        
        
        
        
        
        
        
        
        
        