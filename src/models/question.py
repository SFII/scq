from models.basemodel import BaseModel
import random
import services.lorem_ipsum as lorem_ipsum
class Question(BaseModel):

    USER_RESPONSE_FORMAT = ['Free reponse', 'Mutiple choice', 'Dichotomous', 'Rank order scaling', 'Rating scale']

    def requiredFields(self):
        return ['text', 'reponse_format']

    def fields(self):
        b = super(__class__, self)
        return {
            'text' : (b.is_string, b.is_not_empty, ),
            'response_format' : (b.is_string, self.is_reponse_format(self.USER_RESPONSE_FORMAT))
        }

    def default(self):
        return {
            'text' : "",
            'response_format' : ""
        }

    def is_reponse_format(self, data):
       super(Question, self).is_in_list(self.USER_RESPONSE_FORMAT)

    def create_generic_item(self):
        data = self.default()
        data['text'] = lorem_ipsum.lorem_ipsum
        data['response_format'] = random.choice(self.USER_RESPONSE_FORMAT)
        super(Question, self).create_item(data)
