import smtplib, requests, json


class Verification():
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


    @staticmethod
    def verifyCaptchaCode(code, ip):
        VERIFY_URL = "https://www.google.com/recaptcha/api/siteverify"

        captchaDetails = {
            'secret': '6LdMQ98UAAAAADpBl5ENG7gAUfDQnphq8FZbp2Eh',
            'response': code,
            'remoteip':ip
            }

        try:
            ver_resp = requests.post(VERIFY_URL, data = captchaDetails).text
            ver_resp_json = json.loads(ver_resp)
            if ver_resp_json["success"] == True:
                return True
            else:
                return False
                
        except Exception as e:
            print("ERROR in verifyCaptchaCode: ", str(e))
            return False

