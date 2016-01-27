import unittest
import tornado.testing
import tornado.web
import config.config

from handlers.survey_handler import ResponseHandler, SurveyHandler
from config.config import application
from setup import Setup

from server import initialize_db

class TestHandlers(tornado.testing.AsyncHTTPTestCase):
    def setUpClass():
        initialize_db(db='test')

    def get_app(self):
        return application

    def test_home(self):
        response = self.fetch('/')
        self.assertEqual(response.code, 200)

    def test_dashboard(self):
        response = self.fetch('/dashboard')
        self.assertEqual(response.code, 200)

if __name__ == '__main__':
    unittest.main()
