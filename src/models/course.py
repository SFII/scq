from remodel.models import Model
from remodel.helpers import create_tables, create_indexes

class Course(Model):
    has_many = ('Section',)

def course(course):
    return str(course['name'])


# Creates all database tables defined by models
create_tables()
# Creates all table indexes based on model relations
create_indexes()
