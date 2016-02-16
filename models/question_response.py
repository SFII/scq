from models.basemodel import BaseModel
from models.course import Course
from models.user import User
from models.question import Question
import random


class QuestionResponse(BaseModel):

    def requiredFields(self):
        return ['response_data', 'question_id', 'response_format']

    def strictSchema(self):
        return True

    def fields(self):
        return {
            'response_format': (self.is_string, self.is_in_list(Question().USER_RESPONSE_FORMAT),),
            'question_id': (self.is_string, self.is_not_empty, self.exists_in_table('Question'),),
            'response_data': (self.is_not_none, )
        }

    def default(self):
        return {
            'response_format': "",
            'response_data': "",
            'question_id': None
        }
