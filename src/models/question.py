from models.basemodel import BaseModel

class Question(BaseModel):

    USER_RESPONSE_FORMAT = ['Free reponse', 'Mutiple choice', 'Dichotomous', 'Rank order scaling', 'Rating scale']

    def requiredFields():
        return ['text', 'reponse_format']

    def fields():
        b = super(Question, self)
        return {
            'question_id' : (b.is_string, ),
            'text' : (b.is_str, b.is_not_empty, ),
            'response_format' : (b.is_str, b.is_reponse_format(USER_RESPONSE_FORMAT))
        }

    def is_reponse_format(data):
       super(User, self).is_in_list(USER_RESPONSE_FORMAT, data)
