import os, datetime, time, json
from db_local import DB_Manager

class Cookie_struct():
	def __init__(self, HTTPOnly=True, _lifetime=2):
		self.cookies = {}		#Cookie: UUID, ip address, date
		self.lifetime = _lifetime
		
	def _validate(self, ip, cookie):
		#ensure the IP is the same for the two cookie usage requests.
		print("MY COOKIE: ", cookie)
		all_cookies = self.getAllCookies()
		print("COOKIE STRUCT: ", all_cookies)
		#if cookie not in self.cookies:
		#	 return False
		#if ip != self.cookies[cookie]["ip"]:
		#	 return False
		
		fetched_cookies = DB_Manager.execute("AUTH", '''SELECT * FROM Sessions WHERE (cookie='%s')''', cookie)
		if fetched_cookies == None: return False
		elif len(fetched_cookies) == 0: return False
		else: return True
		
		#ensure the cookie is still within lifetime
		#dateDiff = datetime.datetime.now() - self.cookies[cookie]["datetime"]
		#if (dateDiff.total_seconds()/3600) > self.lifetime:
		#	 return False
		
		return True
		
	def validateCSRF(self, S_ID, token):
		try:
			cookie = self.getCookieByToken(S_ID)
			if cookie == None: return False
			else: return cookie[0][3] == token
		except Exception as e:
			print("ERROR in validateCSRF: ", str(e))
			return False
			
	def getCSRF(self, S_ID):
		cookie = self.getCookieByToken(S_ID)
		if cookie == None: return ''
		return cookie[0][3]
	
	
	def getUUID(self, cookie, ip):
		if not self._validate(ip, cookie):
			return None
		else:
			cookie = self.getCookieByToken(cookie)
			if cookie == None: return None
			else:
				return cookie[0][0]
			
	def deleteCookie(self, cookie, ip):
		if not self._validate(ip, cookie):
			print("Cookie not valid!")
			return False
		else:
			DB_Manager.execute("AUTH", '''DELETE FROM Sessions WHERE (cookie='%s');''', cookie)
			return True
			
	def createBlankCookie(self):
		return ""
		
		
		
		
	def createCookie(self, UUID, ip):
		#https://owasp.org/www-project-cheat-sheets/cheatsheets/Session_Management_Cheat_Sheet.html
		#cookie length - at least 16 bytes
		#must be meaningless - to prevent information dislosure attacks
		currCookie = self.getCookieByUUID(UUID)
		
		if currCookie == None: currCookie = []
		for c in currCookie:
			self.deleteCookie(c[1], c[2])
		
		
		cookie = Token_generator.new_crypto_bytes(20).hex()
		csrf_token = Token_generator.new_crypto_bytes(20).hex()
		creation_datetime = datetime.datetime.now()
		DB_Manager.execute("AUTH", '''INSERT INTO Sessions VALUES ('%s', '%s', '%s', '%s')''', UUID, cookie, ip, csrf_token)

		
		return cookie
		
	def _toString(self):
		for cookie in self.cookies:
			print(cookie)
	
	def clearCookies(self):
		DB_Manager.execute("AUTH", '''DELETE FROM Sessions;''')
		
	def getAllCookies(self):
		total_cookies = DB_Manager.execute("AUTH", '''SELECT * FROM Sessions''')
		if total_cookies == None: return []
		else:return total_cookies
	
	def getCookieByUUID(self, UUID):
		cookies = DB_Manager.execute("AUTH", '''SELECT * FROM Sessions WHERE (UUID='%s')''', UUID)
		if cookies == None: return None
		elif len(cookies) == 0: return None
		else: return cookies
	
	def getCookieByToken(self, token):
		cookies = DB_Manager.execute("AUTH", '''SELECT * FROM Sessions WHERE (cookie='%s')''', token)
		if cookies == None: return None
		elif len(cookies) == 0: return None
		else: return cookies
		
		
		
		
	def saveSessions(self):
		with open('sessions.json', 'w') as outfile:
			json.dump(self.cookies, outfile)
	def getSessions(self):
		data = open('config/HEADERS_local.conf', 'r')
		return json.load(data)

class CSRF_tokens_struct():
	def __init__(self):
		self.CSRF_tokens = {}	#
	def generate_token(self, user_UUID):
		pass
		
	



		
class Token_generator():
	@staticmethod
	def new_crypto_bytes(size):
		#this is cryptographically secure. See https://docs.python.org/3/library/os.html
		return os.urandom(size) 
		
		
		
if __name__ == "__main__":
	c = Cookie_struct(True, 6)
	cookie = c.createCookie("14henderson", "127.0.0.1")
	time.sleep(5)
	print("Got user?", c.getUser(cookie, "127.0.0.1"))
	c._toString()