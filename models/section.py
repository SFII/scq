from models.basemodel import BaseModel


class Section(BaseModel):
    """
    A section is an individual instance of an offered course.
    """

    def requiredFields(self):
        return ['course_id', 'course_name', 'average_grade', 'credit_hours', 'section_time', 'instructor_id']

    def fields(self):
        b = super(Section, self)
        return {
            'course_id': (b.is_int, ),
            'course_name': (b.is_string, ),
            'average_grade': (b.is_int, ),
            'credit_hours': (b.is_int, ),
            'section_time': (b.is_timestamp, ),
            'instructor_id': (b.is_int, )
        }
