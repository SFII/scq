import tornado.web
import ldapauth
from models.user import User

class LoginHandler(tornado.web.RequestHandler):
    LDAP_NAME = 'cn'
    LDAP_MAIL = 'mail'
    LDAP_MAJOR_1 = 'cuEduPersonPrimaryMajor1'
    LDAP_MAJOR_2 = 'cuEduPersonPrimaryMajor2'
    LDAP_MAJOR_3 = 'cuEduPersonSecondaryMajor1'
    LDAP_MAJOR_4 = 'cuEduPersonSecondaryMajor2'
    LDAP_MINOR_1 = 'cuEduPersonPrimaryMinor'
    LDAP_MINOR_2 = 'cuEduPersonSecondaryMinor'
    LDAP_STATUS = 'cuEduPersonClass'
    LDAP_ATTRS = [LDAP_NAME,LDAP_MAJOR_1, LDAP_MAJOR_2, LDAP_MAJOR_3, LDAP_MAJOR_4, LDAP_MAIL, LDAP_MINOR_1, LDAP_MINOR_2, LDAP_STATUS]

    def __loginForm(self):
        self.write("""
                <form method="post" action="/login">
                <b>Enter Your Identikey</b><br>
                <input type="text" name="username"><br>
                <b>Enter Your Password</b><br>
                <input type="password" name="password"></p>
                <input type="submit" value="Submit">
                </form>
            """)

    def get(self):
        self.__loginForm()

    def post(self):
        username = self.get_argument('username',strip = True)
        password = self.get_argument('password',strip = True)
        authorized = ldapauth.auth_user_ldap(username, password)
        if authorized:
            user = self.__getUser(username)
            if user is None:
                self.set_secure_cookie('username', username)
                self.redirect("/register")
                self.__registerForm()
            else:
                self.__login(user)
        else:
            self.__failToAuthenticate()
            self.__loginForm()
        return

    def __failToAuthenticate(self):
        self.write("<i>User and Password not recognized.</i>")

    def __register(self, username):
        ldapinfo = ldapauth.user_info_ldap(username, LDAP_ATTRS)[0][1]
        name = ldapinfo[LDAP_NAME][0]
        mail = ldapinfo[LDAP_MAIL][0]
        status = ldapinfo[LDAP_STATUS][0]
        major1 = ldapinfo[LDAP_MAJOR_1][0] if LDAP_MAJOR_1 in ldapinfo else None
        major2 = ldapinfo[LDAP_MAJOR_2][0] if LDAP_MAJOR_2 in ldapinfo else None
        major3 = ldapinfo[LDAP_MAJOR_3][0] if LDAP_MAJOR_3 in ldapinfo else None
        major4 = ldapinfo[LDAP_MAJOR_4][0] if LDAP_MAJOR_4 in ldapinfo else None
        minor1 = ldapinfo[LDAP_MINOR_1][0] if LDAP_MINOR_1 in ldapinfo else None
        minor2 = ldapinfo[LDAP_MINOR_2][0] if LDAP_MINOR_2 in ldapinfo else None


    def __login(self, user):
        self.__set_current_user(user)
        self.set_secure_cookie("username", self.get_argument("username"))
        self.redirect("/")

    def __getUser(self, username):
        user = User.get(uid=username)

    def __set_current_user(self, user):
        if user:
            self.set_secure_cookie("user", tornado.escape.json_encode(user))
        else:
            self.clear_cookie("user")
