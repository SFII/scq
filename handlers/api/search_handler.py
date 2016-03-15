import tornado.web
import tornado.gen as gen
import json
import time
import logging
from models.group import Group
from models.question_response import QuestionResponse
from models.survey_response import SurveyResponse
from handlers.base_handler import BaseHandler, api_authorized, parse_request_json, refresh_user_cookie_callback


class SearchHandler(BaseHandler):

    @api_authorized
    @parse_request_json
    @refresh_user_cookie_callback
    def post(self):
        """
        Makes a request to search for a specific
        searchtype: Group
        searchstring: ""
        requestedfields: []
        """
        search_type = self.json_data.get('searchtype', 'Group')
        search_string = self.json_data.get('searchstring', '')
        requestedfields = self.json_data.get('requestedfields', ['id'])
        search_model = {
            'Group': Group()
        }[search_type]
        search_fields = {
            'Group': ['id', 'name', 'tags']
        }[search_type]
        search_model.search_items(search_string, search_fields, requestedfields)
        self.set_status(200, "Success")
        return self.write(tornado.escape.json_encode(survey_response_id))
