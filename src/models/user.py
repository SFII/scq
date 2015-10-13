from remodel.models import Model
from remodel.helpers import create_tables, create_indexes

class User(Model):
    pass


# Creates all database tables defined by models
create_tables()
# Creates all table indexes based on model relations
create_indexes()

