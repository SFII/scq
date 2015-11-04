from models.basemodel import BaseModel

class Instructor(BaseModel):

    def requiredFields():
        return ['instructor_name', 'department', 'college', 'section']

    def fields():
        b = super(User, self)
        return {
            'instructor_id' : (is_int, ),
            'instructor_name' : (is_str, ),
            'department' : (is_str, ),
            'college' : (is_str, ),
            'section' : (is_str, )
        }
