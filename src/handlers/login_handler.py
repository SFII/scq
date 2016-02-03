import tornado.web
import logging
from models.user import User
from handlers.base_handler import BaseHandler

class LoginHandler(BaseHandler):

    def get(self):
        if self.current_user:
            return self.redirect(self.get_argument('next', '/dashboard'))
        return self.render('login.html', errors=[], next=self.get_argument('next', '/dashboard'))

    def post(self):
        username = self.get_argument('username')
        password = self.get_argument('password')
        cursor = User().find_item({'username' : username})
        for user_data in cursor:
            user_id = user_data['id']
            if User().authenticate(user_id, password):
                return self.login(user_data)
            else:
                return self.denied('User credentials are incorrect!')
        return self.denied('User credentials not found!')

    def login(self, user_data):
        self.set_current_user(user_data)
        self.redirect(self.get_argument('next', '/dashboard'))

    def denied(self, error):
        self.render(
            'login.html',
            errors=[error],
            next=self.get_argument('next', '/dashboard')
        )
