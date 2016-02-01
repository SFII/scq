import services.culdapauth as culdapauth
import logging
import time
from tornado import gen
import tornado.web
from handlers.register_handler import RegisterHandler
from models.user import User
from models.basemodel import BaseModel
import rethinkdb as r

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
    LDAP_PRIMARY_AFFILIATION = 'eduPersonPrimaryAffiliation'
    LDAP_DEPARTMENTS = 'cuEduPersonHomeDepartment'
    LDAP_ATTRS = [LDAP_NAME,LDAP_MAJOR_1, LDAP_MAJOR_2, LDAP_MAJOR_3, LDAP_MAJOR_4, LDAP_MAIL,
        LDAP_MINOR_1, LDAP_MINOR_2, LDAP_STATUS, LDAP_PRIMARY_AFFILIATION, LDAP_DEPARTMENTS]

    COOKIE = 'registering'
    FIVE_MINUTES = 0.0035

    def get(self):
        return self.render("register/culdapregister.html", errors=[], next=self.get_argument("next","/"))


    def post(self):
        confirming = self.get_argument('confirming',False,strip = True)
        if confirming:
            return self.confirmCULdapRegistration()
        else:
            return self.CULdapRegister()


    def confirmCULdapRegistration(self):
        username = self.get_argument('username',strip = True)
        errors = self.getVerificationErrors()
        if len(errors) != 0:
            return self.verifyCULdapRegistrationPage(username, errors)
        cookie_username = self.get_secure_cookie(self.COOKIE, max_age_days=self.FIVE_MINUTES)
        if cookie_username is None:
            return self.failWithErrors('register/culdapregister.html', ['Time to complete registration expired (5 minutes)'])
        decoded_cookie_username = cookie_username.decode("utf-8")
        if username != decoded_cookie_username:
            logging.error('username %s did not match cookie username %s' % (username, decoded_cookie_username))
            return self.failWithErrors('register/culdapregister.html', ['Registration failed: cookie data is invalid'])
        data = self.collectUserData()
        data['username']        = username
        data['registration']    = User().REGISTRATION_CULDAP
        data['accepted_tos']    = True
        return self.registerUser(data)

    def collectUserData(self):
        data = User().default()
        data['email']           = self.get_argument('email',None,strip = True)
        data['dob']             = self.get_argument('dob',None,strip = True)
        data['gender']          = self.get_argument('gender',None,strip = True)
        data['ethnicity']       = self.get_argument('ethnicity',None,strip = True)
        data['native_language'] = self.get_argument('native_language',None,strip = True)
        data['status']          = self.get_argument('status',None,strip = True)
        data['major1']          = self.get_argument('major1',None,strip = True)
        data['major2']          = self.get_argument('major2',None,strip = True)
        data['major3']          = self.get_argument('major3',None,strip = True)
        data['major4']          = self.get_argument('major4',None,strip = True)
        data['minor1']          = self.get_argument('minor1',None,strip = True)
        data['minor2']          = self.get_argument('minor2',None,strip = True)
        data['departments']      = self.get_argument('departments', None,strip = True)
        data['departments'] = data['departments'].split(',')
        data['primary_affiliation'] = self.get_argument('primary_affiliation', None,strip = True)
        data['primary_affiliation'] = data['primary_affiliation'].split(',')
        return data


    def registerUser(self,data):
        username = self.get_argument('username',strip = True)
        verified = User().verify(data)
        if len(verified) != 0:
            logging.error('User: verification errors!')
            logging.error(verified)
            return self.verifyCULdapRegistrationPage(username, verified)
        user_id = User().create_item(data)
        user_data = User().get_item(user_id)
        self.set_current_user(user_data)
        return self.redirect(self.get_argument("next", "/dashboard"))

    def CULdapRegister(self):
        username = self.get_argument('username',strip = True)
        password = self.get_argument('password',strip = True)
        errors = self.getErrors()
        if len(errors) != 0:
            return self.failWithErrors('register/culdapregister.html', errors)
        authorized = culdapauth.auth_user_ldap(username, password)
        if authorized:
            simmilar_users = self.getLdapUser(username, User().REGISTRATION_CULDAP)
            if len(simmilar_users) == 0:
                return self.verifyCULdapRegistrationPage(username)
            else:
                return self.failWithErrors('register/culdapregister.html', ['Registered user with those credentials already exists'])
        else:
            return self.failWithErrors('register/culdapregister.html', ['Failed to authenticate LDAP username and password'])
        return


    def verifyCULdapRegistrationPage(self, username, errors=[]):
        self.set_secure_cookie(self.COOKIE, value=username, expires_days=self.FIVE_MINUTES)
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
        primary_affiliation=self.get_argument('primary_affiliation',info['primary_affiliation'],strip = True),
        departments = self.get_argument('departments', info['departments'], strip = True)
        )

    #
    def verifyCULdapRegistration(self):
        username = self.get_argument('username',None,strip = True)
        if username is None:
            return self.failWithErrors('register/culdapregister.html')
        errors = self.getVerificationErrors()
        if len(errors) != 0:
            return self.verifyCULdapRegistrationPage(username, errors)

    # returns an array of errors found with input data
    # no errors is indicated by an empty array
    def getVerificationErrors(self):
        errors = []
        email = self.get_argument('email',None,strip = True)
        status = self.get_argument('status',None,strip = True)
        dob = self.get_argument('dob',None,strip = True)
        gender = self.get_argument('gender',None,strip = True)
        ethnicity = self.get_argument('ethnicity',None,strip = True)
        native_language = self.get_argument('native_language',None,strip = True)
        if email is None:
            errors.append('a .colorado.edu email address is required')
        if not email.lower().endswith('@colorado.edu'):
            errors.append('email address must be a valid @colorado.edu email address')
        if dob is None:
            errors.append('a Date of Birth must be specified')
        if gender is None:
            errors.append("a Gender must be specified (you may choose 'Prefer not to Disclose')")
        if ethnicity is None:
            errors.append("a Ethnicity must be specified (you may choose 'Prefer not to Disclose')")
        if native_language is None:
            errors.append("a Native Language must be specified (you may choose 'Prefer not to Disclose')")
        return errors

    # queries the ldapserver for user info, returning a dictionary of information
    def ldapInfo(self, username):
        ldapinfo = culdapauth.user_info_ldap(username, self.LDAP_ATTRS)[0]['attributes']
        info = {}
        info['name'] = ldapinfo[self.LDAP_NAME][0]
        info['email'] = ldapinfo[self.LDAP_MAIL][0].lower()
        info['status'] = ldapinfo[self.LDAP_STATUS].capitalize()
        info['major1'] = ldapinfo[self.LDAP_MAJOR_1].capitalize() if self.LDAP_MAJOR_1 in ldapinfo else ''
        info['major2'] = ldapinfo[self.LDAP_MAJOR_2].capitalize() if self.LDAP_MAJOR_2 in ldapinfo else ''
        info['major3'] = ldapinfo[self.LDAP_MAJOR_3].capitalize() if self.LDAP_MAJOR_3 in ldapinfo else ''
        info['major4'] = ldapinfo[self.LDAP_MAJOR_4].capitalize() if self.LDAP_MAJOR_4 in ldapinfo else ''
        info['minor1'] = ldapinfo[self.LDAP_MINOR_1].capitalize() if self.LDAP_MINOR_1 in ldapinfo else ''
        info['minor2'] = ldapinfo[self.LDAP_MINOR_2].capitalize() if self.LDAP_MINOR_2 in ldapinfo else ''
        info['departments'] = ldapinfo[self.LDAP_DEPARTMENTS].capitalize() if self.LDAP_DEPARTMENTS in ldapinfo else ''
        info['primary_affiliation'] = ldapinfo[self.LDAP_PRIMARY_AFFILIATION].capitalize() if self.LDAP_PRIMARY_AFFILIATION in ldapinfo else ''
        return info
