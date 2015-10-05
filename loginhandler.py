import ldapauth
import models/user

class LoginHandler(tornado.web.RequestHandler):
    def get(self):
        loginForm()

    def post(self):
        identikey = self.get_argument('identikey')
        password = self.get_argument('password')
        authd = ldapauth.auth_user_ldap(identikey, password)
        if authd:
            attrs = ['cn','cuEduPersonPrimaryMajor1','cuEduPersonPrimaryMajor2','cuEduPersonSecondaryMajor1','cuEduPersonSecondaryMajor2','mail','cuEduPersonClass']
            results = ldapauth.user_info_ldap(identikey, attrs)
            writeout = "authd: {0}<br>".format(authd)
            writeout += "{0}".format(results)
            self.write(writeout)
        else:
            failToAuthenticate()
            loginForm()
        return

    def failToAuthenticate():
        self.write("<i>User and Password not recognized.</i>")

    def loginForm():
        self.write("""
                <form method="post" action="/myself">
                <b>Enter Your Identikey</b><br>
                <input type="text" name="identikey"><br>
                <b>Enter Your Password</b><br>
                <input type="password" name="password"></p>
                <input type="submit" value="Submit">
                </form>
            """)

    def getUser(identikey):
        user = User.get(uid=Identikey)


    def failToAuthenticate(identikey):
        self.write("user and password not recognized.".format(identikey))
