import tornado.web
from handlers.base_handler import BaseHandler
import logging
class DashboardHandler(BaseHandler):

    # @tornado.web.authenticated
    def get(self):
        self.refresh_current_user_cookie()
        page_json = self.current_user
        self.render('dashboard.html', page_json=page_json)
