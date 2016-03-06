import tornado.web
from handlers.base_handler import BaseHandler
from models.course import Course
from models.user import User
import logging


class ProfileHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):
        self.refresh_current_user_cookie()
        self.render('profile.html', extra_info_json=self.get_extra_info(), user_info_json=self.get_user_info())

    def post(self):
        pass

    def get_extra_info(self):
        extra_info_json = []
        extra_dict = {
            'gender': User.USER_GENDERS,
            'primary_affiliation': User.USER_PRIMARY_AFFILIATION,
            'ethnicity': User.USER_ETHNICITIES,
            'native_language': User.USER_NATIVE_LANGUAGES,
            'status': User.USER_STATUS
        }
        extra_info_json.append(extra_dict)
        logging.info("SUNG LOOK {0}".format(extra_info_json))
        return tornado.escape.json_encode(extra_info_json)

    def get_user_info(self):
        user_info_json = []
        user_data = self.current_user
        user_info_json.append(user_data)
        logging.info(tornado.escape.json_encode(user_info_json))
        return tornado.escape.json_encode(user_info_json)
