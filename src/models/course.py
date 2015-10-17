from remodel.models import Model
#from remodel.helpers import create_tables, create_indexes

class Course(Model):
    has_many = ('Section',)

    def get_course_name(course):
        return str(course['name'])

    def get_department_name(course):
        return str(course['department'])

    def get_course_id(course):
        return str(course['course_id'])

    def get_credit_hours(course):
        return str(course['credit_hours'])

    def get_section_count(course):
        return str(course['sections'].count())





# Creates all database tables defined by models
#create_tables()
# Creates all table indexes based on model relations
#create_indexes()
