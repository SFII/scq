import tornado.web
import logging
from handlers.base_handler import BaseHandler

class RefreshHandler(BaseHandler):

    def get(self):
        self.refresh_current_user_cookie()
        return self.set_status(200, tornado.escape.json_encode("Success"))
