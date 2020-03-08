import sqlite3, re

class DB_Manager():
    @staticmethod
    def _getConn(perm="LOW"):
        return sqlite3.connect('database.db')
    
    
    #def myFun(*argv):  
    #for arg in argv:  
    #    print (arg) 
    
    @staticmethod
    def execute(perm, sql, *argv):
        if 'SELECT' in sql: query_type = "getData"
        else: query_type = "insertData"
        
        sql_args = []
        for arg in argv:
            sql_args.append(DB_Manager.filter(arg))
            
        sql_args_tuple = tuple(sql_args)        
        final_sql = (sql % sql_args_tuple)
        conn = DB_Manager._getConn()
        cur = conn.cursor()
        ret = 0
        
        if query_type == "getData":
            try:
                cur.execute(final_sql)
                conn.commit()
                ret = cur.fetchall()
                if ret == None: return None
                elif len(ret) == 0: return None
                else: return ret
                    
                
            except Exception as e:
                print("ERROR in execute-GETDATA. Message: ", str(e))
                return None
            
        elif query_type == "insertData":
            try:
                cur.execute(final_sql)
                conn.commit()
                ret = cur.fetchall()
                if ret == None: return "success"
                elif len(ret) == 0: return "success"
                else: return None
                
            except Exception as e:
                print("ERROR in execute-INSERTDATA. Message: ", str(e))
                return None
         
        else:
            return None
        
        
        
    
        
 
    @staticmethod
    def authenticateUser(username, password):
        try:
            authed_users = DB_Manager.execute("AUTH", '''SELECT * 
            FROM Users INNER JOIN User_Auth 
            ON (Users.UUID = User_Auth.UUID) 
            WHERE (Users.username='%s' AND User_Auth.password='%s' AND User_Auth.verified='TRUE')''', username, password)
            print("Returned string: ",authed_users)
            if authed_users == None:
                return False
            if len(authed_users) > 0:
                return True
            else:
                return False
        except Exception as e:
            return False
        
    @staticmethod
    def changePassword(username, password, salt, veri_code):
        action = ""
        try:
            curr_UUID = DB_Manager.getUUID(username)
            if curr_UUID == None: return None
            num_Auth_records = DB_Manager.execute("AUTH", '''SELECT COUNT(*) FROM User_Auth WHERE (UUID='%s');''', curr_UUID)
            if len(num_Auth_records) == 0: action = "insert"
            else: num_Auth_records = num_Auth_records[0][0]
            if num_Auth_records > 0: action = "update"
            else: action = "insert"
            
            if action == "update":
                DB_Manager.execute("AUTH", '''UPDATE User_Auth SET password='%s', salt='%s' WHERE (UUID='%s');''', password, salt, curr_UUID)
            if action == "insert":
                DB_Manager.execute("AUTH", '''INSERT INTO User_Auth VALUES ('%s', '%s', '%s', 'FALSE', '%s');''', curr_UUID, password, salt, veri_code)
            ret = 0
        except Exception as e:
            print("ERROR in changePassword: ", str(e))
            ret = None
        return ret

    @staticmethod
    def getUUID(username):
        user = DB_Manager.execute("LOW", '''SELECT UUID FROM Users WHERE (username='%s')''', username)
        if user == None: return None
        if len(user) > 0:
            return user[0][0]
        else:
            return None
    
    @staticmethod
    def getUsername(UUID):
        user = DB_Manager.execute("LOW", '''SELECT username FROM Users WHERE (UUID='%s')''', UUID)
        if len(user) > 0:
            return user[0][0]
        else:
            return None
        
        
        
        
    @staticmethod
    def filterSQL(text):
        """
        Created on Thu Feb 13 13:24:51 2020

        @author: Leem
        """
    
        keywords = {
             "'" : '@apos', '0x27': '@apos',  
             '"' : '@quot','0x22': '@quot',
             '&' : '@amp', '0x26': '@amp'
             }
        
        
        for key in keywords:
            text = text.replace(key, keywords[key])
        return text
        
        
        
        
    def filterJS(text):
        """
        Created on Thu Feb 13 13:24:51 2020

        @author: Leem
        """
        if text == None: return ''
        keywords = {
            '<': '</', '0x3c': '@lt', 
            '>': '>/', '0x3e': '@gt', 
            '&' : '&/', '0x26': '@amp'
            }
        for key in keywords:
            text = text.replace(key, keywords[key])
        return text
        
        
        
    def filter(text):
        """
        Created on Thu Feb 13 13:24:51 2020

        @author: Leem
        """       
        if text == None: return ''
        keywords = {
            '<': '@lt ', '0x3c': '@lt', 
            '>': '@gt ', '0x3e': '@gt', 
            "'" : '@apos ', '0x27': '@apos',  
            '"' : '@quot ','0x22': '@quot',
            '/' : '@bksl',
            '&' : '@amp ', '0x26': '@amp'
            }
        for key in keywords:
            text = text.replace(key, keywords[key])
        return text
        

        
        