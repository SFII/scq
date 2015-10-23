from basemodel import BaseModel

class Section(BaseModel):

    def requiredFields():
        super + ['section_id', 'course_id', 'course_name', 'average_grade', 'credit_hours', 'section_time', 'instructor_id']

    def fields():
        super.update({
            'section_id' : (is_int, ),
            'course_id' : (is_int, ),
            'course_name' : (is_str, ),
            'average_grade' : (is_int, ),
            'credit_hours' : (is_int, ),
            'section_time' : (is_date_string, ),
            'instructor_id' : (is_int, )
        })
