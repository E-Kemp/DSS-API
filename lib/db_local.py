import sqlite3

class DB_Manager():
    @staticmethod
    def _getConn(perm="LOW"):
        return sqlite3.connect('database.db')
    
    
    @staticmethod
    def execute(sql, perm="LOW"):
        #print(sql)
        conn = DB_Manager._getConn()
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
        return cur.fetchall()
        
 
 
    @staticmethod
    def authenticateUser(username, password):
        authed_users = DB_Manager.execute('''SELECT * 
        FROM Users INNER JOIN User_Auth 
        ON (Users.UUID = User_Auth.UUID) 
        WHERE (Users.username='%s' AND User_Auth.password='%s')''' % (username, password), "AUTH")
        
        if len(authed_users) > 0:
            return True
        else:
            return False
        
    @staticmethod
    def changePassword(username, password, salt):
        curr_UUID = DB_Manager.execute('''SELECT Users.UUID FROM Users WHERE (username = '%s');''' % (username), "AUTH")[0][0]
        num_Auth_records = DB_Manager.execute('''SELECT COUNT(*) FROM User_Auth WHERE (UUID='%s');''' % (curr_UUID), "AUTH")[0][0]
        #print("CURR UUID: ",curr_UUID)
        #print("num auth records: ", num_Auth_records)
        if num_Auth_records > 0:
            DB_Manager.execute('''UPDATE User_Auth SET password='%s', salt='%s' WHERE (UUID='%s');''' % (password, salt, curr_UUID), "AUTH")
        else:
            DB_Manager.execute('''INSERT INTO User_Auth VALUES ('%s', '%s', '%s');''' % (curr_UUID, password, salt), "AUTH")

        
        
        
        
        
        
        