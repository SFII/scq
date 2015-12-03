import rethinkdb as r
import logging
import services.culdapauth as culdapauth
from models.basemodel import BaseModel

class User(BaseModel):
    REGISTRATION_CULDAP     = 'registration_culdap'
    REGISTRATION_METHODS    = [REGISTRATION_CULDAP]
    USER_GENDERS            = ['Male', 'Female', 'Other', 'Prefer Not to Disclose']
    USER_ETHNICITIES        = ['American Indian or Alaska Native', 'Asian', 'Black or African American', 'Hispanic or Latino', 'Native Hawaiian or Other Pacific Islander', 'White', 'Other', 'Prefer Not to Disclose']
    USER_NATIVE_LANGUAGES   = ['English', 'Spanish', 'French', 'German', 'Korean', 'Chinese', 'Japanese', 'Russian', 'Arabic', 'Portuguese', 'Hindi', 'Other', 'Prefer Not to Disclose']

    # must be overridden
    def requiredFields(self):
        return ['registration',  'username', 'email', 'accepted_tos', 'date_registered']

    # must be overrriden
    def fields(self):
        b = super(User, self)
        return {
            'registration' : (b.is_in_list(self.REGISTRATION_METHODS),),
            'user_id' : (b.is_string, ),
            'username' : (b.is_string, b.is_unique),
            'email' : (b.is_string, b.is_valid_email, ),
            'accepted_tos' : (b.is_truthy,),
            'gender' : (b.is_in_list(self.USER_GENDERS),),
            'ethnicity' : (b.is_in_list(self.USER_ETHNICITIES),),
            'native_language' : (b.is_in_list(self.USER_NATIVE_LANGUAGES),),
            'date_registered' : (b.is_date_string,),
            'last_sign_in' : (b.is_date_string,),
            'courses' : (b.is_list,),
            'departments' : (b.is_list,),
            'unanswered_surveys' : (b.is_list,),
            'incomplete_surveys' : (b.is_list,),
            'answered_surveys' : (b.is_list,),
            'answers' : (b.is_list,),
        }

    # Given user_id and possible password, lookup how to authenticate the user
    # and attempt to authenticate the user
    # returns True / False whether the authentication is successful
    def authenticate(self, user_id, password):
        user = self.get_item(user_id)
        username = user['username']
        registration = user['registration']
        return {
            self.REGISTRATION_CULDAP : culdapauth.auth_user_ldap
        }[registration](username, password)
