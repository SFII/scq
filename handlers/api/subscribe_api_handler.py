import tornado.web
import tornado.gen as gen
import json
import time
import logging
import ast
from models.group import Group
from handlers.base_handler import BaseHandler, api_authorized, parse_request_json, refresh_user_cookie_callback


class SubscribeAPIHandler(BaseHandler):
    SUBSCRIBE_ACTION = 'sub'
    UNSUBSCRIBE_ACTION = 'unsub'
    ACTIONS = [SUBSCRIBE_ACTION, UNSUBSCRIBE_ACTION]

    @api_authorized
    @parse_request_json
    @refresh_user_cookie_callback
    def post(self):
        """
        subscribes or unsubscribes a user from a given group
        action: 'sub'/'unsub'
        id: id of the group the current_user wants to subscribe/unsubscribe to
        """
        group_id = self.json_data.get('id', None)
        action = self.json_data.get('action', None)
        user_id = self.current_user['id']
        result = {}
        if group_id is None:
            return self.set_status(400, "id cannot be null")
        group_data = Group().get_item(group_id)
        if group_data is None:
            return self.set_status(400, "group_id {0} does not correspond to a value in the database".format(group_id))
        if action == self.SUBSCRIBE_ACTION:
            result = Group().subscribe_user(user_id, group_id)
        elif action == self.UNSUBSCRIBE_ACTION:
            result = Group().unsubscribe_user(user_id, group_id)
        else:
            return self.set_status(400, "action must be one of {0}".format(ACTIONS))
        return self._analyze_result(result, action)

    def _analyze_result(self, result, action):
        if not result:
            return self.set_status(400, 'Something went wrong')
        replaced = result.get('replaced', 0)
        if replaced:
            return self.set_status(200, 'Success')
        unchanged = result.get('unchanged', 0)
        if unchanged:
            verb = {
                self.SUBSCRIBE_ACTION: 'already subscribed',
                self.UNSUBSCRIBE_ACTION: 'not yet subscribed'
            }[action]
            message = "user is {0} to this group, and cannot {1}. No change has occured.".format(verb, action)
            return self.set_status(400, message)
        logging.error(result)
        return self.set_status(400, 'Something went wrong')
