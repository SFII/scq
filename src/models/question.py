from basemodel import BaseModel

class Question(BaseModel):

    USER_RESPONSE_FORMAT = ['Free reponse', 'Mutiple choice', 'Dichotomous', 'Rank order scaling', 'Rating scale'] 

    def requiredFields():
        super + ['question_id', 'text', 'reponse_format']

    def fields():
        super.update({
            'question_id' : (is_int, ),
            'text' : (is_str, ),
            'response_format' : (is_str, is_reponse_format(USER_RESPONSE_FORMAT))
        })

   def is_reponse_format(data):
       is_in_list(USER_RESPONSE_FORMAT, data) 
