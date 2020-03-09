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



def logoutResponse(dict):
    blankCookie = cookies.createBlankCookie()
    response = make_response(jsonify(dict))
    c_response = Headers.addCookie(response, 'S_ID', blankCookie)
    c2_response = Headers.addCookie(response, 'USR_ID', blankCookie)
    return c2_response


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
        ret = {"code":"warning", "reason":"Captcha failed"}
        return jsonify(ret)
    
    print("Passed captcha veri")
    salt = Token_generator.new_crypto_bytes(20)
    salted_pwd = pbkdf2(password, salt).digest()
    
    x1 = DB_Manager.execute("ALTER", '''INSERT INTO Users VALUES ('%s', '%s', '%s', '%s', '%s', '%s')''', UUID, username, email, forename, surname, DOB)     
    x2 = DB_Manager.changePassword(username, salted_pwd, salt.hex(), verification_code)
    
    if x1==None or x2 == None: 
        ret = {"code":"warning", "reason":"There was an issue with your request"}
        return jsonify(ret)
    else: 
        Verification.sendVerificationEmail(email, forename, verification_code)
        ret = {"code":"success"}
        return jsonify(ret)
    ret = {"code":"warning", "reason":"There was an issue with your request"}
    return jsonify(ret)
    
    
    
@app.route("/account/verifyUser/")
def verifyUser():
    new_random_UUID = Token_generator.new_crypto_bytes(16).hex()
    verification_Code = request.args.get("id")
    x1 = DB_Manager.execute("ALTER", '''UPDATE User_Auth SET verified='TRUE', verification_code='%s' WHERE (verification_code='%s')''',  new_random_UUID, verification_Code)
    if x1 == None:
        ret = {"code":"warning", "reason":"Verification ID incorrect"}
    else:
        ret = {"code":"sucess"}
    return jsonify(ret)
          
   

@app.route('/account/sign-in', methods=['POST'])
def login():
    global cookies
    username = request.form.get("usernameInput")
    password = request.form.get("passwordInput")+P_VALUE
    
    u_UUID = DB_Manager.getUUID(username)
    if u_UUID == None:
        ret = {"code":"warning", "reason":"Username or Password incorrect."}
        return jsonify(ret)
    u_salt = DB_Manager.execute("AUTH", '''SELECT salt FROM User_Auth WHERE (UUID = '%s');''', u_UUID)
    if(len(u_salt) == 0): 
        ret = {"code":"warning", "reason":"Username or Password incorrect."}
        return jsonify(ret)
    else: u_salt = u_salt[0][0]
    
    u_salt = bytearray.fromhex(u_salt)   
    e_password = pbkdf2(password, u_salt).digest()
    ip = request.environ['REMOTE_ADDR']
    
    if DB_Manager.authenticateUser(username, e_password) == True:
        userCookie = cookies.createCookie(u_UUID, ip)
        ret = {"code":"success"}
        response = make_response(jsonify(ret))
        c_response = Headers.addCookie(response, 'S_ID', userCookie)
        c_response = Headers.addCookie(response, 'USR_ID', u_UUID)
        return c_response
    else:
        ret = {"code":"warning", "reason":"Username or Password incorrect."}
        return jsonify(ret)
    
    
@app.route('/account/sign-out', methods=['GET'])
def logout():
    usr_cookie = request.cookies.get("S_ID")
    ip = request.environ['REMOTE_ADDR']
    success = cookies.deleteCookie(usr_cookie, ip)
    
    
    if success == True:
        #blankCookie = cookies.createBlankCookie()
        #response = make_response(redirect(WEB_ADDRESS))
        #c_response = Headers.addCookie(response, 'S_ID', blankCookie)
        ret = {"code": "success"}
        
    else:
        ret = {"code": "warning", "reason": "Error within user session"}
    return jsonify(ret)


