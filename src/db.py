from remodel.models import Model
from remodel.helpers import create_tables, create_indexes
from models.course import Course
from models.section import Section
from models.user import User

create_tables()
create_indexes()
test_user = User.create(uid="alphasalad")
test_course = Course.create(name='MATH 1300')
test_course['sections'].add(Section(name='8AM - DOE'), Section(name='2PM - CHANG'))

def section_count():
    return str(test_course['sections'].count()) # prints 2

def course():
    return str(test_course["name"])
