import tornado.web
import tornado.gen as gen
import json
import time
import logging
from time import sleep
from models.survey import Survey
from models.user import User
from models.course import Course
from handlers.base_handler import BaseHandler, api_authorized, parse_request_json, refresh_user_cookie_callback


class MeHandler(BaseHandler):

    @api_authorized
    @parse_request_json
    @refresh_user_cookie_callback
    def post(self):
        """
        Creates or updates existing user data
        If successful, returns the updated user data
        """
        user_data = self.get_current_user()
        user_id = user_data['id']
        primary_affiliation = self.json_data.get('primary_affiliation', user_data.get('primary_affiliation', ''))
        status = self.json_data.get('status', user_data['status'])
        email = self.json_data.get('email', user_data['email'])
        dob = self.json_data.get('dob', user_data['dob'])
        gender = self.json_data.get('gender', user_data['gender'])
        ethnicity = self.json_data.get('ethnicity', user_data['ethnicity'])
        native_language = self.json_data.get('native_language', user_data['native_language'])
        logging.info(self.json_data)
        majors = self.json_data.get('majors', user_data.get('majors', []))
        minors = self.json_data.get('minors', user_data.get('minors', []))
        departments = self.json_data.get('departments', user_data.get('departments', []))
        courses = self.json_data.get('courses', user_data.get('courses', []))
        courses_taught = self.json_data.get('courses_taught', user_data.get('courses_taught', []))
        post_data = {
            'primary_affiliation': primary_affiliation,
            'status': status,
            'email': email,
            'dob': dob,
            'gender': gender,
            'ethnicity': ethnicity,
            'native_language': native_language,
            'majors': majors,
            'minors': minors,
            'departments': departments,
            'courses': courses,
            'courses_taught': courses_taught,
        }
        if 'id' in post_data.keys():
            return self.set_status(403, "user id cannot be changed")
        if 'username' in post_data.keys():
            return self.set_status(403, "username cannot be changed")
        user_data.update(post_data)
        errors = User().verify(user_data)
        if not len(errors):
            User().update_item(user_id, user_data, skip_verify=True)
            self.set_status(200, "Success")
            return self.write(tornado.escape.json_encode(user_data))
        return self.set_status(403, "Verification errors: {0}".format(errors))

    @api_authorized
    def get(self):
        return self.write(tornado.escape.json_encode(self.get_current_user()))