@app.route('/account/changePassword', methods=['POST'])
def changePassword():
    usr_cookie = request.cookies.get("S_ID")
    ip = request.environ['REMOTE_ADDR']
    user_UUID = cookies.getUUID(usr_cookie, ip)
    if user_UUID == None: 
        return logoutResponse({"code": "danger", "reason": "You have been automatically logged out. Please log in again."})

        
        
    else:
        old_password = request.form.get("old_p")+P_VALUE
        new_password = request.form.get("new_p")+P_VALUE
        
        username = DB_Manager.getUsername(user_UUID)
        
        u_salt = DB_Manager.execute("AUTH", '''SELECT salt FROM User_Auth WHERE (UUID = '%s');''', user_UUID)
        if(len(u_salt) == 0): ret = {"code":"warning", "reason":"Unknown error"}
        else: u_salt = u_salt[0][0]
        
        u_salt = bytearray.fromhex(u_salt)   
        e_password = pbkdf2(old_password, u_salt).digest()
        
        if DB_Manager.authenticateUser(username, e_password) == True:
            new_salt = Token_generator.new_crypto_bytes(20)
            salted_pwd = pbkdf2(new_password, new_salt).digest()
            veri_code = Token_generator.new_crypto_bytes(16).hex()
            x2 = DB_Manager.changePassword(username, salted_pwd, new_salt.hex(), veri_code)
            if x2 == None: ret = {"code":"warning", "reason":"Error with new password"} 
            else:
                ret = {"code":"success"}
        else:
            ret = {"code":"warning", "reason":"Old password incorrect."}
    return jsonify(ret)


@app.route('/account/deleteAccount', methods=['POST'])
def deleteAccount():
    usr_cookie = request.cookies.get("S_ID")
    ip = request.environ['REMOTE_ADDR']
    user_UUID = cookies.getUUID(usr_cookie, ip)
    if user_UUID == None: 
        return logoutResponse({"code": "danger", "reason": "You have been automatically logged out. Please log in again."})
        
    else:
        x1 = DB_Manager.execute("ALTER", '''DELETE FROM Comments WHERE (user_UUID='%s')''', user_UUID)
        x2 = DB_Manager.execute("ALTER", '''DELETE FROM Posts WHERE (user_UUID='%s')''', user_UUID)
        x3 = DB_Manager.execute("ALTER", '''DELETE FROM User_Auth WHERE (UUID='%s')''', user_UUID)
        x4 = DB_Manager.execute("ALTER", '''DELETE FROM Users WHERE (UUID='%s')''', user_UUID)
        if x1 == None or x2 == None or x3 == None or x4 == None:
            ret = {"code":"warning", "reason":"Unknown error deleting user."}
        else: 
            ret = {"code":"success"}
    return jsonify(ret)



@app.route('/post/getPosts', methods=['GET'])
def getPosts():
    posts = DB_Manager.execute("LOW", '''SELECT * FROM Posts''')
    posts_dict = {}
    
    if posts != None:
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
    return jsonify(posts_dict)
    
    
@app.route('/post/comment/getComments', methods=['GET'])
def getComments():
    post_UUID = request.args.get("post_id")
    #print("UUID requested: ", post_UUID)
    comments = DB_Manager.execute("LOW", '''SELECT * FROM Comments WHERE (post_UUID='%s')''', post_UUID)
    comments_dict = {}
    if comments != None: 
        for c in comments:
            username = DB_Manager.getUsername(c[4])
            dict_rec = {
                "UUID": c[0],
                "body": c[1],
                "date_posted": c[2],
                "time_posted": c[3],
                "username": username,
                "post_UUID": c[5],
                "user_UUID": c[4]
            }
            comments_dict[c[0]] = dict_rec
    
    return jsonify(comments_dict)
    
    
    
@app.route('/post/createPost', methods=['POST'])
def createPost():
    print("IN CREATE POST --------------------------------")
    print("REQUEST FORM ARGS: ", request.form)
    print("REQUEST COOKIES: ", request.cookies)
    #print("HEADERS FROM REQUEST: ", request.headers)
    usr_cookie = request.cookies.get("S_ID")
    
    ip = request.environ['REMOTE_ADDR']
    user_UUID = cookies.getUUID(usr_cookie, ip)
    if user_UUID == None: 
        print("NO USER")
        return logoutResponse({"code": "danger", "reason": "You have been automatically logged out. Please log in again."})
        
    else:
        heading = request.form.get("titleInput")
        body = request.form.get("postInput")
        date = datetime.datetime.now().strftime("%Y-%m-%d")
        time = datetime.datetime.now().strftime("%H:%M:%S")
        username = DB_Manager.getUsername(user_UUID)
        UUID = Token_generator.new_crypto_bytes(10).hex()
        print("INSERTING INTO DATABASE")
        #toExecute = (
        code = DB_Manager.execute("ALTER", '''INSERT INTO Posts VALUES ('%s', '%s', '%s', '%s', '%s', '%s');''', UUID, heading, body, date, time, user_UUID)
            
        print("response: ", code)
        if code == None:
            ret = {"code": "warning", "reason": "Oops! Something went wrong. Please try again."}
        else:
            ret = {
                "code":"success",
                "post": {
                    "UUID":UUID,
                    "heading":heading,
                    "body":body,
                    "date":date,
                    "time":time,
                    "username":username,
                    "user_UUID":user_UUID        
                }
            }
    return jsonify(ret)


