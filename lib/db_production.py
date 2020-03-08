import psycopg2

class DB_Manager():
	@staticmethod
	def _getConn(perm="LOW"):
		if perm == "LOW":
			return psycopg2.connect("dbname=apiUser user=lowperm password=dca3729609c9c7b649bb host='127.0.0.1'")
		elif perm == "ALTER":
			return psycopg2.connect("dbname=apiUser user=insertperm password=cc663ef4d05c7055cba9 host='127.0.0.1'")
		elif perm == "AUTH":
			return psycopg2.connect("dbname=apiUser user=authperm password=eb6afa7b272eb7ffd531 host='127.0.0.1'")
	
	
	@staticmethod
	def execute(sql, perm="LOW"):
		conn = DB_Manager._getConn(perm)
		cur = conn.cursor()
		cur.execute(sql)
		conn.commit()
		return cur.fetchall()
		
		
 
	@staticmethod
	def authenticateUser(username, password):
		authed_users = DB_Manager.execute('''SELECT * FROM Authenticate_User('%s', '%s')''' % (username, password), "AUTH")
		print(authed_users)
		return authed_users
		

	@staticmethod
	def changePassword(username, password, salt):
		r = DB_Manager.execute('''SELECT * FROM Change_Password('%s', '%s', '%s');''' & (username, password, salt), "AUTH")
		print(r)
		return r

		
	@staticmethod
	def getUsername(UUID):
		user = DB_Manager.execute("LOW", '''SELECT username FROM Users WHERE (UUID='%s')''', UUID)
		if len(user) > 0:
			return user[0][0]
		else:
			return None
		
    @staticmethod
    def getUUID(username):
        user = DB_Manager.execute("LOW", '''SELECT UUID FROM Users WHERE (username='%s')''', username)
        if user == None: return None
        if len(user) > 0:
            return user[0][0]
        else:
            return None