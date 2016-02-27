import unittest
from test.test_runner import BaseAsyncTest
import time
import rethinkdb as r
import logging
from models.basemodel import BaseModel
from models.user import User
from models.group import Group


class TestGroupSubscribe(BaseAsyncTest):
    generic_user_id = ""
    generic_user_data = {}
    generic_group_id = ""
    generic_user_data = {}

    def setUpClass():
        logging.disable(logging.CRITICAL)
        self.generic_user_id = User().create_generic_item()
        self.generic_user_data = User().get_item(generic_user_id)
        self.generic_group_id = Group().create_generic_item()
        self.generic_group_data = Group().get_item(generic_user_id)
        return

    def test_api_create():
        pass

    def test_api_subscribe():
        # * a user subscribes to a group
        # the user is added to the groups subscribers
        # the group is added to the users subscribed groups
        # subscribed user gets sent active surveys
        # * a survey is added for the group
        # the survey is percolated to all subscribers
        #
        pass

    def test_api_unsubscribe():
        pass

    def test_subscribe_user():
        pass

    def test_unsubscribe_user():
        pass
