import unittest
import tornado.testing

from handlers.survey_handler import Response, Surveys
from config.config import application

class TestServices(tornado.testing.AsyncHTTPTestCase):
    def get_app(self):
        return application

    def test_home(self):
        response = self.fetch('/')
        self.assertEqual(response.code, 200)

    def test_surveys(self):
        headers = {'Cookie': '='+'user'+'uid123'}
        response = self.fetch('/api/surveys', headers=headers)
        self.assertEqual(response.code, 200)

if __name__ == '__main__':
    unittest.main()
