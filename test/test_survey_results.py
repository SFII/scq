import unittest
import tornado.web
import tornado.testing
from tornado.httputil import HTTPHeaders
from test.test_runner import BaseAsyncTest
import time
import rethinkdb as r
import logging
import random
import services.lorem_ipsum as lorem_ipsum
from models.basemodel import BaseModel
from models.user import User
from models.group import Group
from models.survey import Survey
from models.survey_response import SurveyResponse
from models.question_response import QuestionResponse
from models.question import Question
from unittest import mock
from handlers.base_handler import BaseHandler


class TestSurveyResults(BaseAsyncTest):
    survey_response_ids = []
    question_response_ids = []
    survey_id = ""
    survey_data = {}
    user_id = ""
    user_data = {}
    group_id = ""
    question_data = []
    question_ids = []
    q1 = {
        'id': 'q1',
        'title': 'free response',
        "response_format": Question().RESPONSE_FREE,
        "options": []
    }
    q2 = {
        'id': 'q2',
        'title': 'multiple choice',
        "response_format": Question().RESPONSE_MULTIPLE_CHOICE,
        "options": ["alpha", "beta", "gamma", "delta"]
    }
    q3 = {
        'id': 'q3',
        'title': 'true or false',
        "response_format": Question().RESPONSE_TRUE_OR_FALSE,
        "options": [True, False]
    }
    q4 = {
        'id': 'q4',
        'title': 'rating',
        "response_format": Question().RESPONSE_RATING,
        "options": []
    }
    questions = [q1, q2, q3, q4]
    survey_data = {}

    def setUpClass():
        logging.disable(logging.CRITICAL)
        user_ids = [User().create_generic_item() for i in range(10)]
        TestSurveyResults.user_ids = user_ids
        TestSurveyResults.user_data = User().get_item(TestSurveyResults.user_id)
        TestSurveyResults.generic_group_id = Group().create_generic_item()
        TestSurveyResults.survey_data = {
            'id': 'test_survey',
            'item_type': 'Group',
            'item_id': TestSurveyResults.generic_group_id,
            'item_name': 'Generic Group',
            'creator_id': 'meta',
            'creator_name': 'meta',
            'responses': [],
            'created_timestamp': time.time(),
            'closed_timestamp': None,
            'deleted': False
        }
        return

    def test_survey_responses(self):
        self.respond_to_surveys()
        pass

    def respond_to_surveys(self):
        survey_response_ids = []
        question_response_ids = []

        def _respond_to_questions():
            d1 = d2 = d3 = d4 = {}
            d1['question_id'] = 'q1'
            d2['question_id'] = 'q2'
            d3['question_id'] = 'q3'
            d4['question_id'] = 'q4'
            d1['response_format'] = Question().RESPONSE_FREE
            d2['response_format'] = Question().RESPONSE_MULTIPLE_CHOICE
            d3['response_format'] = Question().RESPONSE_TRUE_OR_FALSE
            d4['response_format'] = Question().RESPONSE_RATING
            d1['question_id'] = lorem_ipsum.lorem_ipsum()
            d2['question_id'] = random.choice(["alpha", "beta", "gamma", "delta"])
            d3['question_id'] = random.choice([True, False])
            d4['question_id'] = random.randint(0, 10)
            r1 = QuestionResponse().create_item(d1)
            r2 = QuestionResponse().create_item(d2)
            r3 = QuestionResponse().create_item(d3)
            r4 = QuestionResponse().create_item(d4)
            return [r1, r2, r3, r4]

        for responder_id in self.user_ids:
            question_responses = _respond_to_questions()
            question_response_ids.append(question_responses)
            response_data = {
                'question_responses': question_responses,
                'responder_id': responder_id,
                'survey_id': 'test_survey',
                'response_time': time.time()
            }
            survey_response_id = SurveyResponse().create_item(response_data)
            survey_response_ids.append(survey_response_id)
        self.survey_response_ids = survey_response_ids
        self.question_response_ids = question_response_ids
        return

    def tearDownClass():
        logging.disable(logging.NOTSET)
        # Drop the database
        Question().delete_item('q1')
        Question().delete_item('q2')
        Question().delete_item('q3')
        Question().delete_item('q4')
        Survey().delete_item('test_survey')
        for survey_response in TestSurveyResults.survey_response_ids:
            SurveyResponse.delete_item(survey_response)
        for question_response in TestSurveyResults.question_response_ids:
            QuestionResponse.delete_item(question_response)
