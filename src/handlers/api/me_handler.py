import tornado.web
import tornado.gen as gen
import json
import time
import logging
from time import sleep
from models.survey import Survey
from models.user import User
from models.course import Course
from handlers.base_handler import BaseHandler


class MeHandler(BaseHandler):

    def post(self):
        """
        Creates or updates existing user data
        If successful, returns the updated user data
        """
        user_data = self.get_current_user()
        if user_data is None:
            return self.set_status(403, "You must be signed in to use this api")
        user_id = user_data['id']
        post_data = {k: self.get_argument(k) for k in self.request.arguments}
        logging.info(post_data)
        if 'id' in post_data.keys():
            return self.set_status(403, "user id cannot be changed")
        user_data.update(post_data)
        logging.info(user_data)
        errors = User().verify(user_data)
        if not len(errors):
            User().update_item(user_id, user_data)
            self.set_status(200, "Success")
            return self.write(tornado.escape.json_encode(user_data))
        return self.set_status(403, "Verification errors: {0}".format(errors))

    def get(self):
        return self.write(tornado.escape.json_encode(self.get_current_user()))
