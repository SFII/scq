from models.basemodel import BaseModel

class Instructor(BaseModel):

    def requiredFields(self):
        return ['instructor_name', 'department', 'college', 'section']

    def fields(self):
        b = super(Instructor, self)
        return {
            'instructor_name' : (b.is_string, ),
            'department' : (b.is_string, ),
            'college' : (b.is_string, ),
            'section' : (b.is_string, )
        }
