import unittest
import tornado.testing
import tornado.web
import logging
from test.test_runner import BaseAsyncTest


class TestStaticHandlers(BaseAsyncTest):
    def setUpClass():
        logging.disable(logging.CRITICAL)

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
