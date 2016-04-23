import unittest
import tornado.testing
import tornado.web
import time
from test.test_runner import BaseAsyncTest
from models.question import Question
from models.question_response import QuestionResponse
from models.survey import Survey
from models.survey_response import SurveyResponse
from models.user import User
from models.group import Group
import rethinkdb as r
import logging


class TestModels(BaseAsyncTest):
    models = [Group(), User(), QuestionResponse(), Question(), Survey(), SurveyResponse()]

    def setUpClass():
        # logging.disable(logging.CRITICAL)
        return

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
                message = "model {0}.create_generic_item failed. If this method is implemented, it must pass verification".format(model.__class__.__name__)
                self.assertTrue(type(create_generic_item()) == str, message)

    def tearDownClass():
        logging.disable(logging.NOTSET)


if __name__ == '__main__':
    unittest.main()
