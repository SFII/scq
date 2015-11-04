from models.basemodel import BaseModel

class Course(BaseModel):

    def requiredFields():
        return ['course_name', 'department', 'average_grade', 'credit_hours']

    def fields():
        b = super(User, self)
        return {
            'course_id' : (is_int, ),
            'course_name' : (is_str, ),
            'department' : (is_str, ),
            'average_grade' : (is_int, ),
            'credit_hours' : (is_int, )
        }
