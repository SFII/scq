import unittest
import tornado.testing
import tornado.web
import config.config
import time
from models.basemodel import BaseModel
from models.question import Question
from models.instructor import Instructor
from models.question_response import QuestionResponse
from models.course import Course
from models.survey import Survey
from models.survey_response import SurveyResponse
from models.user import User
import rethinkdb as r
from config.config import application
from setup import Setup
from server import initialize_db
import logging


class TestModels(tornado.testing.AsyncHTTPTestCase):
    models = [User(), Course(), Instructor(), QuestionResponse(), Question(), Survey(), SurveyResponse()]

    def setUpClass():
        logging.disable(logging.CRITICAL)
        initialize_db(db='test')
        # Designates Basemodel to use the test database
        BaseModel.DB = 'test'
        # Gives Basemodel a direct connection to the rethinkdb
        BaseModel.conn = r.connect(host='localhost', port=28015)
        return

    def get_app(self):
        return application

    def test_default_model_keys(self):
        for model in self.models:
            requiredFieldsSet = set(model.requiredFields())
            defaultKeysSet = set(model.default().keys())
            message = "model {0}.default() keys are not in requiredFields.".format(model.__class__.__name__)
            self.assertTrue(requiredFieldsSet.issubset(defaultKeysSet), message)

    def test_create_generic_item(self):
        for model in self.models:
            create_generic_item = getattr(model, "create_generic_item", None)
            if callable(create_generic_item):
                message = "model {0}.create_generic_item failed. If this method is implemented, it must pass.".format(model.__class__.__name__)
                self.assertTrue(type(create_generic_item()) == str, message)

    def tearDownClass():
        logging.disable(logging.NOTSET)


if __name__ == '__main__':
    unittest.main()
