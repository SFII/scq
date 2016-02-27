import tornado.web
from handlers.base_handler import BaseHandler
import logging


class SurveysHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):
        self.refresh_current_user_cookie()
        self.render('surveys.html', user_info_json=self.get_user_info())
    
    def get_user_info(self):
        user_info_json = []
        user_data = self.current_user
        user_info_json.append(user_data)
        logging.info(tornado.escape.json_encode(user_info_json))
        return tornado.escape.json_encode(user_info_json)