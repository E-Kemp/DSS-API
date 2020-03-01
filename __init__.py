from flask import Flask, render_template, request, make_response, jsonify, redirect
import sys, json

sys.path.append("lib/")
from Cookie_manager import Cookie_struct, Token_generator
from Database_Scripts import DB_Manager
from pbkdf2 import pbkdf2, HMAC
from response_headers import Headers

app = Flask(__name__)
app.after_request(Headers.addResponseHeaders)

data = open('config/HEADERS_local.conf', 'r')
header_struct = json.load(data)
data.close()
cookies = Cookie_struct(True, 2)



@app.route("/") 
def hello(): 
    return "Hello World! This is the API."#render_template("index.html")
 
 
 
 

@app.route("/createUser", methods=['GET'])
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
    
    #response = {
    #    "creation-success":True,
    #    "USR_ID":userCookie
    #}
    
    #return jsonify(response)
    
    
    #response = make_response("Your generated cookie is: "+ str(userCookie))
    response = make_response(redirect("http://127.0.0.1:1234"))
    #response = Headers.addCookieHeaders(response)
    #print("Cookie: ", userCookie)
    c_response = Headers.addCookie(response, 'USR_ID', userCookie)
    
    return c_response
    
    
    
   

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
