import tornado.web
from handlers.base_handler import BaseHandler
import logging
class DashboardHandler(BaseHandler):

    # @tornado.web.authenticated
    def get(self):
        self.refresh_current_user_cookie()
        self.render('dashboard.html', page_json=self.page_json())

    def page_json(self):
        user_data = self.current_user
        print('-----------------------------------------------')
        print(user_data)
        unanswered_survey_ids = user_data['unanswered_surveys']
        print(unanswered_survey_ids)
        return []
