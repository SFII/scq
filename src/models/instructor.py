from basemodel import BaseModel

class Instructor(BaseModel):

    def requiredFields():
        super + ['instructor_id', 'instructor_name', 'department', 'college', 'section']

    def fields():
        super.update({
            'instructor_id' : (is_int, ),
            'instructor_name' : (is_str, ),
            'department' : (is_str, ),
            'college' : (is_str, ),
            'section' : (is_str, )
        })
