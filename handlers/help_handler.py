import tornado.web
from handlers.base_handler import BaseHandler
import logging


class HelpHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):
        self.refresh_current_user_cookie()
        self.render('help.html')