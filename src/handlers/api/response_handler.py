import tornado.web
import tornado.gen as gen
import json
import time
import logging
from time import sleep
from models.survey import Survey
from models.user import User
from models.course import Course
from models.question_response import QuestionResponse
from models.survey_response import SurveyResponse
from handlers.base_handler import BaseHandler


class ResponseHandler(BaseHandler):

    def post(self):
        """
        Creates and records a users response to a survey
        """
        user_data = self.get_current_user()
        # user must be logged in
        if user_data is None:
            return self.set_status(403, "you must be signed in to use this api")
        user_responses = user_data.get_item('survey_responses')
        user_id = user_data['id']
        # If user_responses is not initialized, or is not a list
        if not isinstance(user_responses, list):
            User.update(user_id, {'survey_responses', []})
        survey_id = self.get_argument('survey_id')
        survey_data = Survey().get_item(survey_id)
        response_time = time.time()
        # survey_id must be a valid survey
        if survey_data is None:
            return self.set_status(403, "survey_id does not correspond to a known survey")
        survey_closed_timestamp = survey_data['closed_timestamp']
        if survey_closed_timestamp is not None:
            if survey_closed_timestamp < response_time
            return self.set_status(403, "survey_id corresponds to a survey that has closed")
        # survey_id must be in the list of users unanswered_surveys
        if survey_id not in user_data['unanswered_surveys']:
            return self.set_status(403, "users can only respond to surveys in their unanswered_surveys lists")
        question_responses_json = self.get_argument('question_responses', None)
        # question_responses must be present
        if question_responses_json is None:
            return self.set_status(403, "question_responses must be None")
        question_responses = json.loads(question_responses_json)
        # question_responses must be a list
        if not isinstance(question_responses, list):
            return self.set_status(403, "question_responses must be an array")
        # verify question_response_data
        for question_response_data in question_responses:
            verified = QuestionResponse().verify(question_response_data)
            if len(verified):
                return self.set_status(403, "Verification errors: {0}".format(verified))
        # batch create question responses
        question_response_ids = QuestionResponse().create_batch(question_responses, skip_verify=True)
        # create survey data and post it
        survey_response_data = {
            'question_responses': question_response_ids,
            'survey_id': survey_ids,
            'responder_id': user_id,
            'response_time': response_time
        }
        survey_response_id = SurveyResponse.create_item(survey_response_data, skip_verify=True)
        User().remove_item_from_listfield(user_id, 'unanswered_surveys', survey_id)
        User().append_item_to_listfield(user_id, 'survey_responses', survey_response_id)
        Survey().append_item_to_listfield(survey_id, 'survey_responses', survey_response_id)
        self.set_status(200, "Success")
        return self.write(tornado.escape.json_encode(survey_response_id))
