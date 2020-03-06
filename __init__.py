from flask import Flask, render_template, request, make_response, jsonify, redirect, abort, send_from_directory
import sys, json, datetime

RUNTIME = "LOCAL"
WEB_ADDRESS = "http://127.0.0.1:5432"
WEB_PORT = "5432"
API_ADDRESS = "http://127.0.0.1:5000"
API_PORT = "5000"

sys.path.append("lib/")
from Session_structs import Cookie_struct, Token_generator
from pbkdf2 import pbkdf2, HMAC
from response_headers import Headers
from verification import Verification

if RUNTIME == "LOCAL": 
    from db_local import DB_Manager
    data = open('config/HEADERS_local.conf', 'r')
    
elif RUNTIME == "PRODUCTION":
    from db_production import DB_Manager
    data = open('config/HEADERS_production.conf', 'r')

header_struct = json.load(data)
data.close()
P_VALUE = json.load(open('config/crypt_vars.conf'))["P"]
cookies = Cookie_struct(True, 2)


app = Flask(__name__)
app.after_request(Headers.addResponseHeaders)






##############~~~~~ WEB SERVER PAGES ~~~~~##############

@app.route("/", methods=['POST', 'GET']) 
def hello(): 
    return "Hello World! This is the API."#render_template("index.html")
 
@app.route("/robots.txt", methods=['GET'])
def getRobots():
    return send_from_directory(app.static_folder, "robots.txt")
 
 

@app.route("/account/createUser", methods=['POST'])
def createUser():  
    global cookies
    #print("fields: ", request.form)
    UUID = Token_generator.new_crypto_bytes(16).hex()
    verification_code = Token_generator.new_crypto_bytes(16).hex()
    username = request.form.get("usernameInput")
    password = request.form.get("passwordInput")+P_VALUE
    email = request.form.get("emailInput")
    forename = request.form.get("forenameInput")
    surname = request.form.get("surnameInput")
    DOB = request.form.get("dobInput")
    ip = request.environ['REMOTE_ADDR']
    
    captcha_code = request.form.get("g-recaptcha-response")
    captcha_resp = Verification.verifyCaptchaCode(captcha_code, ip)
    if captcha_resp == False:
        ret = {"code":"fail", "reason":"Captcha failed"}
        return ret
    
    salt = Token_generator.new_crypto_bytes(20)
    salted_pwd = pbkdf2(password, salt).digest()
    
    x1 = DB_Manager.execute('''INSERT INTO Users VALUES ('%s', '%s', '%s', '%s', '%s', '%s')''' %
        (UUID, username, email, forename, surname, DOB), "ALTER")    
    x2 = DB_Manager.changePassword(username, salted_pwd, salt.hex(), verification_code)
    
    if x1==None or x2 == None: 
        ret = {"code":"fail", "reason":"There was an issue with your request"}
        return ret
    else: 
        Verification.sendVerificationEmail(email, forename, verification_code)
        ret = {"code":"success"}
        return ret
    ret = {"code":"fail", "reason":"There was an issue with your request"}
    return ret
    
    
    
@app.route("/account/verifyUser/")
def verifyUser():
    verification_Code = request.args.get("id")
    x1 = DB_Manager.execute('''UPDATE User_Auth SET verified=TRUE WHERE (verification_code='%s')''' %
        (verification_Code), "ALTER")
    if x1 == None:
        ret = {"code":"fail", "reason":"Verification ID incorrect"}
    else:
        ret = {"code":"sucess"}
    return ret
          
   

@app.route('/account/sign-in', methods=['POST'])
def login():
    global cookies
    username = request.form.get("usernameInput")
    password = request.form.get("passwordInput")+P_VALUE
    
    u_UUID = DB_Manager.getUUID(username)
    u_salt = DB_Manager.execute('''SELECT salt FROM User_Auth WHERE (UUID = '%s');''' % (u_UUID), "AUTH")
    if(len(u_salt) == 0): return abort(404)
    else: u_salt = u_salt[0][0]
    
    u_salt = bytearray.fromhex(u_salt)   
    e_password = pbkdf2(password, u_salt).digest()
    ip = request.environ['REMOTE_ADDR']
    
    if DB_Manager.authenticateUser(username, e_password) == True:
        cookies._toString()
        userCookie = cookies.createCookie(u_UUID, ip)
        response = make_response(redirect(WEB_ADDRESS))#redirect(WEB_ADDRESS))
        c_response = Headers.addCookie(response, 'S_ID', userCookie)
        c_response = Headers.addCookie(response, 'USR_ID', u_UUID)
        cookies._toString()
        return c_response
    else:
        return abort(404)
    
    
    
