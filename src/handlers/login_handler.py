import tornado.web
from services.hashing import Hashing
from models.user import User

class LoginHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("login.html", errormessage='', next=self.get_argument("next","/"))

    def post(self):
        username = self.get_argument('username',strip = True)
        password = self.get_argument('password',strip = True)
        user = User.get(uid=username)
        if user is None:
            self.render(
                'login.html',
                errormessage="User credentials are incorrect!",
                next=self.get_argument("next","/")
            )
        hashedpassword = password
        if user['passwordhash_sha256'] ==
        else:
            self.__set_current_user(user)
            self.redirect(self.get_argument("next", "/"))


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
