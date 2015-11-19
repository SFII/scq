import tornado.web
from handlers.base_handler import BaseHandler
class LogoutHandler(BaseHandler):
    def get(self):
        self.clear_current_user_cookie()
        self.redirect(self.get_argument("next", "/"))
