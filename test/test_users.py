import unittest
from test.test_runner import BaseAsyncTest
import tornado.web
import time
from models.user import User
import rethinkdb as r
import logging


class TestUser(BaseAsyncTest):
    user_data = {}
    user_id = None
    username = None

    def setUpClass():
        logging.disable(logging.CRITICAL)
        # Creates a bare minimum user data
        data = User().default()
        TestUser.username = str(time.time())
        data['username'] = TestUser.username
        data['accepted_tos'] = True
        data['email'] = 'xxx@colorado.edu'
        TestUser.user_data = data
        TestUser.user_id = User().create_item(data)
        return

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
        logging.disable(logging.NOTSET)


if __name__ == '__main__':
    unittest.main()
