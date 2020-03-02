import os, datetime, time

class Cookie_struct():
    def __init__(self, HTTPOnly=True, _lifetime=2):
        self.cookies = {}       #Cookie: uername, ip address, date
        self.lifetime = _lifetime
        
    def _validate(self, ip, cookie):
        #ensure the IP is the same for the two cookie usage requests.
        if ip != self.cookies[cookie]["ip"]:
            return False
        
        #ensure the cookie is still within lifetime
        dateDiff = datetime.datetime.now() - self.cookies[cookie]["datetime"]
        if (dateDiff.total_seconds()/3600) > self.lifetime:
            return False
        
        return True
        
        
        
    def getUser(self, cookie, ip):
        if not self._validate(ip, cookie):
            return None
        else:
            return self.cookies[cookie]
            
    def deleteCookie(self, cookie, ip):
        if not self._validate(ip, cookie):
            return False
        else:
            del self.cookies[cookie]
            return True
            
    def createCookie(self, username, ip):
        #https://owasp.org/www-project-cheat-sheets/cheatsheets/Session_Management_Cheat_Sheet.html
        #cookie length - at least 16 bytes
        #must be meaningless - to prevent information dislosure attacks
        cookie = Token_generator.new_crypto_bytes(20)
        creation_datetime = datetime.datetime.now()
        
        self.cookies[cookie] = {
            "username":username,
            "ip":ip,
            "datetime":creation_datetime
        }
        
        return cookie
        
    def _toString(self):
        for cookie in self.cookies:
            print(cookie.hex())
        
        
        
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