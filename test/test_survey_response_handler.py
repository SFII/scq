import unittest
import tornado.testing
from tornado.httputil import HTTPHeaders
from test.test_runner import BaseAsyncTest
import ast
import tornado.web
import time
from models.basemodel import BaseModel
from models.course import Course
from models.survey import Survey
from models.user import User
from models.question import Question
from models.survey_response import SurveyResponse
import rethinkdb as r
from handlers.base_handler import BaseHandler
import logging
from unittest import mock


class TestResponseHandler(BaseAsyncTest):
    user_data = {}
    user_id = None
    username = None
    item_type = 'Course'
    item_id = ''
    survey_id = ''
    response_id = ''
    survey_data = {}
    correct_responses = {
        Question().RESPONSE_FREE: 'This class sucks, but the teacher is okay I guess',
        Question().RESPONSE_MULTIPLE_CHOICE: 'beta',
        Question().RESPONSE_TRUE_OR_FALSE: True,
        Question().RESPONSE_RATING: 5
    }
    bad_responses = [{"response_data": None, "response_format": "NOT A FORMAT", "extraneous_field": True}]
    bad_questions = [{"title": "", "response_format": "NOT A FORMAT", "extraneous_field": True}]
    q1 = {
        "title": "q1",
        "response_format": Question().RESPONSE_FREE,
        "options": []
    }
    q2 = {
        "title": "q2",
        "response_format": Question().RESPONSE_MULTIPLE_CHOICE,
        "options": ["alpha", "beta", "gamma", "delta"]
    }
    q3 = {
        "title": "q3",
        "response_format": Question().RESPONSE_TRUE_OR_FALSE,
        "options": [True, False]
    }
    q4 = {
        "title": "q4",
        "response_format": Question().RESPONSE_RATING,
        "options": []
    }
    good_questions = [q1, q2, q3, q4]

    def setUpClass():
        logging.disable(logging.CRITICAL)
        # Creates a bare minimum user data
        data = User().default()
        username = str(time.time())
        data['username'] = username
        data['accepted_tos'] = True
        data['email'] = 'xxx@colorado.edu'
        user_data = data
        # create a user
        user_id = User().create_item(data)
        user_data['id'] = user_id
        item_id = Course().create_generic_item()
        Course().subscribe_user(user_id, item_id)
        TestResponseHandler.user_data = user_data
        TestResponseHandler.user_id = user_id
        TestResponseHandler.username = username
        TestResponseHandler.item_type = 'Course'
        TestResponseHandler.item_id = item_id
        return

    def test_survey_creation_and_response(self):
        self._test_survey_create()
        self._test_survey_read()
        self._test_survey_delete()
        self._test_response_creation()
        self._test_survey_update()
        # self._test_response_acquistion()

    def _test_survey_read(self):
        with mock.patch.object(BaseHandler, 'get_current_user') as m:
            m.return_value = self.user_data
            response = self.fetch('/api/surveys', method="GET")
        self.assertEqual(response.code, 200)
        response_survey_data = tornado.escape.json_decode(response.body)
        self.assertEqual(response_survey_data[0]['id'], self.survey_id)
        self.survey_data = response_survey_data[0]

    def build_response_questions(self):
        def _build(question):
            response_format = question['response_format']
            return {
                'response_data': self.correct_responses[response_format],
                'question_id': question['id'],
                'response_format': response_format
            }
        questions = self.survey_data['questions']
        return list(map(_build, questions))

    def _test_survey_create(self):
        with mock.patch.object(BaseHandler, 'get_current_user') as m:
            m.return_value = self.user_data
            body0 = b""
            response0 = self.fetch('/api/surveys', body=body0, method="POST")
            body1 = tornado.escape.json_encode({'item_type': self.item_type})
            response1 = self.fetch('/api/surveys', body=body1, method="POST")
            body2 = tornado.escape.json_encode({'item_type': self.item_type, 'item_id': self.item_id})
            response2 = self.fetch('/api/surveys', body=body2, method="POST")
            body3 = tornado.escape.json_encode({'item_type': self.item_type, 'item_id': self.item_id, 'questions': 'not an array'})
            response3 = self.fetch('/api/surveys', body=body3, method="POST")
            body4 = tornado.escape.json_encode({'item_type': self.item_type, 'item_id': self.item_id, "questions": self.bad_questions})
            response4 = self.fetch('/api/surveys', body=body4, method="POST")
            body5 = tornado.escape.json_encode({'item_type': self.item_type, 'item_id': self.item_id, "questions": self.good_questions})
            response5 = self.fetch('/api/surveys', body=body5, method="POST")
        self.assertEqual(response0.code, 400)
        self.assertTrue('item_type must be one of' in str(response0.error))
        self.assertEqual(response1.code, 400)
        self.assertTrue(str(response1.error).endswith('item_id cannot be null'))
        self.assertEqual(response2.code, 400)
        self.assertTrue(str(response2.error).endswith('questions cannot be null'))
        self.assertEqual(response3.code, 400)
        self.assertTrue(str(response3.error).endswith("questions must be a json array object"))
        self.assertEqual(response4.code, 400)
        self.assertTrue('Verification errors' in str(response4.error))
        self.assertEqual(response5.code, 200)
        self.assertIsNone(response5.error)
        self.assertIsNotNone(response5.body)
        self.survey_id = ast.literal_eval(response5.body.decode('utf-8'))
        self.user_data = User().get_item(self.user_id)
        # self.user_data['unanswered_surveys'].append(self.survey_id)

    def _test_response_creation(self):
        User().update_item(self.user_id, self.user_data)
        with mock.patch.object(BaseHandler, 'get_current_user') as m:
            m.return_value = self.user_data
            body1 = b""
            response1 = self.fetch('/api/response', body=body1, method="POST")
            body2 = tornado.escape.json_encode({'survey_id': self.survey_id})
            response2 = self.fetch('/api/response', body=body2, method="POST")
            body3 = tornado.escape.json_encode({'survey_id': self.survey_id, 'question_responses': 'not an array'})
            response3 = self.fetch('/api/response', body=body3, method="POST")
            body4 = tornado.escape.json_encode({'survey_id': self.survey_id, "question_responses": self.bad_responses})
            response4 = self.fetch('/api/response', body=body4, method="POST")
            body5 = tornado.escape.json_encode({'survey_id': self.survey_id, "question_responses": self.build_response_questions()})
            response5 = self.fetch('/api/response', body=body5, method="POST")
        self.assertEqual(response1.code, 400)
        self.assertTrue('survey_id cannot be null' in str(response1.error))
        self.assertEqual(response2.code, 400)
        self.assertTrue("question_responses cannot be null" in str(response2.error))
        self.assertEqual(response3.code, 400)
        self.assertTrue("question_responses must be an array" in str(response3.error))
        self.assertEqual(response4.code, 400)
        self.assertTrue("Verification errors" in str(response4.error))
        self.assertEqual(response5.code, 200)
        self.assertIsNone(response5.error)
        self.assertIsNotNone(response5.body)
        self.response_id = ast.literal_eval(response5.body.decode('utf-8'))
        self.user_data['unanswered_surveys'].remove(self.survey_id)
        self.user_data['answered_surveys'].append(self.survey_id)
        self.user_data['survey_responses'].append(self.response_id)
        self.survey_data['responses'].append(self.response_id)
        user_dbdata = User().get_item(self.user_id)
        survey_dbdata = Survey().get_item(self.survey_id)
        self.assertEqual(self.user_data['unanswered_surveys'], user_dbdata['unanswered_surveys'])
        self.assertEqual(self.user_data['answered_surveys'], user_dbdata['answered_surveys'])
        self.assertEqual(self.user_data['survey_responses'], user_dbdata['survey_responses'])
        self.assertEqual(self.survey_data['responses'], survey_dbdata['responses'])

    def _test_survey_delete(self):
        User().update_item(self.user_id, self.user_data)
        with mock.patch.object(BaseHandler, 'get_current_user') as m:
            m.return_value = self.user_data
            endpoint = '/api/surveys?survey_id=' + self.survey_id
            test = {'body': None, 'method': 'DELETE', }
            resp = self.fetch(endpoint, **test)
            self.assertEqual(200, resp.code)
            response = self.fetch('/api/surveys', method="GET")
            self.assertEqual(tornado.escape.json_decode(response.body), [])

    def _test_survey_update(self):
        User().update_item(self.user_id, self.user_data)
        with mock.patch.object(BaseHandler, 'get_current_user') as m:
            m.return_value = self.user_data
            new_questions = [self.q1]
            title = "a new title"
            new_questions[0]['title'] = title
            body = tornado.escape.json_encode({'item_type': self.item_type, 'item_id': self.item_id, "questions": new_questions, 'id': self.survey_id})
            response = self.fetch('/api/surveys', body=body, method="POST")
            self.assertEqual(200, response.code)

            s = Survey().get_item(self.survey_id)
            q = Question().get_item(s['questions'][0])
            self.assertEqual(q['title'], title)

    def tearDownClass():
        user_id = TestResponseHandler.user_id
        survey_id = TestResponseHandler.survey_id
        item_id = TestResponseHandler.item_id
        response_id = TestResponseHandler.response_id
        User().delete_item(user_id)
        Survey().delete_item(survey_id)
        SurveyResponse().delete_item(response_id)
        Course().delete_item(item_id)
        logging.disable(logging.NOTSET)

if __name__ == '__main__':
    unittest.main()
