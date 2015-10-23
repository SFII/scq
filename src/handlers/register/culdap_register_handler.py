import services.culdapauth as culdapauth
from handlers.register_handler import RegisterHandler
from models.user import User

class CuLdapRegisterHandler(RegisterHandler):

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

    COOKIE = 'registering'
    FIVE_MINUTES = 0.0035

    def get(self):
        return self.render("register/culdapregister.html", errors=[], next=self.get_argument("next","/"))

    def post(self):
        confirming = self.get_argument('confirming',False,strip = True)
        print confirming
        if confirming:
            return self.verifyCULdapRegistration()
        else:
            return self.CULdapRegister()


    def verifyCULdapRegistration(self):
        username = self.get_argument('username',strip = True)
        errors = self.getVerificationErrors()
        if len(errors) != 0:
            return self.verifyCULdapRegistrationPage(username, errors)
        cookie_username = self.get_secure_cookie(COOKIE, max_age_days=FIVE_MINUTES)
        if username != cookie_username:
            return self.failWithErrors('register/culdapregister.html', ['Time to complete registration expired (5 minutes)'])


    def CULdapRegister(self):
        username = self.get_argument('username',strip = True)
        password = self.get_argument('password',strip = True)
        errors = self.getErrors()
        if len(errors) != 0:
            return self.failWithErrors('register/culdapregister.html', errors)
        authorized = culdapauth.auth_user_ldap(username, password)
        if authorized:
            user = self.getLdapUser(username, User().REGISTRATION_CULDAP)

            if user is None:
                return self.verifyCULdapRegistrationPage(username)
            else:
                return self.failWithErrors('register/culdapregister.html', ['Registered user with those credentials already exists'])
        else:
            return self.failWithErrors('register/culdapregister.html', ['Failed to authenticate LDAP username and password'])
        return


    def verifyCULdapRegistrationPage(self, username, errors=[]):
        self.set_secure_cookie(self.COOKIE, value=username)
        info = self.ldapInfo(username)
        self.render('register/culdapregisterconfirm.html',
        errors=errors,
        next=self.get_argument("next","/"),
        user_genders=User().USER_GENDERS,
        user_ethnicities=User().USER_ETHNICITIES,
        user_native_languages=User().USER_NATIVE_LANGUAGES,
        email=info['email'],
        username=username,
        dob= self.get_argument('dob','',strip = True),
        gender= self.get_argument('gender','',strip = True),
        ethnicity= self.get_argument('ethnicity','',strip = True),
        native_language= self.get_argument('native_language','',strip = True),
        status= self.get_argument('status',info['status'],strip = True),
        major1= self.get_argument('major1',info['major1'],strip = True),
        major2= self.get_argument('major2',info['major2'],strip = True),
        major3= self.get_argument('major3',info['major3'],strip = True),
        major4= self.get_argument('major4',info['major4'],strip = True),
        minor1= self.get_argument('minor1',info['minor1'],strip = True),
        minor2= self.get_argument('minor2',info['minor2'],strip = True),
        )

    def verifyCULdapRegistration(self):
        print 'verifying'
        username = self.get_argument('username',None,strip = True)
        if username is None:
            return self.failWithErrors('register/culdapregister.html')
        errors = self.getConfirmationErrors()
        if len(errors) != 0:
            return self.verifyCULdapRegistrationPage(username, errors)



    def getConfirmationErrors(self):
        errors = []
        email = self.get_argument('email',None,strip = True)
        status = self.get_argument('status',None,strip = True)
        dob = self.get_argument('dob',None,strip = True)
        print dob
        gender = self.get_argument('gender',None,strip = True)
        print gender
        ethnicity = self.get_argument('ethnicity',None,strip = True)
        print ethnicity
        native_language = self.get_argument('native_language',None,strip = True)
        print native_language
        if email is None:
            errors.append('a .colorado.edu email address is required')
        if not email.endswith('@colorado.edu'):
            errors.append('email address must be a valid @colorado.edu email address')
        if dob is None:
            errors.append('a Date of Birth must be specified')
        if gender is None:
            errors.append("a Gender must be specified (you may 'Prefer not to Disclose')")
        if ethnicity is None:
            errors.append("a Ethnicity must be specified (you may 'Prefer not to Disclose')")
        if native_language is None:
            errors.append("a Native Language must be specified (you may 'Prefer not to Disclose')")
        return errors


    def ldapInfo(self, username):
        ldapinfo = culdapauth.user_info_ldap(username, self.LDAP_ATTRS)[0][1]
        info = {}
        info['name'] = ldapinfo[self.LDAP_NAME][0]
        info['email'] = ldapinfo[self.LDAP_MAIL][0]
        info['status'] = ldapinfo[self.LDAP_STATUS][0]
        info['major1'] = ldapinfo[self.LDAP_MAJOR_1][0] if self.LDAP_MAJOR_1 in ldapinfo else ''
        info['major2'] = ldapinfo[self.LDAP_MAJOR_2][0] if self.LDAP_MAJOR_2 in ldapinfo else ''
        info['major3'] = ldapinfo[self.LDAP_MAJOR_3][0] if self.LDAP_MAJOR_3 in ldapinfo else ''
        info['major4'] = ldapinfo[self.LDAP_MAJOR_4][0] if self.LDAP_MAJOR_4 in ldapinfo else ''
        info['minor1'] = ldapinfo[self.LDAP_MINOR_1][0] if self.LDAP_MINOR_1 in ldapinfo else ''
        info['minor2'] = ldapinfo[self.LDAP_MINOR_2][0] if self.LDAP_MINOR_2 in ldapinfo else ''
        print info
        return info


    # def confirmRegistration(self,page='register/culdapregisterconfirm.html',errors=['Something went wrong.'],username="",dob="",user_gender="",user_native_language="",user_ethnicity=""):
    #     return self.render(
    #         page,
    #         username=username,
    #         errors=errors,
    #         dob=""
    #         genders=User().USER_GENDERS,
    #         ethnicites=User().USER_ETHNICITIES,
    #         native_languages=User().USER_NATIVE_LANGUAGES,
    #         gender
    #         next=self.get_argument("next","/")
    #     )
