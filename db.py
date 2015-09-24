from remodel.models import Model
from remodel.helpers import create_tables, create_indexes

class Course(Model):
    has_many = ('Section',)

class Section(Model):
    belongs_to = ('Course',)

create_tables()
create_indexes()
test_course = Course.create(name='MATH 1300')
test_course['sections'].add(Section(name='8AM - DOE'), Section(name='2PM - CHANG'))

def section_count():
    return str(test_course['sections'].count()) # prints 2

def course():
    return str(test_course["name"])
