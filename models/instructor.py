from models.basemodel import BaseModel


class Instructor(BaseModel):

    def requiredFields(self):
        return ['instructor_first', 'instructor_last', 'department', 'college']

    def fields(self):
        return {
            'instructor_first': (self.is_string, self.is_not_empty, ),
            'instructor_last': (self.is_string, self.is_not_empty, ),
            'department': (self.is_string, ),
            'college': (self.is_string, ),
        }

    def default(self):
        return {
            'instructor_first': '',
            'instructor_last': '',
            'department': '',
            'college': ''
        }

    def create_generic_item(self):
        data = self.default()
        data['instructor_first'] = 'Mike'
        data['instructor_last'] = 'Rawtch'
        data['department'] = 'ENGR'
        data['college'] = 'AS'
        instructor_id = self.create_item(data)
        return instructor_id
