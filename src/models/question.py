from models.basemodel import BaseModel

class Question(BaseModel):

    USER_RESPONSE_FORMAT = ['Free reponse', 'Mutiple choice', 'Dichotomous', 'Rank order scaling', 'Rating scale']

    def requiredFields():
        return ['text', 'reponse_format']

    def fields():
        b = super(User, self)
        return {
            'question_id' : (is_int, ),
            'text' : (is_str, ),
            'response_format' : (is_str, is_reponse_format(USER_RESPONSE_FORMAT))
        }

    def is_reponse_format(data):
       is_in_list(USER_RESPONSE_FORMAT, data)
