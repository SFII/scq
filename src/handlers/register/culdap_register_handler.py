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

    def get(self):
        return self.render("register/culdapregister.html", errors=[], next=self.get_argument("next","/"))

    def post(self):
        confirming = self.get_argument('Confirming',False,strip = True)
        if confirming:
            return self.verifyRegisterCULdap()
        else:
            return self.CULdapRegister()


    def verifyCULdapRegister(self):
        username = self.get_argument('username',strip = True)
        errors = self.getVerificationErrors()
        if len(errors) != 0:
            return self.verifyCULdapRegistrationPage(username, errors)
        cookie_username = self.get_secure_cookie(COOKIE)
        if username != cookie_username:
            return self.failWithErrors('register/culdapregister.html')


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
        self.set_secure_cookie(self.COOKIE, value=username, max_age_days=1)
        info = self.ldapInfo(username)
        self.render('register/culdapregisterconfirm.html',
        errors=errors,
        next=self.get_argument("next","/"),
        user_genders=User().USER_GENDERS,
        user_ethnicities=User().USER_ETHNICITIES,
        user_native_languages=User().USER_NATIVE_LANGUAGES,
        email=info['email'],
        username=username,
        dob='',
        gender='',
        ethnicity='',
        native_language='',
        status=info['status'],
        major1=info['major1'],
        major2=info['major2'],
        major3=info['major3'],
        major4=info['major4'],
        minor1=info['minor1'],
        minor2=info['minor2'],
        )

    def confirmCULdap(self):
        print 'confirm'
        username = self.get_argument('username',strip = True)
        if username is None:
            return self.redirect('register/culdap')
        info = self.ldapInfo(username)

    def getConfirmationErrors(self):
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


    def ldapInfo(self, username):
        ldapinfo = culdapauth.user_info_ldap(username, self.LDAP_ATTRS)[0][1]
        info = {}
        info['name'] = ldapinfo[self.LDAP_NAME][0]
        info['mail'] = ldapinfo[self.LDAP_MAIL][0]
        info['status'] = ldapinfo[self.LDAP_STATUS][0]
        info['major1'] = ldapinfo[self.LDAP_MAJOR_1][0] if self.LDAP_MAJOR_1 in ldapinfo else None
        info['major2'] = ldapinfo[self.LDAP_MAJOR_2][0] if self.LDAP_MAJOR_2 in ldapinfo else None
        info['major3'] = ldapinfo[self.LDAP_MAJOR_3][0] if self.LDAP_MAJOR_3 in ldapinfo else None
        info['major4'] = ldapinfo[self.LDAP_MAJOR_4][0] if self.LDAP_MAJOR_4 in ldapinfo else None
        info['minor1'] = ldapinfo[self.LDAP_MINOR_1][0] if self.LDAP_MINOR_1 in ldapinfo else None
        info['minor2'] = ldapinfo[self.LDAP_MINOR_2][0] if self.LDAP_MINOR_2 in ldapinfo else None
        info


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
