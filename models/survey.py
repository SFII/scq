from models.basemodel import BaseModel
from models.course import Course
from models.user import User
from models.instructor import Instructor
from models.question import Question
import time
import random
import logging


class Survey(BaseModel):
    ITEM_TYPES = ['Course', 'Instructor', 'User']

    def requiredFields(self):
        return ['questions', 'item_id', 'item_type', 'item_name', 'creator_id', 'creator_name', 'responses', 'closed_timestamp', 'created_timestamp', 'deleted']

    def strictSchema(self):
        return True

    def fields(self):
        return {
            'questions': (self.is_list, self.is_not_empty, self.schema_list_check(self.is_string),),
            'item_type': (self.is_string, self.is_in_list(self.ITEM_TYPES),),
            'item_id': (self.is_string, self.is_not_empty, ),
            'item_name': (self.is_string, self.is_not_empty,),
            'creator_id': (self.is_string, self.is_not_empty, self.exists_in_table('User'),),
            'creator_name': (self.is_string, self.is_not_empty,),
            'responses': (self.is_list, self.schema_list_check((self.is_string,)),),
            'created_timestamp': (self.is_timestamp, ),
            'closed_timestamp': (self.schema_or(self.is_timestamp, self.is_none), ),
            'deleted': (self.is_boolean,),
        }

    def create_item(self, data):
        data['responses'] = []
        data['created_timestamp'] = time.time()
        if 'closed_timestamp' not in data.keys():
            data['closed_timestamp'] = None
        item_id = data['item_id']
        creator_id = data['creator_id']
        creator_data = User().get_item(creator_id)
        course_data = Course().get_item(item_id)
        if creator_data is None:
            logging.error('creator_id does not correspond to value in database')
            return None
        if course_data is None:
            logging.error('item_id does not correspond to value in database')
            return None
        data['item_name'] = course_data['course_name']
        data['creator_name'] = creator_data['username']
        survey_id = super(Survey, self).create_item(data)
        active_surveys = course_data['active_surveys']
        active_surveys.append(survey_id)
        subscribers = course_data['subscribers']
        Course().update_item(item_id, {'active_surveys': active_surveys}, skip_verify=True)
        self.send_user_survey(creator_id, survey_id, 'created_surveys')
        for subscriber_id in subscribers:
            self.send_user_survey(subscriber_id, survey_id)
        return survey_id

    # returns default survey data, that can be overwritten. Good for templating a new user
    def default(self):
        return {
            'questions': [],
            'item_type': "",
            'item_id': "",
            'item_name': "",
            'creator_id': "",
            'creator_name': "",
            'responses': [],
            'closed_timestamp': None,
            'created_timestamp': time.time(),
            'deleted': False,
        }

    # TODO: implement Departments as an item_type
    def _model_from_item_type(self, item_type):
        return {
            'Instructor': Instructor(),
            'Course': Course(),
            'User': User()
        }[item_type]

    def create_generic_item(self, creator_id=None, item_id=None, item_type='Course'):
        data = self.default()
        model = self._model_from_item_type(item_type)
        data['item_type'] = item_type
        data['item_id'] = item_id if item_id else model.create_generic_item()
        data['creator_id'] = creator_id if creator_id else User().create_generic_item()
        for i in range(4):
            data['questions'].append(Question().create_generic_item())
        survey_id = self.create_item(data)
        return survey_id

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

    def mark_deleted(self, survey_id):
        survey = self.get_item(survey_id)
        survey['deleted'] = True
        Survey().update_item(survey_id, survey)
