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
        data = User().default()
        data['username'] = self.current_user['username']
        data['email'] = self.get_argument('email', None, strip=True)
        data['dob'] = self.get_argument('dob', None, strip=True)
        data['gender'] = self.get_argument('gender', None, strip=True)
        data['ethnicity'] = self.get_argument('ethnicity', None, strip=True)
        data['native_language'] = self.get_argument('native_language', None, strip=True)
        data['status'] = self.get_argument('status', '', strip=True)
        data['primary_affiliation'] = (self.get_argument('primary_affiliation', None, strip=True))
        data['subscribed_groups'] = self.get_argument('subscribed_groups', None, strip=True)
        if (data['subscribed_groups'] is None):
            data['courses'] = []
        else:
            data['subscribed_groups'] = (self.get_argument('subscribed_groups', None, strip=True)).replace(' ', '').split(',')
        verified = User().verify(data)
        if len(verified) != 0:
            logging.error('User: verification errors in user update page!')
            logging.error(verified)
            return self.redirect(self.get_argument("/profile"))
        User().update_item(self.current_user['id'], data)
        return self.redirect(self.get_argument("next", "/dashboard"))

    def get_extra_info(self):
        user_data = self.current_user
        extra_info_json = []
        extra_dict = {
            'gender': User.USER_GENDERS,
            'primary_affiliation': User.USER_PRIMARY_AFFILIATION,
            'ethnicity': User.USER_ETHNICITIES,
            'native_language': User.USER_NATIVE_LANGUAGES,
            'status': User.USER_STATUS
        }
        if (user_data['gender'] in extra_dict['gender']):
            extra_dict['gender'].remove(user_data['gender'])
        if (user_data['primary_affiliation'] in extra_dict['primary_affiliation']):
            extra_dict['primary_affiliation'].remove(user_data['primary_affiliation'])
        if (user_data['ethnicity'] in extra_dict['ethnicity']):
            extra_dict['ethnicity'].remove(user_data['ethnicity'])
        if (user_data['native_language'] in extra_dict['native_language']):
            extra_dict['native_language'].remove(user_data['native_language'])
        if (user_data['status'] in extra_dict['status']):
            extra_dict['status'].remove(user_data['status'])
        extra_info_json.append(extra_dict)
        return tornado.escape.json_encode(extra_info_json)

    def get_user_info(self):
        user_info_json = []
        user_data = self.current_user
        user_info_json.append(user_data)
        logging.info(tornado.escape.json_encode(user_info_json))
        return tornado.escape.json_encode(user_info_json)
