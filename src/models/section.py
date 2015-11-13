from models.basemodel import BaseModel

class Section(BaseModel):

    def requiredFields():
        return ['course_id', 'course_name', 'average_grade', 'credit_hours', 'section_time', 'instructor_id']

    def fields():
        b = super(User, self)
        return {
            'section_id' : (b.is_int, ),
            'course_id' : (b.is_int, ),
            'course_name' : (b.is_str, ),
            'average_grade' : (b.is_int, ),
            'credit_hours' : (b.is_int, ),
            'section_time' : (b.is_date_string, ),
            'instructor_id' : (b.is_int, )
        }
