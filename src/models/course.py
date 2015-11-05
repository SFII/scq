from models.basemodel import BaseModel

class Course(BaseModel):

    def requiredFields():
        return ['course_name', 'department', 'average_grade', 'credit_hours']

    def fields():
        b = super(User, self)
        return {
            'course_id' : (b.is_int, ),
            'course_name' : (b.is_str, ),
            'department' : (b.is_str, ),
            'average_grade' : (b.is_int, ),
            'credit_hours' : (b.is_int, )
        }
