import tornado.web
import services.ldapauth as ldapauth
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

    def get(self, input=None):
        print input
        if input is None:
            return self.render("register.html", errors=[], next=self.get_argument("next","/"))
        if input == 'culdap':
            return self.render("culdapregister.html", errors=[], next=self.get_argument("next","/"))
        self.redirect(self.get_argument("next", "/register"))

    def post(self, input=None):
        print input
        if input is None:
            return self.__registerDefault()
        if input == 'culdap':
            return self.__registerCULdap()
        self.redirect(self.get_argument("next", "/register"))


    def __getErrors(self):
        errors = []
        username = self.get_argument('username',None,strip = True)
        password = self.get_argument('password',None,strip = True)
        confirmpassword = self.get_argument('passwordconfirm',None,strip = True)
        accepted = self.get_argument('accept',None,strip = True)
        if username is None:
            errors.append('username is required')
        if password is None:
            errors.append('password is required')
        if confirmpassword is None:
            errors.append('password confirmation is required')
        if password != confirmpassword:
            errors.append('passwords do not match')
        if not accepted:
            errors.append('you must accept the Terms and Conditions to Register')
        return errors


    def __registerDefault(self):
        errors = self.__getErrors()
        return self.render(
            'register.html',
            errors=errors,
            next=self.get_argument("next","/")
        )

    def __registerCULdap(self):
        print 'register ldap'
        username = self.get_argument('username',strip = True)
        password = self.get_argument('password',strip = True)
        errors = self.__getErrors()
        if len(errors) != 0:
            return self.__failWithErrors('culdapregister.html', errors)
        print 'no errors, validating user'
        authorized = ldapauth.auth_user_ldap(username, password)
        print User().REGISTRATION_CULDAP
        print authorized
        if authorized:
            user = self.__getCULdapUser(username)
            if user is None:
                # make new User Object in DB
                # get their LDAP Info
                self.__registerCULdap(username)
            else:
                return self.__failWithErrors('culdapregister.html', ['Registered user with those credentials already exists'])
        else:
            return self.__failWithErrors('culdapregister.html', ['Failed to authenticate LDAP username and password'])
        return

    def __failWithErrors(self,page='register.html',errors=['Something Went Wrong']):
        return self.render(
            page,
            errors=errors,
            next=self.get_argument("next","/")
        )


    def __registerCULDAP(self, username):
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

    def __getCULdapUser(self, username):
        user = User().get({'username' : username, 'registration' : User().REGISTRATION_CULDAP})
