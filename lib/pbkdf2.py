import math, hmac, hashlib, sys
from struct import pack

# Hashing algorithms writen in Python using specs drawn out in RFC specifications.
# See:
# https://tools.ietf.org/html/rfc2104
# https://www.ietf.org/rfc/rfc2898.txt
#
# Author: Niklas Henderson, UEA


class HMAC():
    """
    Simple Python implementation of the HMAC-SHA algorithm.
    Pseudorandom function used is SHA3-256 for best security practice. 
    See (pages.nist.gov/800-63-3/sp800-63b.html#memsecretver) for more info regarding password security.
    See (https://tools.ietf.org/html/rfc2104) for specification of HMAC algorithm. (With SHA1)
    
    Author: Niklas Henderson, UEA.
    """
    def __init__(self, string, secret_key):
        self.K = secret_key     #a salt of sorts.
        self.text = string      #data to encrypt
        
        self.ipad = b''         #inner padding
        self.opad = b''         #outer padding
        self.B = 136            #Block size (in bytes) of chosen hash (SHA3-256)
        self.L = 32             #Length of output (in bytes) from chosen hash (SHA3-256)
        self._initPadding()     #create padding of required length depending on input

    def _initPadding(self):
        for n in range(self.B):
            self.ipad += b'\x36'
            self.opad += b'\x5c'
            
        if(len(self.K) > self.B):   #If key is too large, hash to get correct size.
            self.K = self._H(self.K)
        for n in range(self.B - len(self.K)):   #apply padding
            self.K += b'\x00'

    def _H(self, key): 
        """Apply pseudorandom function to a key."""
        hash_func = hashlib.sha3_256(key)
        out_hash_func = hash_func.digest()
        return out_hash_func
    
    def _sxor(self, s1, s2):
        """Carries out and returns an xor on two bytes objects."""
        z1 = zip(s1, s2)
        out1 = []
        for x, y in z1:
            out1.append(x ^ y)
        return bytes(out1)
       
    def digest(self):
        """Uses pre-defined paramaters to calculate the hash. Output is in hexidecimal format."""
        first = self._sxor(self.K, self.opad)
        second = self._H(self._sxor(self.K, self.ipad)+self.text)
        return self._H(first + second).hex()
        
    






class pbkdf2():
    """
    Simple Python pbkdf2 Key Derevation Function.
    
    Performs a PBKDF2 hash on a string with a string salt, specified int rounds of hashing and key length.
    This uses the original specifications drawn out in RFC 2898 (https://www.ietf.org/rfc/rfc2898.txt)
    
    NIST recommends SHA3_256 as the hashing pseudorandom function, so HMAC-SHA-256 has been deployed.
    Rounds should be at least 10,000 (100,000 is better)
    See (https://www.ncsc.gov.uk/collection/passwords/updating-your-approach) and (pages.nist.gov/800-63-3/sp800-63b.html#memsecretver) for more info.
    
    Author: Niklas Henderson, UEA.
    """
    def __init__(self, password_, salt_, rounds_ = 10000, keyLen_=32):
        if rounds_<10000:
            raise ValueError("rounds of encryption should be at least 10,000, as recommended by NIST")
        if len(salt_) < 4:
            raise ValueError("Salt must be at least 32 bits in length, as recommended by NIST")
        if keyLen_ != 32:
            print("WARNING: keyLen should be same length as HMAC_SHA3_256 output (32 bytes)")
        self.hLen = 32      #hLen = num of octets from HMAC-SHA3-256
        
        if self.hLen > ((2**32) -1)*self.hLen:
            raise ValueError("Derived key too long")
        
        self.password = str(password_)
        self.salt = salt_
        self.rounds = rounds_
        self.keyLen = keyLen_
        
        
    def _sxor(self, s1, s2):
        """Carries out and returns an xor on two bytes objects."""
        z1 = zip(s1, s2)
        out1 = []
        for x, y in z1:
            out1.append(x ^ y)
        return bytes(out1)
    
    def _prf(self, P, S):
        """
        Uses a pseudorandom hashing functions on a string with a salt.
        HMAC-SHA3-256 is used in this simple implementation.
        """
        return hmac.new(P, S, hashlib.sha3_256).digest()
        
    
    def _f(self, P, S, c, i):
        """
        Calculates the XORd output of the pseudorandom function for a block.
        """
        U_N = []
        salt_c = S+pack("!L", i)			#L is long, which is 4 bytes long.
        U_0 = self._prf(P, salt_c)
        U_N.append(U_0)

        for n in range(1, c):
            U_c = self._prf(P, U_N[n-1])
            U_N.append(U_c)
        
        #then xor them together to return
        out = U_N[0]
        for n in range(1, c):
            out = self._sxor(out, U_N[n])
        return out
        

        
    def digest(self):
        """
        Uses pre-defined paramaters to calculate the hash. Output is in hexidecimal format.
        """
        
        dkLen = self.keyLen
        password_ = self.password
        salt_ = self.salt
        
        l_len = math.ceil(dkLen/self.hLen)			#how many seperate HMAC-SHA-256
        r = dkLen - (l_len-1) * self.hLen			#how many octets in the final hash
        T_N = []
        password_ = bytes(password_, 'utf-8')
        #salt_ = bytes(salt_, 'utf-8')              #assuming salt is already string bytes

        #for every 32 byte block
        for n in range(l_len):
            T_n = self._f(password_, salt_, self.rounds, n+1)
            T_N.append(T_n)

        out_hash = T_N[0][0:r]
        for n in range(1, len(T_N)):   #l_len should be r
            out_hash += T_N[n][0:r]

        return out_hash.hex()
	
    
    
    
if __name__ == "__main__":        
    salt = bytes("abc123".encode())
    pwd = bytes("password".encode())
    print("HMAC-SHA3-256 output: "+str(hmac.new(salt, pwd, hashlib.sha3_256).digest().hex()))
    mycrypto = HMAC(pwd, salt)
    print("My cryptographic function: "+str(mycrypto.digest()))
