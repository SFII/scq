import tornado.web
import logging
from models.user import User

class LoginHandler(tornado.web.RequestHandler):

    def get(self):
        self.render("login.html", errormessage='', next=self.get_argument("next","/"))

    def post(self):
        username = self.get_argument('username',strip = True)
        password = self.get_argument('password',strip = True)
        user = User().get({'username' : username})
        if user is None:
            return self.render(
                'login.html',
                errormessage="User credentials not found!",
                next=self.get_argument("next","/")
            )
        else:
            print(user)
            if User().authenticate(username, password):
                return __login(user)
            else:
                return self.render(
                    'login.html',
                    errormessage="User credentials are incorrect!",
                    next=self.get_argument("next","/")
                )

    def __login(self, user):
        self.__set_current_user(user)
        self.redirect(self.get_argument("next", "/"))

    def __set_current_user(self, user):
        if user:
            self.set_secure_cookie("user", tornado.escape.json_encode(user))
        else:
            self.clear_cookie("user")
