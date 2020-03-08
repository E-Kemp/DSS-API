import datetime, json

# Describes a collection of methods that add different headers server responses
# This includes HTTP headers, and Cookie headers
# See:
#   https://www.thesslstore.com/blog/what-is-hypertext-strict-transport-security-hsts/
#   https://owasp.org/www-project-secure-headers/
# @Author: Niklas Henderson, UEA

data = open('config/HEADERS_local.conf', 'r')
header_struct = json.load(data)
data.close()


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
		response.headers['Access-Control-Allow-Origin'] = header_struct["HTTPHeaders"]["Access-Control-Allow-Origin"]
		response.headers['Access-Control-Allow-Credentials'] = header_struct["HTTPHeaders"]["Access-Control-Allow-Credentials"]
		#print("Response Access-Control-Allow-Origin header: ", response.headers['Access-Control-Allow-Origin'])
		response.headers['X-Frame-Options'] = header_struct["HTTPHeaders"]["X-Frame-Options"]
		response.headers['Strict-Transport-Security'] = header_struct["HTTPHeaders"]["Strict-Transport-Security"]                    #'max-age=31536000; includeSubDomains' #see https://www.thesslstore.com/blog/what-is-hypertext-strict-transport-security-hsts/
		response.headers['X-XSS-Protection'] = header_struct["HTTPHeaders"]["X-XSS-Protection"]                      #see https://owasp.org/www-project-secure-headers/
		response.headers['Access-Control-Allow-Headers'] = header_struct["HTTPHeaders"]["Access-Control-Allow-Headers"]
		#include content security policy header when have time

		return response
        

	@staticmethod
	def addCookie(response, name, value):
		cookieSetString = ""
		cookieSetString += name+"="+value+";"
		
		
		if value == "":
			_expires = datetime.datetime.now() - datetime.timedelta(hours=2)
			_lifetime = 0
		else:
			_lifetime = header_struct["CookieHeaders"]["lifetime"]
			_expires = datetime.datetime.now() + datetime.timedelta(hours=2)



		_httpOnly = header_struct["CookieHeaders"]["httpOnly"]
		_samesite = header_struct["CookieHeaders"]["samesite"]
		_security = header_struct["CookieHeaders"]["secure"]
		_path = header_struct["CookieHeaders"]["path"]
		_domain = header_struct["CookieHeaders"]["domain"]

		#removed samesite=_samesite
		response.set_cookie(name, value, max_age=_lifetime, expires=_expires, samesite=_samesite, domain=_domain, secure=_security)#, path, domain, security, httpOnly)
		return response

			
