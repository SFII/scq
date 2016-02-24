import tornado.web
import tornado.gen as gen
import json
import time
import logging
from time import sleep
from models.survey import Survey
from models.user import User
from models.course import Course
from handlers.base_handler import BaseHandler, api_authorized, parse_request_json


class MeHandler(BaseHandler):

    @api_authorized
    @parse_request_json
    def post(self):
        """
        Creates or updates existing user data
        If successful, returns the updated user data
        """
        user_data = self.get_current_user()
        user_id = user_data['id']
        primary_affiliation = self.json_data.get('primary_affiliation', user_data['primary_affiliation']).split(',')
        status = self.json_data.get('status', user_data['status'])
        email = self.json_data.get('email', user_data['email'])
        dob = self.json_data.get('dob', user_data['dob'])
        gender = self.json_data.get('gender', user_data['gender'])
        ethnicity = self.json_data.get('ethnicity', user_data['ethnicity'])
        native_language = self.json_data.get('native_language', user_data['native_language'])
        major1 = self.json_data.get('major1', user_data['major1'])
        major2 = self.json_data.get('major2', user_data['major2'])
        major3 = self.json_data.get('major3', user_data['major3'])
        major4 = self.json_data.get('major4', user_data['major4'])
        minor1 = self.json_data.get('minor1', user_data['minor1'])
        minor2 = self.json_data.get('minor2', user_data['minor2'])
        departments = self.json_data.get('departments', user_data['departments']).split(',')
        courses = self.json_data.get('courses', user_data['courses']).split(',')
        courses_taught = self.json_data.get('courses_taught', user_data['courses_taught']).split(',')
        post_data = {
            'primary_affiliation': primary_affiliation,
            'status': status,
            'email': email,
            'dob': dob,
            'gender': gender,
            'ethnicity': ethnicity,
            'native_language': native_language,
            'major1': major1,
            'major2': major2,
            'major3': major3,
            'major4': major4,
            'minor1': minor1,
            'minor2': minor2,
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
