import unittest
import tornado.testing
import tornado.web
import config.config
import time
from models.basemodel import BaseModel
from models.user import User
import rethinkdb as r
from handlers.survey_handler import Response, Surveys
from config.config import application
from setup import Setup


class TestUser(tornado.testing.AsyncHTTPTestCase):
    user_data = {}
    user_id = None
    username = None

    def setUpClass():
        # Designates Basemodel to use the test database
        BaseModel.DB = 'test'
        # Gives Basemodel a direct connection to the rethinkdb
        BaseModel.conn = r.connect(host='localhost', port=28015)
        # Creates a bare minimum user data
        data = User().default()
        TestUser.username = str(time.time())
        data['username'] = TestUser.username
        data['accepted_tos'] = True
        data['email'] = 'xxx@colorado.edu'
        TestUser.user_data = data
        TestUser.user_id = User().create_item(data)
        return

    def get_app(self):
        return application

    def test_testing_authentication(self):
        self.assertEqual(TestUser.user_data['registration'], User().REGISTRATION_TESTING)
        good_auth = User().authenticate(TestUser.user_id, User().TESTING_PASSWORD)
        bad_auth = User().authenticate(TestUser.user_id, 'wrong password')
        self.assertTrue(good_auth)
        self.assertFalse(bad_auth)

    def test_verify_valid_user(self):
        verify = User().verify(TestUser.user_data)
        self.assertEqual(verify, [])

    def test_verify_invalid_user(self):
        verify = User().verify(User().default())
        self.assertNotEqual(len(verify), 0)

    def test_created_user(self):
        self.assertIsNotNone(TestUser.user_id)
        db_user_data = User().get_item(TestUser.user_id)
        for key in TestUser.user_data:
            self.assertEqual(TestUser.user_data[key], db_user_data[key])

    def tearDownClass():
        x = User().delete_item(TestUser.user_id)


if __name__ == '__main__':
    unittest.main()
