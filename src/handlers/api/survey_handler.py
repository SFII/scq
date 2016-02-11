import tornado.web
import tornado.gen as gen
import json
import time
import logging
import ast
from models.survey import Survey
from models.user import User
from models.course import Course
from models.question import Question
from handlers.base_handler import BaseHandler, api_authorized, parse_request_json


class SurveyHandler(BaseHandler):

    @api_authorized
    @parse_request_json
    def post(self):
        """
        Creates or updates an existing survey object
        If the id is present, it will update the existing survey
        """
        survey_id = self.json_data.get('id', None)
        if survey_id is None:
            return self._create_survey()
        else:
            return self._edit_survey()

    def _create_survey(self):
        creator_id = self.current_user['id']
        creator_name = self.current_user['username']
        course_id = self.json_data.get('course_id', None)
        course_name = self.json_data.get('course_name', None)
        questions_json = self.json_data.get('questions', None)
        if course_id is None:
            return self.set_status(400, "course_id cannot be null")
        if course_name is None:
            course_data = Course().get_item(course_id)
            if course_data is None:
                return self.set_status(400, "course_id {0} does not correspond to value in database".format(course_id))
            course_name = course_data['course_name']
        if questions_json is None:
            return self.set_status(400, "questions cannot be null")
        try:
            questions = ast.literal_eval(tornado.escape.json_decode(questions_json))
        except:
            return self.set_status(400, "questions must be a json array object")
        if not isinstance(questions, (list, tuple)):
            return self.set_status(400, "questions must be a json array object")
        # verify question_response_data
        for index, question_data in enumerate(questions):
            verified = Question().verify(question_data)
            if len(verified):
                return self.set_status(400, "Verification errors with question[{0}]: {1}".format(index, verified))
        # batch create question responses
        question_ids = Question().create_batch(questions, skip_verify=True)
        survey_data = {
            'creator_id': creator_id,
            'creator_name': creator_name,
            'course_id': course_id,
            'course_name': course_name,
            'questions': question_ids,
            'responses': [],
            'created_timestamp': time.time(),
            'closed_timestamp': None
        }
        verified = Survey().verify(survey_data)
        if len(verified):
            return self.set_status(400, "Verification errors: {0}".format(verified))
        survey_id = Survey().create_item(survey_data)
        self.set_status(200, "Success")
        return self.write(tornado.escape.json_encode(survey_id))

    def _edit_survey(self):
        pass

    @api_authorized
    @parse_request_json
    def get(self):
        surveys = []
        unanswered_survey_ids = self.current_user['unanswered_surveys']
        for survey_id in unanswered_survey_ids:
            survey_data = Survey().decompose_from_id(survey_id)
            if survey_data is None:
                continue
            surveys.append(survey_data)
        self.set_status(200, "Success")
        return self.write(tornado.escape.json_encode(surveys))
