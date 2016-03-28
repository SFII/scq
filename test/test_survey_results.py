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
    responses_to_make = 5
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
        'title': 'free response',
        "response_format": Question().RESPONSE_FREE,
        "options": []
    }
    q2 = {
        'title': 'multiple choice',
        "response_format": Question().RESPONSE_MULTIPLE_CHOICE,
        "options": ["alpha", "beta", "gamma", "delta"]
    }
    q3 = {
        'title': 'true or false',
        "response_format": Question().RESPONSE_TRUE_OR_FALSE,
        "options": [True, False]
    }
    q4 = {
        'title': 'rating',
        "response_format": Question().RESPONSE_RATING,
        "options": []
    }
    questions = []
    survey_data = {}

    def setUpClass():
        logging.disable(logging.CRITICAL)
        user_ids = [User().create_generic_item() for i in range(TestSurveyResults.responses_to_make)]
        TestSurveyResults.user_ids = user_ids
        TestSurveyResults.user_data = User().get_item(TestSurveyResults.user_id)
        TestSurveyResults.generic_group_id = Group().create_generic_item()
        for question in [TestSurveyResults.q1, TestSurveyResults.q2, TestSurveyResults.q3, TestSurveyResults.q4]:
            question_id = Question().create_item(question)
            TestSurveyResults.questions.append(question_id)
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
            'deleted': False,
            'questions': TestSurveyResults.questions
        }
        Survey().create_item(TestSurveyResults.survey_data)
        return

    def test_survey_responses(self):
        self.respond_to_surveys()
        results = Survey().get_results('test_survey')
        formatted_results = Survey().get_formatted_results('test_survey')
        # logging.info(formatted_results)
        for question_response_id in self.question_response_ids:
            question_response = QuestionResponse().get_item(question_response_id)
            question_id = question_response['question_id']
            response_data = question_response['response_data']
            self.assertIn(response_data, results[question_id])
        for question_id, value in list(results.items()):
            for formatted_result_data in formatted_results:
                if formatted_result_data['id'] != question_id:
                    continue
                else:
                    self.assertEqual(len(value), len(formatted_result_data['results']))
                    self.assertEqual(sorted(value), sorted(formatted_result_data['results']))
                    response_format = formatted_result_data['response_format']
                    if response_format == Question().RESPONSE_FREE:
                        self._test_formatted_response_free(formatted_result_data)
                    elif response_format == Question().RESPONSE_RATING:
                        self._test_formatted_response_rating(formatted_result_data)
                    elif response_format == Question().RESPONSE_TRUE_OR_FALSE:
                        self._test_formatted_response_true_or_false(formatted_result_data)
                    elif response_format == Question().RESPONSE_MULTIPLE_CHOICE:
                        self._test_formatted_response_multiple_choice(formatted_result_data)
                    else:
                        self.fail("unknown response format: {0}".format(response_format))
                    break
        return

    def test_survey_results_api(self):
        formatted_results = Survey().get_formatted_results('test_survey')
        with mock.patch.object(BaseHandler, 'get_current_user') as m:
            m.return_value = self.user_ids[0]
            response = self.fetch('/api/results/test_survey', method="GET")
        result = tornado.escape.json_decode(response.body)
        self.assertEqual(response.code, 200)
        self.assertEqual(result, formatted_results)

    def _test_formatted_response_free(self, formatted_result_data):
        self.assertEqual(formatted_result_data['bar_data'], [])
        self.assertEqual(formatted_result_data['pie_data'], [])
        return

    def _test_formatted_response_rating(self, formatted_result_data):
        logging.info(formatted_result_data)
        bar_data = formatted_result_data['bar_data']
        series_data = bar_data['series'][0]
        self.assertNotEqual(bar_data, [])
        self.assertEqual(sorted(bar_data['labels']), [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        self.assertEqual(len(bar_data['labels']),
            len(series_data),
            "length of {0} does not match length of {1}".format(bar_data['labels'], series_data))
        self.assertEqual(formatted_result_data['pie_data'], [])
        return

    def _test_formatted_response_true_or_false(self, formatted_result_data):
        self.assertEqual(formatted_result_data['bar_data'], [])
        self.assertNotEqual(formatted_result_data['pie_data'], [])
        return

    def _test_formatted_response_multiple_choice(self, formatted_result_data):
        self.assertNotEqual(formatted_result_data['bar_data'], [])
        self.assertEqual(formatted_result_data['pie_data'], [])
        return

    def respond_to_surveys(self):
        survey_response_ids = []
        question_response_ids = []
        questions = self.questions

        def _respond_to_questions(questions):
            d1 = {}
            d2 = {}
            d3 = {}
            d4 = {}
            d1['question_id'] = questions[0]
            d2['question_id'] = questions[1]
            d3['question_id'] = questions[2]
            d4['question_id'] = questions[3]
            d1['response_format'] = Question().RESPONSE_FREE
            d2['response_format'] = Question().RESPONSE_MULTIPLE_CHOICE
            d3['response_format'] = Question().RESPONSE_TRUE_OR_FALSE
            d4['response_format'] = Question().RESPONSE_RATING
            d1['response_data'] = lorem_ipsum.lorem_ipsum()
            d2['response_data'] = random.choice(["alpha", "beta", "gamma", "delta"])
            d3['response_data'] = random.choice([True, False])
            d4['response_data'] = random.randint(0, 10)
            r1 = QuestionResponse().create_item(d1)
            r2 = QuestionResponse().create_item(d2)
            r3 = QuestionResponse().create_item(d3)
            r4 = QuestionResponse().create_item(d4)
            return [r1, r2, r3, r4]

        for responder_id in self.user_ids:
            question_responses = _respond_to_questions(questions)
            for response_id in question_responses:
                question_response_ids.append(response_id)
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
        for question_id in TestSurveyResults.questions:
            Question().delete_item(question_id)
        Survey().delete_item('test_survey')
        for survey_response in TestSurveyResults.survey_response_ids:
            SurveyResponse().delete_item(survey_response)
        for question_response in TestSurveyResults.question_response_ids:
            QuestionResponse().delete_item(question_response)
        for responder_id in TestSurveyResults.user_ids:
            User().delete_item(responder_id)
