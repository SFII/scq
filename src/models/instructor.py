from models.basemodel import BaseModel


class Instructor(BaseModel):

    def requiredFields(self):
        return ['instructor_first', 'instructor_last', 'department', 'college', 'section']

    def fields(self):
        return {
            'instructor_first': (self.is_string, self.is_not_empty, ),
            'instructor_last': (self.is_string, self.is_not_empty, ),
            'department': (self.is_string, ),
            'college': (self.is_string, ),
            'section': (self.is_string, )
        }

    def default(self):
        return {
            'instructor_first': "",
            'instructor_last': "",
            'department': "",
            'college': "",
            'section': ""
        }
