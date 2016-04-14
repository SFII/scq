import tornado.web
import tornado.gen as gen
import json
import time
import logging
import numpy as np
from time import sleep
from models.survey import Survey
from models.user import User
from handlers.base_handler import BaseHandler, api_authorized


class SurveyResultsHandler(BaseHandler):

    @api_authorized
    def get(self, survey_id):
        """
        gets the formatted results to a survey_id
        """
        results = Survey().get_formatted_results(survey_id)

        for i in results:
            if i['response_format'] == 'multipleChoice':
                i['bar_data']['series'] = np.sum(i['results'], axis=0).tolist()
                
        logging.info(results)
        return self.write(tornado.escape.json_encode(results))
