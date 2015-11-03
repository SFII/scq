import rethinkdb as r
import services.culdapauth
from models.basemodel import BaseModel

class User(BaseModel):
    REGISTRATION_CULDAP     = 'registration_culdap'
    REGISTRATION_METHODS    = [REGISTRATION_CULDAP]
    USER_GENDERS            = ['Male', 'Female', 'Other', 'Prefer Not to Disclose']
    USER_ETHNICITIES        = ['American Indian or Alaska Native', 'Asian', 'Black or African American', 'Hispanic or Latino', 'Native Hawaiian or Other Pacific Islander', 'White', 'Other', 'Prefer Not to Disclose']
    USER_NATIVE_LANGUAGES   = ['English', 'Spanish', 'French', 'German', 'Korean', 'Chinese', 'Japanese', 'Russian', 'Arabic', 'Portuguese', 'Hindi', 'Other', 'Prefer Not to Disclose']

    # must be overridden
    def requiredFields(self):
        r = ['registration',  'username', 'email', 'accepted_tos', 'date_registered']
        return r

    # must be overrriden
    def fields(self):
        b = super(User, self)
        f = {
            'registration' : (b.is_in_list(self.REGISTRATION_METHODS),),
            'user_id' : (b.is_int, ),
            'username' : (b.is_string, ),
            'email' : (b.is_string, b.is_valid_email, ),
            'accepted_tos' : (b.is_truthy,),
            'gender' : (b.is_in_list(self.USER_GENDERS),),
            'ethnicity' : (b.is_in_list(self.USER_ETHNICITIES),),
            'native_language' : (b.is_in_list(self.USER_NATIVE_LANGUAGES),),
            'date_registered' : (b.is_date_string,),
            'last_sign_in' : (b.is_date_string,)
        }
        return f

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
            REGISTRATION_CULDAP : culdapauth.auth_user_ldap
        }[registration](username, password)
