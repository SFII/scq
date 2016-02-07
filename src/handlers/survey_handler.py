import tornado.web
import tornado.gen as gen
import json
import time
import logging
from models.survey import Survey
from models.user import User
from models.course import Course
from handlers.base_handler import BaseHandler


class SurveyHandler(BaseHandler):

    def post(self):
        """
        Creates or updates an existing survey object
        If the id is present, it will update the existing survey
        """
        if self.current_user() is None:
            return None
        survey_id = self.get_argument('id', None)
        if survey_id is None:
            return self.create_survey()
        else:
            return self.edit_survey()

    def create_survey(self):
        creator_id = self.current_user['id']
        creator_name = self.current_user['username']
        course_id = self.get_argument('course_id', None)
        course_name = self.get_argument('course_name', None)
        questions_json = self.get_argument('questions', None)
        if course_id is None:
            return self.set_status(403, "course_id cannot be null")
        if course_name is None:
            course_data = Course().get_item(course_id)
            if course_data is None:
                return self.set_status(403, "course_id {0} does not correspond to value in database".format(course_id))
            course_name = course_data['course_name']
        if questions_json is None:
            return self.set_status(403, "questions cannot be null")
        questions = json.loads(questions_json)
        if not isinstance(questions, list):
            return self.set_status(403, "questions must be an array object")
        survey_data = {
            'creator_id': creator_id,
            'creator_name': creator_name,
            'course_id': course_id,
            'course_name': course_name,
            'questions': questions,
        }
        verified = Survey().verify(survey_data)
        if len(verified):
            return self.set_status(403, "Verification errors: {0}".format(verified))
        survey_id = Survey().create_item(survey_data)
        self.set_status(200, "Success")
        return self.write(tornado.escape.json_encode(survey_id))

    def edit_survey(self):
        pass

    def get(self):
        user_data = self.get_current_user()
        if user_data is None:
            return None
        surveys = []
        unanswered_survey_ids = user_data['unanswered_surveys']
        for survey_id in unanswered_survey_ids:
            survey_data = Survey().decompose_from_id(survey_id)
            if survey_data is None:
                continue
            surveys.append(survey_data)
        logging.info(unanswered_survey_ids)
        logging.info(surveys)
        self.set_status(200, "Success")
        return self.write(tornado.escape.json_encode(surveys))
