from remodel.models import Model
from remodel.helpers import create_tables, create_indexes

class Section(Model):
    belongs_to = ('Course',)

def section_count(section):
    return str(section['sections'].count())

# Creates all database tables defined by models
create_tables()
# Creates all table indexes based on model relations
create_indexes()

