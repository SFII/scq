import tornado.web
import logging
from models.user import User

class LoginHandler(tornado.web.RequestHandler):

    def get(self):
        self.render("login.html", errormessage='', next=self.get_argument("next","/"))

    def post(self):
        username = self.get_argument('username',strip = True)
        password = self.get_argument('password',strip = True)
        cursor = User().find({'username' : username})
        for user in cursor:
            logging.info(user)
            if user is None:
                return self.render(
                    'login.html',
                    errormessage="User credentials not found!",
                    next=self.get_argument("next","/")
                )
            else:
                user_id = user['id']
                if User().authenticate(user_id, password):
                    return login(user)
                else:
                    return self.render(
                        'login.html',
                        errormessage="User credentials are incorrect!",
                        next=self.get_argument("next","/")
                    )

    def login(self, user_id):
        self.set_current_user(user_id)
        self.redirect(self.get_argument("next", "/"))

    def set_current_user(self, user_id):
        if user_id:
            self.set_secure_cookie("user", tornado.escape.json_encode(user_id))
        else:
            self.clear_cookie("user")
