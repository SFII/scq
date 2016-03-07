import unittest
import tornado.web
import tornado.testing
from tornado.httputil import HTTPHeaders
from test.test_runner import BaseAsyncTest
import time
import rethinkdb as r
import logging
from models.basemodel import BaseModel
from models.user import User
from models.group import Group
from models.survey import Survey
from unittest import mock
from handlers.base_handler import BaseHandler


class TestGroupSubscribe(BaseAsyncTest):
    generic_user_id = ""
    generic_user_data = {}
    generic_group_id = ""
    generic_user_data = {}

    def setUpClass():
        logging.disable(logging.CRITICAL)
        TestGroupSubscribe.generic_user_id = User().create_generic_item()
        TestGroupSubscribe.generic_user_data = User().get_item(TestGroupSubscribe.generic_user_id)
        TestGroupSubscribe.generic_group_id = Group().create_generic_item()
        TestGroupSubscribe.generic_group_data = Group().get_item(TestGroupSubscribe.generic_group_id)
        return

    def test_api_group(self):
        with mock.patch.object(BaseHandler, 'get_current_user') as m:
            m.return_value = User().get_item(self.generic_user_id)
            bodya = tornado.escape.json_encode({})
            bodyb = tornado.escape.json_encode({'id': self.generic_group_id})
            bodyc = tornado.escape.json_encode({'id': str(time.time())})
            bodyd = tornado.escape.json_encode({'id': 'not unique'})
            response0 = self.fetch('/api/groups', body=bodya, method="POST")
            response1 = self.fetch('/api/groups', body=bodyb, method="POST")
            response2 = self.fetch('/api/groups', body=bodyc, method="POST")
            response3 = self.fetch('/api/groups', method="GET")
        self.assertEqual(response0.code, 400)
        self.assertTrue('id cannot be null' in str(response0.error))
        self.assertEqual(response1.code, 400)
        self.assertTrue('group with id' in str(response1.error))
        self.assertEqual(response2.code, 200, str(response2.error))
        self.assertEqual(response3.code, 200, str(response3.error))

    def test_api_subscribe(self):
        with mock.patch.object(BaseHandler, 'get_current_user') as m:
            m.return_value = User().get_item(self.generic_user_id)
            bodya = tornado.escape.json_encode({'action': 'sub'})
            bodyb = tornado.escape.json_encode({'action': 'sub', 'id': self.generic_group_id})
            bodyc = tornado.escape.json_encode({'action': 'sub', 'id': 'xxx'})
            bodyd = tornado.escape.json_encode({'action': 'unsub', 'id': 'xxx'})
            bodye = tornado.escape.json_encode({'action': 'unsub', 'id': self.generic_group_id})
            response0 = self.fetch('/api/subscribe', body=bodya, method="POST")
            response1 = self.fetch('/api/subscribe', body=bodyc, method="POST")
            response2 = self.fetch('/api/subscribe', body=bodyb, method="POST")
            response3 = self.fetch('/api/subscribe', body=bodyb, method="POST")
            response4 = self.fetch('/api/subscribe', body=bodyd, method="POST")
            response5 = self.fetch('/api/subscribe', body=bodye, method="POST")
            response6 = self.fetch('/api/subscribe', body=bodye, method="POST")
        self.assertEqual(response0.code, 400)
        self.assertTrue('id cannot be null' in str(response0.error))
        self.assertEqual(response1.code, 400)
        self.assertTrue('group_id xxx does not correspond' in str(response1.error))
        self.assertEqual(response2.code, 200)
        self.assertEqual(response3.code, 400)
        self.assertTrue('user is already subscribed to this group' in str(response3.error))
        self.assertEqual(response4.code, 400)
        self.assertTrue('group_id xxx does not correspond' in str(response4.error))
        self.assertEqual(response5.code, 200)
        self.assertEqual(response6.code, 400)
        self.assertTrue('user is not yet subscribed to this group' in str(response6.error))

    def _test_group_survey_percolation(self):
        # see surveys in a group's list of active_surveys
        survey_id = Survey().create_generic_item(creator_id=None, item_id=self.generic_group_id, item_type='Group')
        self.generic_group_data = Group().get_item(self.generic_user_id)
        active_surveys = self.generic_group_data.get('active_surveys', [])
        message = "expected survey_id {0} in group {1} active_surveys".format(survey_id, self.generic_group_id)
        self.assertIn(survey_id, active_surveys, message)

    def test_subscribe_unsubscribe_user(self):
        # create a survey and subscribe a user to a group
        survey_id = Survey().create_generic_item(creator_id=None, item_id=self.generic_group_id, item_type='Group')
        Group().subscribe_user(self.generic_user_id, self.generic_group_id)
        self.generic_user_data = User().get_item(self.generic_user_id)
        self.generic_group_data = Group().get_item(self.generic_group_id)
        subscribers = self.generic_group_data.get('subscribers', [])
        subscribed_groups = self.generic_user_data.get('subscribed_groups', [])
        user_unanswered_surveys = self.generic_user_data.get('unanswered_surveys', [])
        message1 = "expected group id {0} in user {1} subscribed_groups".format(self.generic_group_id, self.generic_user_id)
        message2 = "expected user id {0} in group {1} subscribers".format(self.generic_user_id, self.generic_group_id)
        message3 = "expected survey_id {0} in user {1} unanswered_surveys".format(survey_id, self.generic_user_id)
        self.assertIn(self.generic_group_id, subscribed_groups, message1)
        self.assertIn(self.generic_user_id, subscribers, message2)
        self.assertIn(survey_id, user_unanswered_surveys, message3)
        # create a new survey after the user has subscribed and see it percolate to the user
        survey_id2 = Survey().create_generic_item(creator_id=None, item_id=self.generic_group_id, item_type='Group')
        message4 = "expected survey_id {0} in user {1} unanswered_surveys".format(survey_id2, self.generic_user_id)
        self.generic_user_data = User().get_item(self.generic_user_id)
        user_unanswered_surveys = self.generic_user_data.get('unanswered_surveys', [])
        self.assertIn(survey_id2, user_unanswered_surveys, message4)
        pass

    def tearDownClass():
        logging.disable(logging.NOTSET)
        # Drop the database
        Group().delete_item(TestGroupSubscribe.generic_group_id)
        User().delete_item(TestGroupSubscribe.generic_user_id)
