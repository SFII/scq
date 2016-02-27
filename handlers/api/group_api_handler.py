import tornado.web
import tornado.gen as gen
import json
import time
import logging
import ast
from models.group import Group
from handlers.base_handler import BaseHandler, api_authorized, parse_request_json


class GroupAPIHandler(BaseHandler):

    @api_authorized
    @parse_request_json
    def post(self):
        """
        Creates or updates an existing group object
        If the id is present, it will update the existing survey
        """
        group_id = self.json_data.get('id', None)
        if group_id is None:
            return self._create_group()
        else:
            return self._edit_group(group_id)

    def _create_group(self):
        group_data = self._group_from_request()
        if group_data is None:
            return
        group_id = Group().create_item(group_data)
        self.set_status(200, "Success")
        return self.write(tornado.escape.json_encode(group_id))

    def _edit_group(self, group_id):
        group_data = self._group_from_request()
        if group_data is None:
            return
        Group().update_item(group_id, group_data)
        self.set_status(200, "Success")

    def _group_from_request(self):
        creator_id = self.current_user['id']
        creator_name = self.current_user['username']
        item_type = self.json_data.get('item_type', None)
        item_id = self.json_data.get('item_id', None)
        item_name = self.json_data.get('item_name', None)
        questions = self.json_data.get('questions', None)
        if item_type not in Group().ITEM_TYPES:
            return self.set_status(400, "item_type must be one of {0}".format(Group().ITEM_TYPES))
        if item_id is None:
            return self.set_status(400, "item_id cannot be null")
        if item_name is None:
            model = Group()._model_from_item_type(item_type)
            item_data = model.get_item(item_id)
            if item_data is None:
                message = "{0} item_id {1} does not correspond to value in database".format(item_type, item_id)
                return self.set_status(400, message)
            name = {
                'Instructor': 'instructor_last',
                'Course': 'course_name',
                'User': 'username'
            }[item_type]
            item_name = item_data[name]
        if questions is None:
            return self.set_status(400, "questions cannot be null")
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
            'item_type': item_type,
            'item_id': item_id,
            'item_name': item_name,
            'questions': question_ids,
            'responses': [],
            'created_timestamp': time.time(),
            'closed_timestamp': None,
            'deleted': False,
        }
        verified = Group().verify(survey_data)
        if len(verified):
            return self.set_status(400, "Verification errors: {0}".format(verified))
        return survey_data

    @api_authorized
    @parse_request_json
    def delete(self):
        survey_id = self.get_query_argument('survey_id')
        Group().mark_deleted(survey_id)

    @api_authorized
    @parse_request_json
    def get(self):
        surveys = []
        unanswered_group_ids = self.current_user['unanswered_groups']
        for survey_id in unanswered_group_ids:
            survey_data = Group().decompose_from_id(survey_id)
            if survey_data is None:
                continue
            if survey_data['deleted']:
                continue
            surveys.append(survey_data)
        self.set_status(200, "Success")
        return self.write(tornado.escape.json_encode(surveys))
