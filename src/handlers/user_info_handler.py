import tornado.web
from handlers.base_handler import BaseHandler
from models.user import User
from models.basemodel import BaseModel
from handlers.register.culdap_register_handler import CuLdapRegisterHandler

class UserInfoHandler(BaseHandler):

    def get(self, input=None):
        user_info_dict = self.current_user
        if user_info_dict:
            verified = User().verify(user_info_dict)
            if len(verified) != 0:
                logging.error('User: verification errors!')
                logging.error(verified)
                return self.verifyCULdapRegistrationPage(user_info_dict['username'], verified)
            return self.render('userinfo.html',
            errors = [],
            username = user_info_dict['username'],
            email = user_info_dict['email'],
            status = user_info_dict['status'],
            dob = user_info_dict['dob'],
            native_language = user_info_dict['native_language'],
            gender = user_info_dict['gender'],
            ethnicity = user_info_dict['ethnicity'],
            major1 = user_info_dict['major1'],
            major2 = user_info_dict['major2'],
            major3 = user_info_dict['major3'],
            major4 = user_info_dict['major4'],
            minor1 = user_info_dict['minor1'],
            minor2 = user_info_dict['minor2'],
            departments = user_info_dict['departments'],
            courses = user_info_dict['courses'],
            primary_affiliation = user_info_dict['primary_affiliation'],
            next = self.get_argument("next","/edituserinfo"))
        return self.render('login.html', errors=[], next=self.get_argument('next','/dashboard'))
