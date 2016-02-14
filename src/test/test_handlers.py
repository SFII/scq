import unittest
import tornado.testing
import tornado.web
import config.config
import logging
from config.config import application
from setup import Setup
from server import initialize_db


class TestHandlers(tornado.testing.AsyncHTTPTestCase):
    def setUpClass():
        logging.disable(logging.CRITICAL)
        initialize_db(db='test')

    def get_app(self):
        return application

    def test_home(self):
        response = self.fetch('/')
        self.assertEqual(response.code, 200)

    def test_dashboard(self):
        response = self.fetch('/dashboard')
        self.assertEqual(response.code, 200)

    def tearDownClass():
        logging.disable(logging.NOTSET)

if __name__ == '__main__':
    unittest.main()
