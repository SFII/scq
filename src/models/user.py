import rethinkdb as r
import services.ldapauth
from basemodel import BaseModel

class User(BaseModel):
    REGISTRATION_LDAP       = 'registration_ldap'
    REGISTRATION_METHODS    = [REGISTRATION_LDAP]
    USER_GENDERS            = ['Male', 'Female', 'Other', 'Prefer Not to Disclose']

    # must be overridden
    def requiredFields():
        super + ['registration', 'username', 'email']

    # must be overrriden
    def fields():
        super.update({
            'registration' : (is_in_list(REGISTRATION_METHODS),),
            'username' : (is_string, ),
            'email' : (is_string, is_valid_email, ),
            'gender' : (is_gender,),
            'date_registered' : (is_date_string,)
        })

    def is_gender(data):
        is_in_list(USER_GENDERS, data)

    def getUser(self, username):
        r.table(__name__).filter({'username': username})

    def authenticate(self, username, password):
        user = self.getUser(username)
        registration = user['registration']
        {
            REGISTRATION_LDAP : ldapauth.auth_user_ldap
        }[registration](username, password)


# Creates all database tables defined by models
#create_tables()
# Creates all table indexes based on model relations
#create_indexes()
