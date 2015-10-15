from remodel.models import Model
#from remodel.helpers import create_tables, create_indexes

class User(Model):
    has_one = ('Student', 'Instructor',)
    HASHEDPASSWORDKEY = 'hashedpassword_sha256'

    def validatePassword(password):
        hashedpassword = hashing.sha256(password)
        return self[HASHEDPASSWORDKEY] == hashedpassword

# Creates all database tables defined by models
#create_tables()
# Creates all table indexes based on model relations
#create_indexes()
