from flask import Flask, render_template, request, make_response, jsonify, redirect, abort
import sys, json, datetime

RUNTIME = "LOCAL"
WEB_ADDRESS = "http://127.0.0.1:5432"
WEB_PORT = "5432"
API_ADDRESS = "http://127.0.0.1:5000"
API_PORT = "5000"

sys.path.append("lib/")
from Cookie_manager import Cookie_struct, Token_generator
from pbkdf2 import pbkdf2, HMAC
from response_headers import Headers


if RUNTIME == "LOCAL": 
    from db_local import DB_Manager
    data = open('config/HEADERS_local.conf', 'r')
    
elif RUNTIME == "PRODUCTION":
    from db_production import DB_Manager
    data = open('config/HEADERS_production.conf', 'r')

header_struct = json.load(data)
data.close()
cookies = Cookie_struct(True, 2)

app = Flask(__name__)
app.after_request(Headers.addResponseHeaders)






##############~~~~~ WEB SERVER PAGES ~~~~~##############

@app.route("/", methods=['POST', 'GET']) 
def hello(): 
    return "Hello World! This is the API."#render_template("index.html")
 
 
 
 

@app.route("/account/createUser", methods=['POST'])
def createUser():
    print(request.form)
    
    UUID = Token_generator.new_crypto_bytes(16).hex()
    username = request.form.get("usernameInput")
    password = request.form.get("passwordInput")
    email = request.form.get("emailInput")
    forename = request.form.get("forenameInput")
    surname = request.form.get("surnameInput")
    DOB = request.form.get("dobInput")
    ip = request.environ['REMOTE_ADDR']
    print(username, password, email)
    salt = Token_generator.new_crypto_bytes(20)
    salted_pwd = pbkdf2(password, salt).digest()
    
    DB_Manager.execute('''INSERT INTO Users VALUES ('%s', '%s', '%s', '%s', '%s', '%s')''' %
        (UUID, username, email, forename, surname, DOB), "ALTER")
    DB_Manager.changePassword(username, salted_pwd, salt.hex())
        
        
        
    #then login the user
    userCookie = cookies.createCookie(username, ip).hex()
    response = make_response(redirect(WEB_ADDRESS))
    c_response = Headers.addCookie(response, 'USR_ID', userCookie)
    h_response = Headers.addResponseHeaders(c_response)
    
    return h_response
    
    
    
   

@app.route('/account/sign-in', methods=['POST'])
def login():
    username = request.form.get("usernameInput")
    password = request.form.get("passwordInput")
    
    print(username, password)
    
    u_UUID = DB_Manager.execute('''SELECT Users.UUID FROM Users WHERE (username = '%s');''' % (username), "AUTH")[0][0]
    u_salt = DB_Manager.execute('''SELECT salt FROM User_Auth WHERE (UUID = '%s');''' % (u_UUID), "AUTH")[0][0]
    print("Fetched salt: ", u_salt)
    u_salt = bytearray.fromhex(u_salt)
    
    print("bytes salt: ", u_salt)
    
    e_password = pbkdf2(password, u_salt).digest()
    
    
    ip = request.environ['REMOTE_ADDR']
    
    if DB_Manager.authenticateUser(username, e_password) == True:
        userCookie = cookies.createCookie(username, ip).hex()
        response = make_response(redirect(WEB_ADDRESS))
        c_response = Headers.addCookie(response, 'USR_ID', userCookie)
        return c_response
    else:
        return abort(404)
    #first validate user and password
    
    
    
    
    
@app.route('/account/sign-out')
def logout():
    usr_cookie = request.cookies.get("USR_ID")
    ip = request.environ['REMOTE_ADDR']
    success = cookies.deleteCookie(usr_cookie, ip)
    if success == True:
        blankCookie = cookies.createBlankCookie().hex()
        response = make_response(redirect(WEB_ADDRESS))
        c_response = Headers.addCookie(response)
        return c_response
        
    else:
        return abort(404)




# @app.route('/account/changePassword')
# @app.route('/account/deleteAccount')



@app.route('/post/getPosts')
def getPosts():
    posts = DB_Manager.execute('''SELECT * FROM Posts''', "LOW")
    
    posts_dict = {}
    for p in posts:
        dic_rec = {
            "UUID": p[0],
            "heading": p[1],
            "body": p[2],
            "Date": p[3],
            "Time": p[4],
            "User_UUID": [5]
        }
        posts_dict[p[0]] = dic_rec
        
    return posts_dict
    
    
@app.route('/post/comment/getComments/')
def getComments():
    comments = DB_Manager.execute('''SELECT * FROM Comments''', "LOW")
    username = "fafa"#####################
    
    comments_dict = {}
    for c in comments:
        dict_rec = {
            "UUID": p[0],
            "body": p[1],
            "date_posted": p[2],
            "time_posted": p[3],
            "username": username,
            "user_UUID": p[4],
            "post_UUID": p[5]         
        }
        comments_dict[p[0]] = dict_rec
    return comments_dict
    
    
    
@app.route('/post/createPost', methods=['POST'])
def createPost():
    usr_cookie = request.cookies.get("USR_ID")
    ip = request.environ['REMOTE_ADDR']
    
    user = cookies.getUser(usr_cookie, ip)
    if user == None:
        return abort(404)
    else:
        heading = request.form.get("headingInput")
        body = request.form.get("postInput")
        date = datetime.datetime.now().date()
        time = datetime.datetime.now().time()
        
        
        DB_Manager.execute(
#ALTER



# @app.route('/post/deletePost')

# @app.route('/post/comment/createComment')
# @app.route('/post/comment/deleteComment')

    
    
if __name__ == "__main__":
    app.run(debug=True, port=API_PORT)
