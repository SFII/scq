import tornado.web
import tornado.gen as gen
import json
import time
from models.survey import Survey
from models.user import User
import models.answer

class Survey(tornado.web.RequestHandler):
    def get(self, idnumber):
        idnumber = int(idnumber)
        data = models.survey.Survey().get_item(idnumber)
        if data == None:
            self.write_error(404)
        else:
            self.write(json.dumps(data))

    def post(self, idnumber):
        idnumber = int(idnumber)
        body = self.request.body.decode("utf-8")
        data = json.loads(body)
        models.answer.Answer().create_item(data)

class Surveys(tornado.web.RequestHandler):
    def post(self):
        body = self.request.body.decode("utf-8")
        data = json.loads(body)
        models.survey.Survey().create_item(data)

    def get(self):
        uid = self.get_secure_cookie("username")
        user = User().get_item(uid)
        classes = user['courses']
        for course in courses:
            data += models.survey.Survey().find({'course': course,})
        self.write(json.dumps(data))
