import datetime


# Describes a collection of methods that add different headers server responses
# This includes HTTP headers, and Cookie headers
# See:
#   https://www.thesslstore.com/blog/what-is-hypertext-strict-transport-security-hsts/
#   https://owasp.org/www-project-secure-headers/
# @Author: Niklas Henderson, UEA


class Headers():
    """
    A collection of static methods that add different headers server responses
    This includes HTTP headers, and Cookie headers
    See:
      https://www.thesslstore.com/blog/what-is-hypertext-strict-transport-security-hsts/
      https://owasp.org/www-project-secure-headers/
    @Author: Niklas Henderson, UEA
    """
    
    @staticmethod
    def addResponseHeaders(response):
        response.headers['Access-Control-Allow-Origin'] = '*'#'https://www.the-pirate-cove572851084171.co.uk'
        response.headers['X-Frame-Options'] = 'SAMEORIGIN'
        response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains' #see https://www.thesslstore.com/blog/what-is-hypertext-strict-transport-security-hsts/
        response.headers['X-XSS-Protection'] = '1; mode=block' #see https://owasp.org/www-project-secure-headers/
        #include content security policy header when have time
        
        return response
        
        
    @staticmethod
    def addCookie(response, name, value):
        cookieSetString = ""
        cookieSetString += name+"="+value+";"
        
        lifetime = 2*60*60
        expires = datetime.datetime.now() + datetime.timedelta(hours=2)
        
        httpOnly = True
        _samesite = "strict"
        security = False
        path = '/'
        domain="127.0.0.1"
        #domain=".the-pirate-cove572851084171.co.uk"
        
        
        response.set_cookie(name, value, max_age=lifetime, expires=expires, samesite=_samesite, domain=domain, secure=security)#, path, domain, security, httpOnly)
        return response