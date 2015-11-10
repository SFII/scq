from models.basemodel import BaseModel

class SurveyReponse(BaseModel):
    def requiredFields():
        return ['user_id', 'survey_id', 'answer_id']

    def fields():
        b = super(User, self)
        return {
            'user_id' : (b.is_int, ),
            'survey_id' : (b.is_int, ),
            'answer_id' : (b.is_int, )
        }
