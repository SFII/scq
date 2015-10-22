import rethinkdb as r
import services.ldapauth
from basemodel import BaseModel

class User(BaseModel):
    REGISTRATION_CULDAP     = 'registration_culdap'
    REGISTRATION_METHODS    = [REGISTRATION_CULDAP]
    USER_GENDERS            = ['Male', 'Female']
    USER_ETHNICITIES        = ['American Indian or Alaska Native', 'Asian', 'Black or African American', 'Hispanic or Latino', 'Native Hawaiian or Other Pacific Islander', 'White', 'Other']
    USER_NATIVE_LANGUAGES   = ['English', 'Spanish', 'French', 'German', 'Korean', 'Chinese', 'Japanese', 'Russian', 'Arabic', 'Portuguese', 'Hindi']

    # must be overridden
    def requiredFields():
        super + ['registration', 'user_id',  'username', 'email', 'gender', 'accepted_tos']

    # must be overrriden
    def fields():
        super.update({
            'registration' : (is_in_list(REGISTRATION_METHODS),),
            'user_id' : (is_int, ),
            'username' : (is_string, ),
            'email' : (is_string, is_valid_email, ),
            'accepted_tos' : (is_truthy,),
            'gender' : (is_gender,),
            'ethnicity' : (is_ethnicity,),
            'native_language' : (is_native_language,),
            'date_registered' : (is_date_string,),
            'last_sign_in' : (is_date_string,)
        })

    def is_gender(data):
        is_in_list(USER_GENDERS, data)

    def is_ethnicity(data):
        is_in_list(USER_ETHNICITIES, data)

    def is_native_language(data):
        is_in_list(USER_NATIVE_LANGUAGES, data)

    def authenticate(self, username, password):
        user = self.get({'username' : username})
        registration = user['registration']
        {
            REGISTRATION_CULDAP : ldapauth.auth_user_ldap
        }[registration](username, password)
