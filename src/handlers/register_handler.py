import tornado.web
from models.user import User

class RegisterHandler(tornado.web.RequestHandler):

    # Mandatories: Name, Universty email, password, confirm password, group (student...), accept term and conditions
    # Not mandatories: date, birthday, phone number, location, gender, ethnicity, native language

    def get(self, input=None):
        return self.render("register.html", errors=[], next=self.get_argument("next","/"))


    def post(self, input=None):
        return self.__registerDefault()

    def getErrors(self):
        errors = []
        username = self.get_argument('username',None,strip = True)
        password = self.get_argument('password',None,strip = True)
        confirmpassword = self.get_argument('passwordconfirm',None,strip = True)
        accepted = self.get_argument('accept',None,strip = True)
        if username is None:
            errors.append('username is required')
        if password is None:
            errors.append('password is required')
        if confirmpassword is None:
            errors.append('password confirmation is required')
        if password != confirmpassword:
            errors.append('passwords do not match')
        if not accepted:
            errors.append('you must accept the Terms and Conditions to Register')
        return errors


    def __registerDefault(self):
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


    def __login(self, user):
        self.set_secure_cookie("username", self.get_argument("username"))
        self.redirect(self.get_argument("next", "/"))

    def getLdapUser(self, username, registration):
        user = User().find({'username' : username, 'registration' : registration})
