import rethinkdb as r
import logging
import time
import services.culdapauth as culdapauth
from models.basemodel import BaseModel

class User(BaseModel):
    REGISTRATION_CULDAP     = 'registration_culdap'
    REGISTRATION_METHODS    = [REGISTRATION_CULDAP]
    NO_DISCLOSURE           = 'Prefer Not to Disclose'
    USER_GENDERS            = ['Male', 'Female', 'Other', NO_DISCLOSURE]
    USER_ETHNICITIES        = ['American Indian or Alaska Native', 'Asian', 'Black or African American', 'Hispanic or Latino', 'Native Hawaiian or Other Pacific Islander', 'White', 'Other', NO_DISCLOSURE]
    USER_NATIVE_LANGUAGES   = ['English', 'Spanish', 'French', 'German', 'Korean', 'Chinese', 'Japanese', 'Russian', 'Arabic', 'Portuguese', 'Hindi', 'Other', NO_DISCLOSURE]
    #USER_AFFLIATION = ['Student', 'Faculty']

    # must be overridden
    def requiredFields(self):
        return ['registration',  'username', 'email', 'accepted_tos', 'date_registered']

    # must be overrriden
    def fields(self):
        b = super(User, self)
        return {
            'registration' : (b.is_in_list(self.REGISTRATION_METHODS),),
            'username' : (b.is_string,),
            'email' : (b.is_string, b.is_valid_email, ),
            'accepted_tos' : (b.is_truthy,),
            'gender' : (b.is_in_list(self.USER_GENDERS),),
            'ethnicity' : (b.is_in_list(self.USER_ETHNICITIES),),
            'native_language' : (b.is_in_list(self.USER_NATIVE_LANGUAGES),),
            'date_registered' : (b.is_date_string,),
            'last_sign_in' : (b.is_date_string,),
            'courses' : (b.is_list,),
            'departments' : (b.is_list,),
            'created_surveys' : (b.is_list,),
            'unanswered_surveys' : (b.is_list,),
            'answered_surveys' : (b.is_list,),
            'answers' : (b.is_list,),
            'primary_affiliation' : (b.is_list,),
        }

    # returns default user data, that can be overwritten. Good for templating a new user
    def default(self):
        return {
            'registration' : self.REGISTRATION_METHODS[0],
            'username' : '',
            'email' : '',
            'accepted_tos' : True,
            'gender' : self.USER_GENDERS[-1],
            'ethnicity' : self.USER_ETHNICITIES[-1],
            'native_language' : self.USER_NATIVE_LANGUAGES[-1],
            'date_registered' : time.strftime('%a %b %d %H:%M:%S %Z %Y'),
            'last_sign_in' : time.strftime('%a %b %d %H:%M:%S %Z %Y'),
            'courses' : [],
            'departments' : [],
            'unanswered_surveys' : [],
            'answered_surveys' : [],
            'created_surveys' : [],
            'answers' : [],
            'primary_affiliation' : [],
        }


    # Given user_id and possible password, lookup how to authenticate the user
    # and attempt to authenticate the user
    # returns True / False whether the authentication is successful
    def authenticate(self, user_id, password):
        print("{0} , {1}".format(user_id, password))
        user = self.get_item(user_id)
        username = user['username']
        registration = user['registration']
        return {
            self.REGISTRATION_CULDAP : culdapauth.auth_user_ldap
        }[registration](username, password)
