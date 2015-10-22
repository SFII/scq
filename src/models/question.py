from basemodel import BaseModel
from answer import Answer

class Question(BaseModel):

    def requiredFields():
        super + ['question_id', 'text', 'reponse_format']

    def fields():
        super.update({
            'question_id' : (is_int, ),
            'text' : (is_str, ),
            'response_format' : (is_str, Answer.is_response_format(Answer.USER_RESPONSE_FORMAT))
        })
