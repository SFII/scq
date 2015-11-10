import tornado.web
import tornado.gen as gen
import json
import models.survey
import models.answer

class Survey(tornado.web.RequestHandler):
    @gen.coroutine
    def get(self, survey_id):
        data = yield models.survey.Survey().get_item(str(survey_id))
        # This is necessary because tornado has a runtime assert that
        # coroutines only return futures, and coroutines can't yield
        # and return, so we must double yield here, unless someone
        # figures out a better way.
        data = yield data
        if data == None:
            self.write_error(404)
            return
        self.write(json.dumps(data))

    @gen.coroutine
    def post(self):
        body = self.request.body
        data = json.loads(body)
        yield models.answer.Answer().create_item(data)

class Surveys(tornado.web.RequestHandler):
    @gen.coroutine
    def post(self):
        body = self.request.body
        data = json.loads(body)
        yield models.survey.Survey().create_item(data)