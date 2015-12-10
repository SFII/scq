import tornado.web
from handlers.base_handler import BaseHandler
from models.survey import Survey
import logging
class DashboardHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):
        self.refresh_current_user_cookie()
        self.render('dashboard.html', survey_json=self.get_survey_json())

    def get_survey_json(self):
        survey_json = []
        user_data = self.current_user
        print(self.current_user)
        unanswered_survey_ids = user_data['unanswered_surveys']
        for survey_id in unanswered_survey_ids:
            survey_data = Survey().decompose(survey_id)
            survey_json.append(survey_data)
        print(survey_json)
        return survey_json
