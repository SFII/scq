from models.basemodel import BaseModel
from models.course import Course
from models.user import User
from models.question import Question
import time
import random
import logging


class Survey(BaseModel):

    def requiredFields(self):
        return ['questions', 'course_id', 'creator_id', 'course_name', 'creator_name', 'responses', 'closed_timestamp', 'created_timestamp']

    def strictSchema(self):
        return True

    def fields(self):
        return {
            'questions': (self.is_list, self.is_not_empty, self.schema_list_check(self.is_string),),
            'course_id': (self.is_string, self.is_not_empty, self.exists_in_table('Course')),
            'course_name': (self.is_string, self.is_not_empty,),
            'creator_id': (self.is_string, self.is_not_empty, self.exists_in_table('User'),),
            'creator_name': (self.is_string, self.is_not_empty,),
            'responses': (self.is_list, self.schema_list_check((self.is_string,)),),
            'created_timestamp': (self.is_timestamp, ),
            'closed_timestamp': (self.schema_or(self.is_timestamp, self.is_none), ),
        }

    def create_item(self, data):
        data['responses'] = []
        data['created_timestamp'] = time.time()
        if 'closed_timestamp' not in data.keys():
            data['closed_timestamp'] = None
        course_id = data['course_id']
        creator_id = data['creator_id']
        creator_data = User().get_item(creator_id)
        course_data = Course().get_item(course_id)
        if creator_data is None:
            logging.error('creator_id does not correspond to value in database')
            return None
        if course_data is None:
            logging.error('course_id does not correspond to value in database')
            return None
        data['course_name'] = course_data['course_name']
        data['creator_name'] = creator_data['username']
        survey_id = super(Survey, self).create_item(data)
        active_surveys = course_data['active_surveys']
        active_surveys.append(survey_id)
        subscribers = course_data['subscribers']
        Course().update_item(course_id, {'active_surveys': active_surveys}, skip_verify=True)
        self.send_user_survey(creator_id, survey_id, 'created_surveys')
        for subscriber_id in subscribers:
            self.send_user_survey(subscriber_id, survey_id)
        return survey_id

    # returns default survey data, that can be overwritten. Good for templating a new user
    def default(self):
        return {
            'questions': [],
            'course_id': "",
            'creator_id': "",
            'course_name': "",
            'creator_name': "",
            'responses': [],
            'closed_timestamp': None,
            'created_timestamp': time.time()
        }

    def create_generic_item(self, creator_id=None, course_id=None):
        data = self.default()
        data['course_id'] = course_id if course_id else Course().create_generic_item()
        data['creator_id'] = creator_id if creator_id else User().create_generic_item()
        for i in range(4):
            data['questions'].append(Question().create_generic_item())
        x = self.create_item(data)
        return x

    def decompose_from_id(self, survey_id):
        survey_data = self.get_item(survey_id)
        return self.decompose(survey_data)

    def decompose(self, survey_data):
        if survey_data is None:
            return None
        decomposed_data = survey_data.copy()
        decomposed_question_data = []
        question_ids = survey_data['questions']
        for question_id in question_ids:
            question_data = Question().get_item(question_id)
            decomposed_question_data.append(question_data)
        decomposed_data['questions'] = decomposed_question_data
        return decomposed_data
