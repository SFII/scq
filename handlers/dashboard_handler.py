import tornado.web
from handlers.base_handler import BaseHandler
from models.survey import Survey
import logging


class DashboardHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):
        self.refresh_current_user_cookie()
        self.render('dashboard.html', survey_json=self.get_survey_json(), response_data_json=self.get_response_data(), user_info_json=self.get_user_info())

    def get_survey_json(self):
        survey_json = []
        user_data = self.current_user
        unanswered_survey_ids = user_data['unanswered_surveys']
        for survey_id in unanswered_survey_ids:
            survey_data = Survey().decompose_from_id(survey_id)
            if survey_data is None:
                continue
            survey_json.append(survey_data)
        #print(tornado.escape.json_encode(survey_json))
        return tornado.escape.json_encode(survey_json)
    
    def get_user_info(self):
        user_info_json = []
        user_data = self.current_user
        user_info_json.append(user_data)
        logging.info(tornado.escape.json_encode(user_info_json))
        return tornado.escape.json_encode(user_info_json)
