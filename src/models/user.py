from remodel.models import Model
#from remodel.helpers import create_tables, create_indexes

class User(Model):
    REGISTRATION_LDAP = 'registration_ldap'
    REGISTRATION = [REGISTRATION_LDAP]
    # has_one = ('Student', 'Instructor',)
    HASHEDPASSWORDKEY = 'hashedpassword_sha256'

    def validatePassword(password):
        hashedpassword = hashing.sha256(password)
        return self[HASHEDPASSWORDKEY] == hashedpassword

    FIELDS = {
        "registration" :
        "id" : (is_int, ),
        "title" : (is_string, ),
        "parent" : (schema_or(is_none, is_user_node), ),
        "owner" : (is_user, ),
        "created_on" : (is_int, ),
        "base_node" : (schema_or(is_none, is_user_node), ),
        "children" : (is_list, schema_list_check(schema_recurse(user_node_child_fields))),
    }

# Creates all database tables defined by models
#create_tables()
# Creates all table indexes based on model relations
#create_indexes()
