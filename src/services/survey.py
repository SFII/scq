import tornado.web
import tornado.gen as gen
import json
import time
import models.survey
import models.answer

class Survey(tornado.web.RequestHandler):
    def get(self, idnumber):
        idnumber = int(idnumber)
        data = models.survey.Survey().get_item(idnumber)
        # This is necessary because tornado has a runtime assert that
        # coroutines only return futures, and coroutines can't yield
        # and return, so we must double yield here, unless someone
        # figures out a better way.
        if data == None:
            self.write_error(404)
            return
        self.write(json.dumps(data))

    def post(self, idnumber):
        idnumber = int(idnumber)
        body = self.request.body.decode("utf-8")
        data = json.loads(body)
        yield models.answer.Answer().create_item(data)

class Surveys(tornado.web.RequestHandler):
    def post(self):
        body = self.request.body.decode("utf-8")
        data = json.loads(body)
        models.survey.Survey().create_item(data)