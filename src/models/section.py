from remodel.models import Model
#from remodel.helpers import create_tables, create_indexes

class Section(Model):
    belongs_to = ('Course',)
    #has_one = ('Instructor',)
    
    def get_section_id(section):
        return str(section['section_id'])

    def get_course_id(section):
        return str(section['course_id'])

    def get_course_name(section):
        return str(section['course_name'])

    def get_department_name(section):
        return str(section['department_name'])

    def get_credit_hours(section):
        return str(section['credit_hours'])





# Creates all database tables defined by models
#create_tables()
# Creates all table indexes based on model relations
#create_indexes()

