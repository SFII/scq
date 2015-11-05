from models.basemodel import BaseModel

class Instructor(BaseModel):

    def requiredFields():
        return ['instructor_name', 'department', 'college', 'section']

    def fields():
        b = super(User, self)
        return {
            'instructor_id' : (b.is_int, ),
            'instructor_name' : (b.is_str, ),
            'department' : (b.is_str, ),
            'college' : (b.is_str, ),
            'section' : (b.is_str, )
        }
