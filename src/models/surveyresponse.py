from models.basemodel import BaseModel

class SurveyReponse(BaseModel):
    def requiredFields():
        super + ['user_id', 'survey_id', 'answer_id']

    def fields():
        super.update({
            'user_id' : (is_int, ),
            'survey_id' : (is_int, ),
            'answer_id' : (is_int, )
        })
