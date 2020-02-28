from flask import Flask, render_template, request, make_response
from Cookie_manager import Cookie_struct, Token_generator
from Database_Scripts import DB_Manager
from pbkdf2 import pbkdf2, HMAC

app = Flask(__name__)
cookies = Cookie_struct(True, 2)




def addheaders(response):
    response.headers['Access-Control-Allow-Origin'] = '*'#'https://www.the-pirate-cove572851084171.co.uk'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains' #see https://www.thesslstore.com/blog/what-is-hypertext-strict-transport-security-hsts/
    response.headers['X-XSS-Protection'] = '1; mode=block' #see https://owasp.org/www-project-secure-headers/
    #include content security policy header when have time
    
    return response
app.after_request(addheaders)



@app.route("/createUser", methods=['POST'])
def createUser():
    username = request.args.get("username")
    password = request.args.get("password")
    email = request.args.get("email")
    forename = request.args.get("forename")
    surname = request.args.get("surname")
    DOB = request.args.get("DOB")
    ip = request.environ['REMOTE_ADDR']
    
    salt = Token_generator.new_crypto_bytes(20)
    salted_pwd = pbkdf2(password, salt).digest()
    
    DB_Manager.execute('''INSERT INTO Users VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s')''' %
        (username, email, salted_pwd, str(salt.hex()), forename, surname, DOB))
        
    userCookie = cookies.createCookie(username, ip).hex()
    cookies._toString()
    
    response = make_response("Your generated cookie is: ", str(userCookie))
    #response = addheaders(response)
    response.set_cookie('USR_ID', userCookie)
    
    return response
    
    
    

@app.route("/") 
def hello(): 
    return render_template("index.html")
    

@app.route('/login', methods=['POST'])
def login():
    print("in login function")
    username = request.args.get("username")
    password = request.args.get("password")
    ip = request.environ['REMOTE_ADDR']
    
    #first validate user and password
    userCookie = cookies.createCookie(username, ip).hex()
    cookies._toString()
    
    response = make_response("Your generated cookie is: ", str(userCookie))
    #response = addheaders(response)
    response.set_cookie('USR_ID', userCookie)
    
    return response


    
    
if __name__ == "__main__":
    app.run(debug=True)
