import unittest
import tornado.testing
import tornado.web
import config.config
from models.basemodel import BaseModel
import rethinkdb as r
from handlers.survey_handler import ResponseHandler, SurveyHandler
from config.config import application
from setup import Setup

class TestServices(tornado.testing.AsyncHTTPTestCase):

    def setUpClass():
        # These two methods must be called to be sure a test database is used
        BaseModel.DB = 'test'
        BaseModel.conn = r.connect(host='localhost', port=28015)
        return

    def get_app(self):
        return application

    def test_surveys(self):
        secure_cookie = tornado.web.create_signed_value(
            config.config.SETTINGS['cookie_secret'],
            'user',
            'userid')
        headers = {'Cookie': '='.join(('user', str(secure_cookie)))}
        response = self.fetch('/api/surveys', headers=headers)
        self.assertEqual(response.code, 200)

    # def test_response(self):
    #     response = self.fetch(
    #         '/api/response',
    #         method='POST',
    #         body='{"survey": "response"}')
    #     self.assertEqual(response.code, 200)

if __name__ == '__main__':
    unittest.main()
