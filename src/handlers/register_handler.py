import tornado.web
from models.user import User
from handlers.base_handler import BaseHandler

class RegisterHandler(BaseHandler):

    # Mandatories: Name, Universty email, password, confirm password, group (student...), accept term and conditions
    # Not mandatories: date, birthday, phone number, location, gender, ethnicity, native language

    def get(self, input=None):
        return self.render("register.html", errors=[], next=self.get_argument("next","/"))


    def post(self, input=None):
        return self.registerDefault()

    def getErrors(self):
        errors = []
        username = self.get_argument('username',None,strip = True)
        password = self.get_argument('password',None,strip = True)
        accepted = self.get_argument('accept',None,strip = True)
        if username is None:
            errors.append('username is required')
        if password is None:
            errors.append('password is required')
        if not accepted:
            errors.append('you must accept the Terms and Conditions to Register')
        return errors


    def registerDefault(self):
        errors = self.getErrors()
        return self.render(
            'register.html',
            errors=errors,
            next=self.get_argument("next","/")
        )

    def failWithErrors(self,page='register.html',errors=['Something went wrong.']):
        return self.render(
            page,
            errors=errors,
            next=self.get_argument("next","/")
        )

    def getLdapUser(self, username, registration):
        user = User().find({'username' : username, 'registration' : registration})
