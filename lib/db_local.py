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
        ret = 0
        try:
            cur.execute(sql)
            conn.commit()
            ret = cur.fetchall()
            if ret==None:ret="success"
        except Exception as e:
            print("ERROR. Message: ", str(e))
            ret = None
        return ret
        
 
 
    @staticmethod
    def authenticateUser(username, password):
        authed_users = DB_Manager.execute('''SELECT * 
        FROM Users INNER JOIN User_Auth 
        ON (Users.UUID = User_Auth.UUID) 
        WHERE (Users.username='%s' AND User_Auth.password='%s' AND User_Auth.verified=TRUE)''' % (username, password), "AUTH")
        print("Returned string: ",authed_users)
        if len(authed_users) > 0:
            return True
        else:
            return False
        
    @staticmethod
    def changePassword(username, password, salt, veri_code):
        try:
            curr_UUID = DB_Manager.execute('''SELECT Users.UUID FROM Users WHERE (username = '%s');''' % (username), "AUTH")[0][0]
            num_Auth_records = DB_Manager.execute('''SELECT COUNT(*) FROM User_Auth WHERE (UUID='%s');''' % (curr_UUID), "AUTH")[0][0]
            #print("CURR UUID: ",curr_UUID)
            #print("num auth records: ", num_Auth_records)
            if num_Auth_records > 0:
                DB_Manager.execute('''UPDATE User_Auth SET password='%s', salt='%s' WHERE (UUID='%s');''' % (password, salt, curr_UUID), "AUTH")
            else:
                DB_Manager.execute('''INSERT INTO User_Auth VALUES ('%s', '%s', '%s', '%s');''' % (curr_UUID, password, salt, veri_code), "AUTH")
            ret = 0
        except Exception as e:
            print("ERROR: ", str(e))
            ret = None
        return ret

    @staticmethod
    def getUUID(username):
        user = DB_Manager.execute('''SELECT * FROM Users WHERE (username='%s')''' % (username), "LOW")
        if len(user) > 0:
            return user[0][0]
        else:
            return None
    
    @staticmethod
    def getUsername(UUID):
        user = DB_Manager.execute('''SELECT * FROM Users WHERE (UUID='%s')''' % (UUID), "LOW")
        if len(user) > 0:
            return user[0][1]
        else:
            return None
        
        
        
        
        