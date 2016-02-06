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


class ResponseHandler(BaseHandler):

    def post(self):
        """
        Creates and records a users response to a survey
        """
        user_data = self.get_current_user()
        if user_data is None:
            return self.set_status(403, "You must be signed in to use this api")
        survey_id = self.get_argument('survey_id')
        responder_id = user_data['id']
        response_time = time.time()
        survey_data = self.get_item(survey_id)
        if survey_data is None:
            return self.set_status(403, "survey_id does not correspond to a known survey")
