import tornado.web
from models.user import User
import logging
import json
import time
from functools import wraps


class BaseHandler(tornado.web.RequestHandler):
    json_data = {}

    # any handler can call self.current_user to get the cookie-stored rethinkdb
    # data for a User. The data is set at login (when the cookie is set)
    def get_current_user(self):
        user_cookie = self.get_secure_cookie('user')
        if user_cookie is None:
            return None
        return json.loads(user_cookie.decode('utf-8'))

    def refresh_current_user_cookie(self):
        if self.current_user is None:
            return
        user_id = self.current_user['id']
        user_data = User().get_item(user_id)
        self.set_current_user(user_data)
        return self.get_current_user()

    def clear_current_user_cookie(self):
        self.set_current_user(None)

    def set_current_user(self, user_data):
        if user_data:
            user_data['last_sign_in'] = time.time()
            self.set_secure_cookie('user', tornado.escape.json_encode(user_data))
        else:
            self.clear_cookie('user')
        return self.get_current_user()


def api_authorized(method):
    """
    Decorate methods with this to require that the user be logged in to use the api function.
    If the user is not logged in, the api will return 403 "you must be signed in to use this api"
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        if self.current_user is None:
            return self.set_status(403, "you must be signed in to use this api resource")
        return method(self, *args, **kwargs)
    return wrapper


def refresh_user_cookie_callback(method):
    """
    Decorate methods with this to refresh a users cookie after this API request
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        method(self, *args, **kwargs)
        self.refresh_current_user_cookie()
    return wrapper


def parse_request_json(method):
    """
    Decorate methods with this to parse json from the request body"
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        if len(self.request.body):
            try:
                self.json_data = tornado.escape.json_decode(self.request.body)
            except Exception as e:
                self.json_data = {}
                return self.set_status(400, "JSON syntax error: {0}".format(e))
        return method(self, *args, **kwargs)
    return wrapper
