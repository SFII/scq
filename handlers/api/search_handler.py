import tornado.web
import tornado.gen as gen
import json
import time
import logging
from models.group import Group
from models.user import User
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
            'Group': Group(),
            'User': User()
        }[search_type]
        search_fields = {
            'Group': ['id', 'tags'],
            'User': ['username']
        }[search_type]
        try:
            search_results = search_model.search_items(search_string, search_fields, requestedfields)
        except err:
            return self.set_status(400, "Something went wrong")
        self.set_status(200, "Success")
        return self.write(tornado.escape.json_encode(search_results))
