import tornado.web
from handlers.base_handler import BaseHandler


class AbuseHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render('abuse.html')