@app.route('/account/sign-out', methods=['GET'])
def logout():
    usr_cookie = request.cookies.get("S_ID")
    ip = request.environ['REMOTE_ADDR']
    success = cookies.deleteCookie(usr_cookie, ip)
    
    
    if success == True:
        blankCookie = cookies.createBlankCookie()
        response = make_response(redirect(WEB_ADDRESS))
        c_response = Headers.addCookie(response, 'S_ID', blankCookie)
        return c_response
    else:
        return abort(404)



@app.route('/account/changePassword', methods=['POST'])
def changePassword():
    usr_cookie = request.cookies.get("S_ID")
    ip = request.environ['REMOTE_ADDR']
    user_UUID = cookies.getUUID(usr_cookie, ip)
    if user_UUID == None: 
        ret = {"code": "fail", "reason": "You have been automatically logged out. Please log in again."}
        
    else:
        old_password = request.form.get("old_p")+P_VALUE
        new_password = request.form.get("new_p")+P_VALUE
        
        u_UUID = DB_Manager.getUUID(username)
        u_salt = DB_Manager.execute('''SELECT salt FROM User_Auth WHERE (UUID = '%s');''' % (u_UUID), "AUTH")
        if(len(u_salt) == 0): ret = {"code":"fail", "reason":"Unknown error"}
        else: u_salt = u_salt[0][0]
        
        u_salt = bytearray.fromhex(u_salt)   
        e_password = pbkdf2(password, u_salt).digest()
        
        if DB_Manager.authenticateUser(username, e_password) == True:
            new_salt = Token_generator.new_crypto_bytes(20)
            salted_pwd = pbkdf2(new_password, new_salt).digest()
            x2 = DB_Manager.changePassword(username, salted_pwd, salt.hex())
            if x2 == None: ret = {"code":"fail", "reason":"Error with new password"} 
            else:
                ret = {"code":"success"}
        else:
            ret = {"code":"fail", "reason":"Old password incorrect."}
    return ret


@app.route('/account/deleteAccount')
def deleteAccount():
    usr_cookie = request.cookies.get("S_ID")
    ip = request.environ['REMOTE_ADDR']
    user_UUID = cookies.getUUID(usr_cookie, ip)
    if user_UUID == None: 
        ret = {"code": "fail", "reason": "You have been automatically logged out. Please log in again."}
        
    else:
        x1 = DB_Manager.execute('''DELETE FROM Comments WHERE (user_UUID='%s')'''
            % (user_UUID), "ALTER")
        x2 = DB_Manager.execute('''DELETE FROM Posts WHERE (user_UUID='%s')'''
            % (user_UUID), "ALTER")
        x3 = DB_Manager.execute('''DELETE FROM User_Auth WHERE (UUID='%s')'''
            % (user_UUID), "ALTER")
        x4 = DB_Manager.execute('''DELETE FROM Users WHERE (UUID='%s')'''
            % (user_UUID), "AUTH")
        if x1 == None or x2 == None or x3 == None or x4 == None:
            ret = {"code":"fail", "reason":"Unknown error deleting user."}
        else: 
            ret = {"code":"success"}
    return ret



@app.route('/post/getPosts', methods=['GET'])
def getPosts():
    posts = DB_Manager.execute('''SELECT * FROM Posts''', "LOW")
    
    posts_dict = {}
    for p in posts:
        username = DB_Manager.getUsername(p[5])
        dic_rec = {
            "UUID": p[0],
            "heading": p[1],
            "body": p[2],
            "date_posted": p[3],
            "time_posted": p[4],
            "user_UUID": p[5],
            "username": username
        }
        posts_dict[p[0]] = dic_rec
    return posts_dict
    
    
@app.route('/post/comment/getComments/', methods=['GET'])
def getComments():
    post_UUID = request.args.get("post_id")
    comments = DB_Manager.execute('''SELECT * FROM Comments WHERE (UUID='%s')''' % (post_UUID), "LOW")
    
    comments_dict = {}
    for c in comments:
        username = DB_Manager.getUsername(c[4])
        dict_rec = {
            "UUID": c[0],
            "body": c[1],
            "date_posted": c[2],
            "time_posted": c[3],
            "username": username,
            "post_UUID": c[5]         
        }
        comments_dict[c[0]] = dict_rec
    return comments_dict
    
    
    
