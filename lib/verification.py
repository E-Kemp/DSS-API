import smtplib


class emailVerification():
    @staticmethod
    def sendVerificationEmail(email, forename, URLtoken):
        subject = '''Verify account on ThePirateCove'''
        body = ('''
Dear %s,
Please follow the following link to verify your account at ThePirateCove.
Verification link: http://127.0.0.1:5000/account/verifyUser?id=%s
Kind Regards,
ThePirateCove Team.
            ''' % (forename, URLtoken))


    
        email_content = ('Subject: %s\n\n%s' % (subject, body))
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login("pcove7135645772@gmail.com", "topsecret123$")
        server.sendmail("sf2testmail@gmail.com", email, email_content)
        server.quit()        


# data = {"secret": "6LezdXwUAAAAAJ0ZrdD7w5JNHG-WLQE2N6Wo86aU", "response": code, "remoteip": ip}
        # req = urllib.request.Request(url="https://www.google.com/recaptcha/api/siteverify",
                                     # data=urllib.parse.urlencode(data).encode("utf-8"),
                                     # headers={"Content-type": "application/x-www-form-urlencoded"})
        # response = urllib.request.urlopen(req)
        # the_page = response.read().decode("utf-8")
        # the_page = the_page.replace("'", "\"")
        # the_page = json.loads(the_page)
        
        # #smtplib