@app.route("/post/comment/createComment", methods=['POST'])
def createComment():
    usr_cookie = request.cookies.get("S_ID")
    ip = request.environ['REMOTE_ADDR']
    user_UUID = cookies.getUUID(usr_cookie, ip)
    if user_UUID == None: 
        return logoutResponse({"code": "danger", "reason": "You have been automatically logged out. Please log in again."})
    else:
        body = request.form.get("comment_body")
        date = datetime.datetime.now().strftime("%Y-%m-%d")
        time = datetime.datetime.now().strftime("%H:%M:%S")
        UUID = Token_generator.new_crypto_bytes(10).hex()
        username = DB_Manager.getUsername(user_UUID)
        post_UUID = request.form.get("post_id")
        code = DB_Manager.execute("ALTER", '''INSERT INTO Comments VALUES ('%s', '%s', '%s', '%s', '%s', '%s');''', UUID, body, date, time, user_UUID, post_UUID)
            
        if code == None:
            ret = {"code": "warning", "reason": "Oops! Something went wrong. Please try again."}
        else:
            ret = {
                "code":"success",
                "comment":{
                    "UUID":UUID,
                    "body":body,
                    "date_posted":date,
                    "time_posted":time,
                    "username":username,
                    "user_UUID":user_UUID,
                    "post_UUID":post_UUID
                }
            }
    return jsonify(ret)
    
    
    
    
    
@app.route('/post/deletePost', methods=['POST'])
def deletePost():
    usr_cookie = request.cookies.get("S_ID")
    ip = request.environ['REMOTE_ADDR']
    user_UUID = cookies.getUUID(usr_cookie, ip)
    if user_UUID == None: 
        return logoutResponse({"code": "danger", "reason": "You have been automatically logged out. Please log in again."})
    else:
        UUID = request.form.get("post_UUID")
        post_to_delete = DB_Manager.execute("LOW", '''SELECT * FROM Posts WHERE (UUID='%s');''', UUID)
        if post_to_delete == None:
            ret = {"code":"warning", "reason": "Post does not exist."}
        elif len(post_to_delete) == 0:
            ret = {"code":"warning", "reason": "Post does not exist."}
        elif post_to_delete[0][5] != user_UUID:
            ret = {"code":"warning", "reason": "You do not own this post."}
        else:
            x1 = DB_Manager.execute("ALTER", '''DELETE FROM Comments WHERE (post_UUID='%s')''', UUID)
            x2 = DB_Manager.execute("ALTER", '''DELETE FROM Posts WHERE (UUID='%s')''', UUID)
            if x1 == None or x2 == None: ret = {"code":"warning", "reason":"There was an error deleting your post."}
            else: ret = {"code":"success"}
    return jsonify(ret)  




@app.route('/post/comment/deleteComment', methods=['POST'])
def deleteComment():
    usr_cookie = request.cookies.get("S_ID")
    ip = request.environ['REMOTE_ADDR']
    user_UUID = cookies.getUUID(usr_cookie, ip)
    if user_UUID == None: 
        return logoutResponse({"code": "danger", "reason": "You have been automatically logged out. Please log in again."})

    else:
        UUID = request.form.get("comment_UUID")
        comment_to_delete = DB_Manager.execute("LOW", '''SELECT * FROM Comments WHERE (UUID='%s');''', UUID)
        if comment_to_delete == None or len(comment_to_delete) == 0:
            ret = {"code":"warning", "reason": "Comment with this ID does not exist"}
        elif comment_to_delete[0][4] != user_UUID:
            ret = {"code":"warning", "reason": "You do not own this comment."}
        else:
            x1 = DB_Manager.execute("ALTER", '''DELETE FROM Comments WHERE (UUID='%s')''', UUID)
            if x1 == None: ret = {"code":"warning", "reason":"There was an error deleting your comment."}
            else: ret = {"code":"success"}
    return jsonify(ret)
        
        
        
@app.route('/post/search', methods=['GET'])
def searchPosts():
    search_term = request.args.get('search_term')
    posts = DB_Manager.execute("LOW", '''SELECT * FROM Posts WHERE (heading LIKE '%s')''', '%'+search_term+'%',)
    
    posts_dict = {}
    
    if posts != None:
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
    return jsonify(posts_dict)
        
    
if __name__ == "__main__":
    app.run(debug=True, port=API_PORT)
