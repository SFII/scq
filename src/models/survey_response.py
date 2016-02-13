from models.basemodel import BaseModel
from models.course import Course
from models.user import User
from models.question import Question
import random


class SurveyResponse(BaseModel):

    def requiredFields(self):
        return ['question_responses', 'responder_id', 'survey_id', 'response_time']

    def strictSchema(self):
        return True

    def fields(self):
        return {
            'question_responses': (self.is_list, self.is_not_empty, self.schema_list_check(self.is_string),),
            'survey_id': (self.is_string, self.is_not_empty, self.exists_in_table('Survey'),),
            'responder_id': (self.is_string, self.is_not_empty, self.exists_in_table('User'),),
            'response_time': (self.is_timestamp, ),
        }

    def default(self):
        return {
            'question_responses': [],
            'responder_id': "",
            'survey_id': "",
            'response_time': 0
        }
