from models.basemodel import BaseModel

class Response(BaseModel):
    def requiredFields(self):
        return ['user_id', 'survey_id', 'answer_id']

    def fields(self):
        b = super(Response, self)
        return {
            'user_id' : (b.is_int, ),
            'survey_id' : (b.is_int, ),
            'answer_id' : (b.is_int, )
        }
