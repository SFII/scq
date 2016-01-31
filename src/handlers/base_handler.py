import tornado.web
from models.user import User
import logging
import json


class BaseHandler(tornado.web.RequestHandler):

    # any handler can call self.current_user to get the cookie-stored rethinkdb
    # data for a User. The data is set at login (when the cookie is set)
    def get_current_user(self):
        user_cookie = self.get_secure_cookie('user')
        if user_cookie is None:
            return None
        return json.loads(user_cookie.decode("utf-8"))

    def refresh_current_user_cookie(self):
        if self.current_user is None:
            return
        user_id = self.current_user['id']
        user_data = User().get_item(user_id)
        self.set_current_user(user_data)
        return

    def clear_current_user_cookie(self):
        self.set_current_user(None)

    def set_current_user(self, user_data):
        if user_data:
            user_data['last_sign_in'] = time.time()
            self.set_secure_cookie('user', tornado.escape.json_encode(user_data))
        else:
            self.clear_cookie('user')
