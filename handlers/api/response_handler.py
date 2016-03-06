import tornado.web
import tornado.gen as gen
import json
import time
import logging
import ast
from time import sleep
from models.survey import Survey
from models.user import User
from models.course import Course
from models.question_response import QuestionResponse
from models.survey_response import SurveyResponse
from handlers.base_handler import BaseHandler, api_authorized, parse_request_json, refresh_user_cookie_callback


class ResponseHandler(BaseHandler):

    @api_authorized
    @parse_request_json
    @refresh_user_cookie_callback
    def post(self):
        """
        Creates and records a users response to a survey
        """
        user_data = self.get_current_user()
        user_responses = user_data.get('survey_responses')
        user_id = user_data['id']
        # If user_responses is not initialized, or is not a list
        if not isinstance(user_responses, list):
            User().update_item(user_id, {'survey_responses': []}, skip_verify=True)
        survey_id = self.json_data.get('survey_id', None)
        if survey_id is None:
            return self.set_status(400, "survey_id cannot be null")
        survey_data = Survey().get_item(survey_id)
        response_time = time.time()
        # survey_id must be a valid survey
        if survey_data is None:
            return self.set_status(400, "survey_id does not correspond to a known survey")
        survey_closed_timestamp = survey_data['closed_timestamp']
        if survey_closed_timestamp is not None:
            if survey_closed_timestamp < response_time:
                return self.set_status(400, "survey_id corresponds to a survey that has closed")
        # survey_id must be in the list of users unanswered_surveys
        if survey_id not in user_data['unanswered_surveys']:
            return self.set_status(400, "users can only respond to surveys in their unanswered_surveys lists")
        question_responses = self.json_data.get('question_responses', None)
        # question_responses must be present
        if question_responses is None:
            return self.set_status(400, "question_responses cannot be null")
        # question_responses must be a list
        if not isinstance(question_responses, (list, tuple)):
            return self.set_status(400, "question_responses must be an array")
        # verify question_response_data
        for index, question_response_data in enumerate(question_responses):
            verified = QuestionResponse().verify(question_response_data)
            if len(verified):
                return self.set_status(400, "Verification errors with question_responses[{0}]: {1}".format(index, verified))
        # batch create question responses
        question_response_ids = QuestionResponse().create_batch(question_responses, skip_verify=True)
        # create survey data and post it
        survey_response_data = {
            'question_responses': question_response_ids,
            'survey_id': survey_id,
            'responder_id': user_id,
            'response_time': response_time
        }
        survey_response_id = SurveyResponse().create_item(survey_response_data, skip_verify=True)
        User().remove_item_from_listfield(user_id, 'unanswered_surveys', survey_id)
        User().append_item_to_listfield(user_id, 'answered_surveys', survey_id)
        User().append_item_to_listfield(user_id, 'survey_responses', survey_response_id)
        Survey().append_item_to_listfield(survey_id, 'responses', survey_response_id)
        self.set_status(200, "Success")
        return self.write(tornado.escape.json_encode(survey_response_id))
