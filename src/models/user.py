import rethinkdb as r
from basemodel import BaseModel

class User(BaseModel):
    REGISTRATION_LDAP = 'registration_ldap'
    REGISTRATION_METHODS = [REGISTRATION_LDAP]

    def required_fields():
        super + ['registration', 'username', 'email']

    def fields():
        super.update({
            "registration" : is_in_list(REGISTRATION_METHODS),
            "username" : (is_string, ),
            "email" : (is_string, )
        })

# Creates all database tables defined by models
#create_tables()
# Creates all table indexes based on model relations
#create_indexes()
