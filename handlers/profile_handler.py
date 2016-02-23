import tornado.web
from handlers.base_handler import BaseHandler
from models.survey import Survey
import logging


class DashboardHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):
        self.refresh_current_user_cookie()
        self.render('profile.html')