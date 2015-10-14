from remodel.models import Model
#from remodel.helpers import create_tables, create_indexes

class User(Model):
    has_one = ('Student', 'Instructor',)


# Creates all database tables defined by models
#create_tables()
# Creates all table indexes based on model relations
#create_indexes()

