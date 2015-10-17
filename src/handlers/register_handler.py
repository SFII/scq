import tornado.web
import services.ldapauth
from models.user import User

class RegisterHandler(tornado.web.RequestHandler):

    # Mandatories: Name, Universty email, password, confirm password, group (student...), accept term and conditions
    # Not mandatories: date, birthday, phone number, location, gender, ethnicity, native language

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

    def get(self, input):
        if input is None:
            return self.render("register.html", errormessage='', next=self.get_argument("next","/"))
        if input is 'ldap':
            return self.render("ldapregister.html", errormessage='', next=self.get_argument("next","/"))
        self.redirect(self.get_argument("next", "/register"))

    def post(self, input):
        if input is None:
            return __registerDefault(self)
        if input is 'ldap':
            return __registerLdap(self)
        self.redirect(self.get_argument("next", "/register"))


    def __getErrors(self):
        errors = []
        username = self.get_argument('username',strip = True)
        password = self.get_argument('password',strip = True)
        confirmpassword = self.get_argument('password',strip = True)
        accepted = self.get_argument('accepted',strip = True)
        if password != confirmpassword:
            errors.append('passwords do not match')
        if not accepted:
            errors.append('you must accept the Terms and Conditions to Register')
        return errors


    def __registerDefault(self):
        username = self.get_argument('username',strip = True)
        password = self.get_argument('password',strip = True)
        errors = __getErrors(self)
        if errors.count != 0:
            return self.render(
                'register.html',
                errors=errors,
                next=self.get_argument("next","/")
            )



    def __registerLdap(self):
        username = self.get_argument('username',strip = True)
        password = self.get_argument('password',strip = True)
        errors = __getErrors(self)
        if errors.count != 0:
            return self.render(
                'registerldap.html',
                errors=errors,
                next=self.get_argument("next","/")
            )
        authorized = ldapauth.auth_user_ldap(username, password)
        if authorized:
            user = self.__getUser(username)
            if user is None:
                self.__registerForm()
            else:
                self.__login(user)
        else:
            self.__failToAuthenticate()
            self.__loginForm()
        return


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
        self.set_secure_cookie("username", self.get_argument("username"))
        self.redirect(self.get_argument("next", "/"))

    def __getUser(self, username):
        user = User.get(uid=username)
