import tornado.web
import tornado.gen as gen
import json
import time
import logging
from time import sleep
from models.survey import Survey
from models.user import User
from models.course import Course
from handlers.base_handler import BaseHandler, api_authorized


class MeHandler(BaseHandler):

    @api_authorized
    def post(self):
        """
        Creates or updates existing user data
        If successful, returns the updated user data
        """
        user_data = self.get_current_user()
        user_id = user_data['id']
        post_data = {k: self.get_argument(k) for k in self.request.arguments}
        if 'id' in post_data.keys():
            return self.set_status(403, "user id cannot be changed")
        user_data.update(post_data)
        errors = User().verify(user_data)
        if not len(errors):
            User().update_item(user_id, user_data)
            self.set_status(200, "Success")
            return self.write(tornado.escape.json_encode(user_data))
        return self.set_status(403, "Verification errors: {0}".format(errors))

    @api_authorized
    def get(self):
        return self.write(tornado.escape.json_encode(self.get_current_user()))