@app.route('/post/createPost', methods=['POST'])
def createPost():
    usr_cookie = request.cookies.get("S_ID")
    ip = request.environ['REMOTE_ADDR']
    user_UUID = cookies.getUUID(usr_cookie, ip)
    if user_UUID == None: 
        ret = {"code": "fail", "reason": "You have been automatically logged out. Please log in again."}
        
    else:
        heading = request.form.get("titleInput")
        body = request.form.get("postInput")
        date = datetime.datetime.now().strftime("%Y-%m-%d")
        time = datetime.datetime.now().strftime("%H:%M:%S")
        UUID = Token_generator.new_crypto_bytes(10).hex()
        toExecute = ('''INSERT INTO Posts VALUES ('%s', '%s', '%s', '%s', '%s', '%s');''' % (UUID, heading, body, date, time, user_UUID))

        code = DB_Manager.execute(toExecute, "ALTER")
            
        if code == None:
            ret = {"code": "fail", "reason": "Oops! Something went wrong. Please try again."}
        else:
            ret = {
                "code":"success",
                "post": {
                    "UUID":UUID,
                    "heading":heading,
                    "body":body,
                    "date":date,
                    "time":time,
                    "user_UUID":user_UUID        
                }
            }
    return ret


@app.route("/post/comment/createComment", methods=['POST'])
def createComment():
    usr_cookie = request.cookies.get("S_ID")
    ip = request.environ['REMOTE_ADDR']
    user_UUID = cookies.getUUID(usr_cookie, ip)
    if user_UUID == None: 
        ret = {"code": "fail", "reason": "You have been automatically logged out. Please log in again."}
    else:
        body = request.form.get("comment_body")
        date = datetime.datetime.now().strftime("%Y-%m-%d")
        time = datetime.datetime.now().strftime("%H:%M:%S")
        UUID = Token_generator.new_crypto_bytes(10).hex()
        post_UUID = request.form.get("post_id")
        code = DB_Manager.execute('''INSERT INTO Comments VALUES ('%s', '%s', '%s', '%s', '%s', '%s');'''
            % (UUID, body, date, time, user_UUID, post_UUID), "ALTER")
            
        if code == None:
            ret = {"code": "fail", "comment": {}}
        else:
            ret = {
                "code":"success",
                "comment":{
                    "UUID":UUID,
                    "body":body,
                    "date":date,
                    "time":time,
                    "user_UUID":user_UUID,
                    "post_UUID":post_UUID
                }
            }
    return ret
    
    
    
    
    
@app.route('/post/deletePost', methods=['POST'])
def deletePost():
    usr_cookie = request.cookies.get("S_ID")
    ip = request.environ['REMOTE_ADDR']
    user_UUID = cookies.getUUID(usr_cookie, ip)
    if user_UUID == None: 
        ret = {"code": "fail", "reason": "You have been automatically logged out. Please log in again."}

    else:
        UUID = request.form.get("post_UUID")
        post_to_delete = DB_Manager.execute('''SELECT * FROM Posts WHERE (UUID='%s');'''
            % (UUID), "LOW")
        
        if post_to_delete[5] != user_UUID:
            ret = {"code":"fail", "reason": "You do not own this post."}
        else:
            x1 = DB_Manager.execute('''DELETE FROM Comments WHERE (post_UUID='%s')'''
                % (UUID), "ALTER")
            x2 = DB_Manager.execute('''DELETE FROM Posts WHERE (UUID='%s')'''
                % (UUID), "ALTER")
            if x1 == None or x2 == None: ret = {"code":"fail", "reason":"There was an error deleting your post."}
            else: ret = {"code":"success"}
    return ret




@app.route('/post/comment/deleteComment', methods=['POST'])
def deleteComment():
    usr_cookie = request.cookies.get("S_ID")
    ip = request.environ['REMOTE_ADDR']
    user_UUID = cookies.getUUID(usr_cookie, ip)
    if user_UUID == None: 
        ret = {"code": "fail", "reason": "You have been automatically logged out. Please log in again."}

    else:
        UUID = request.form.get("comment_UUID")
        comment_to_delete = DB_Manager.execute('''SELECT * FROM Comments WHERE (UUID='%s');'''
            % (UUID), "LOW")
        if comment_to_delete[4] != user_UUID:
            ret = {"code":"fail", "reason": "You do not own this comment."}
        else:
            x1 = DB_Manager.execute('''DELETE FROM Comments WHERE (UUID='%s')'''
                % (UUID), "ALTER")
            if x1 == None: ret = {"code":"fail", "reason":"There was an error deleting your comment."}
            else: ret = {"code":"success"}
    return ret
        
        
        
            
        
    
if __name__ == "__main__":
    app.run(debug=True, port=API_PORT)
