from models.basemodel import BaseModel

class Answer(BaseModel):
    # Dichotomous: two possible responses (i.e. yes or no)
    # Rank order scaling: Among the choices given, rank them in order
    # Rating scale: ex --> very pleasant, somewhat pleasant, never pleasant nor unpleasant, somewhat unpleasent, very unpleasent
    USER_RESPONSE_FORMAT = ['Free reponse', 'Mutiple choice', 'Dichotomous', 'Rank order scaling', 'Rating scale']

    def requiredFields():
        return ['user_id', 'survey_id', 'question_id', 'response_format']

    def fields():
        b = super(Answer, self)
        return {
            'answer_id' : (b.is_string, ),
            'user_id' : (b.is_int, ),
            'survey_id' : (b.is_int, ),
            'question_id' : (b.is_int, ),
            'response_format' : (b.is_string, is_reponse_format,)
        }

    def is_reponse_format(data):
        is_in_list(USER_RESPONSE_FORMAT, data)
