from flask import Flask, render_template
app = Flask(__name__)


def addheaders(response):
    response.headers['Access-Control-Allow-Origin'] = '*'#'https://www.the-pirate-cove572851084171.co.uk'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains' #see https://www.thesslstore.com/blog/what-is-hypertext-strict-transport-security-hsts/
    response.headers['X-XSS-Protection'] = '1; mode=block' #see https://owasp.org/www-project-secure-headers/
    #include content security policy header when have time
    
    return response
app.after_request(addheaders)





@app.route("/") 
def hello(): 
    return render_template("index.html")
    
    
    
    
if __name__ == "__main__":
    app.run(debug=True)
