import rethinkdb as r
import services.ldapauth
from basemodel import BaseModel

class Student(BaseModel):
    'college'
    'majors'
    'minors'
    'gpa'
    'course_history'
    'academic_years'
    'credits_earned'
    COLLEGE_ARTS_AND_SCIENCES = 'School of Arts and Sciences'
    COLLEGE_ENGINEERING = 'School of Engineering'
    COLLEGES = [COLLEGE_ARTS_AND_SCIENCES, COLLEGE_ENGINEERING]

    def is_major(data):
        pass

    def is_minor(data):
        pass

    # must be overridden
    def requiredFields():
        super + []

    # must be overrriden
    def fields():
        super.update({
            'college' : (is_in_list(REGISTRATION_METHODS), ),
            'majors' : (is_list, schema_list_check(is_major),),
            'minors' : (is_list, schema_list_check(is_minor),),
            'email' : (is_string, is_valid_email, )
        })
