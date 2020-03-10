import os, datetime, time, json

class Cookie_struct():
    def __init__(self, HTTPOnly=True, _lifetime=2):
        self.cookies = {}       #Cookie: UUID, ip address, date
        self.lifetime = _lifetime
        
    def _validate(self, ip, cookie):
        #ensure the IP is the same for the two cookie usage requests.
        print("MY COOKIE: ", cookie)
        print("COOKIE STRUCT: ", self.cookies)
        if cookie not in self.cookies:
            return False
        if ip != self.cookies[cookie]["ip"]:
            return False
        
        #ensure the cookie is still within lifetime
        dateDiff = datetime.datetime.now() - self.cookies[cookie]["datetime"]
        if (dateDiff.total_seconds()/3600) > self.lifetime:
            return False
        return True
        
    def validateCSRF(self, S_ID, token):
        try:
            return self.cookies[S_ID]["csrf"] == token
        except Exception as e:
            print("ERROR in validateCSRF: ", str(e))
            
    def getCSRF(self, S_ID):
        return self.cookies[S_ID]["csrf"]
    
    
    def getUUID(self, cookie, ip):
        if not self._validate(ip, cookie):
            return None
        else:
            return self.cookies[cookie]["UUID"]
            
    def deleteCookie(self, cookie, ip):
        if not self._validate(ip, cookie):
            print("Cookie not valid!")
            return False
        else:
            del self.cookies[cookie]
            return True
            
    def createBlankCookie(self):
        return ""
        
        
        
        
    def createCookie(self, UUID, ip):
        #https://owasp.org/www-project-cheat-sheets/cheatsheets/Session_Management_Cheat_Sheet.html
        #cookie length - at least 16 bytes
        #must be meaningless - to prevent information dislosure attacks
        cookie = Token_generator.new_crypto_bytes(20).hex()
        csrf_token = Token_generator.new_crypto_bytes(20).hex()
        creation_datetime = datetime.datetime.now()
        
        self.cookies[cookie] = {
            "UUID":UUID,
            "ip":ip,
            "datetime":creation_datetime,
            "csrf":csrf_token
        }
        
        return cookie
        
    def _toString(self):
        for cookie in self.cookies:
            print(cookie)
    
    def saveSessions(self):
        with open('sessions.json', 'w') as outfile:
            json.dump(self.cookies, outfile)
    def getSessions(self):
        data = open('config/HEADERS_local.conf', 'r')
        return json.load(data)

class CSRF_tokens_struct():
    def __init__(self):
        self.CSRF_tokens = {}   #
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