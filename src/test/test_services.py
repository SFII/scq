import unittest
import tornado.testing
import tornado.web
import config.config

from handlers.survey_handler import Response, Surveys
from config.config import application
from setup import Setup

class TestServices(tornado.testing.AsyncHTTPTestCase):
    Setup().init_data()
    def get_app(self):
        return application
    
    def test_home(self):
        response = self.fetch('/')
        self.assertEqual(response.code, 200)

    def test_surveys(self):
        secure_cookie = tornado.web.create_signed_value(
            config.config.SETTINGS['cookie_secret'],
            'user',
            'userid')
        headers = {'Cookie': '='.join(('user', str(secure_cookie)))}
        response = self.fetch('/api/surveys', headers=headers)
        self.assertEqual(response.code, 200)

    def test_response(self):
        response = self.fetch(
            '/api/response',
            method='POST',
            body='{"survey": "response"}')
        self.assertEqual(response.code, 200)

if __name__ == '__main__':
    unittest.main()
