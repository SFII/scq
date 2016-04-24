import tornado.web
from handlers.base_handler import BaseHandler, refresh_user_cookie_callback
from models.course import Course
from models.user import User
import logging


class ProfileHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):
        self.refresh_current_user_cookie()
        self.render('profile.html', extra_info_json=self.get_extra_info(), user_info_json=self.get_user_info())

    def post(self):
        self.refresh_current_user_cookie()
        user_data = self.current_user
        data = User().default()
        data['username'] = self.current_user['username']
        data['email'] = self.get_argument('email', None, strip=True)
        data['dob'] = self.get_argument('dob', None, strip=True)
        data['gender'] = self.get_argument('gender', None, strip=True)
        data['ethnicity'] = self.get_argument('ethnicity', None, strip=True)
        data['native_language'] = self.get_argument('native_language', None, strip=True)
        data['status'] = self.get_argument('status', '', strip=True)
        data['primary_affiliation'] = (self.get_argument('primary_affiliation', None, strip=True))
        data['subscribed_groups'] = self.current_user['subscribed_groups']
        data['pending_groups'] = self.current_user['pending_groups']
        data['answered_surveys'] = self.current_user['answered_surveys']
        data['answers'] = self.current_user['answers']
        data['unanswered_surveys'] = self.current_user['unanswered_surveys']
        data['created_surveys'] = self.current_user['created_surveys']
        data['survey_responses'] = self.current_user['survey_responses']
        '''
        if (data['subscribed_groups'] is None):
            data['subscribed_groups'] = []
        else:
            data['subscribed_groups'] = (self.get_argument('subscribed_groups', None, strip=True)).replace(' ', '').split(',')
        '''
        if data['status'] == '':
            data['status'] = user_data['status'] or "Freshman"
        data['status'] = self.get_argument('status', '', strip=True)
        data['major1'] = self.get_argument('major1', None, strip=True)
        data['major2'] = self.get_argument('major2', None, strip=True)
        data['major3'] = self.get_argument('major3', None, strip=True)
        data['major4'] = self.get_argument('major4', None, strip=True)
        data['minor1'] = self.get_argument('minor1', None, strip=True)
        data['minor2'] = self.get_argument('minor2', None, strip=True)
        # put majors and minors into one list each
        preData = {}
        preData['majors'] = [data['major1'], data['major2'], data['major3'], data['major4']]
        preData['minors'] = [data['minor1'], data['minor2']]
        # delete individual entries of majors
        del data['major1'], data['major2'], data['major3'], data['major4'], data['minor1'], data['minor2']
        majors = []
        minors = []
        # create arrays we're going to index
        for i in preData['majors']:
            if i != '':
                majors.append(i)
        for i in preData['minors']:
            if i != '':
                minors.append(i)
        # finish indexing
        data['majors'] = majors
        data['minors'] = minors
        verified = User().verify(data)
        if len(verified) != 0:
            logging.error('User: verification errors in POST profile page!')
            logging.error(verified)
            return self.redirect(self.get_argument("next", "/dashboard"))
        User().update_item(self.current_user['id'], data)
        self.refresh_current_user_cookie()
        return self.redirect(self.get_argument("next", "/profile"))

    def get_extra_info(self):
        extra_dict = {
            'gender': User.USER_GENDERS,
            'primary_affiliation': User.USER_PRIMARY_AFFILIATION,
            'ethnicity': User.USER_ETHNICITIES,
            'native_language': User.USER_NATIVE_LANGUAGES,
            'status': User.USER_STATUS
        }
        user_data = self.current_user
        extra_info_json = []
        extra_info_json.append(extra_dict)
        return tornado.escape.json_encode(extra_info_json)

    def get_user_info(self):
        user_info_json = []
        user_data = self.current_user
        user_info_json.append(user_data)
        logging.info(tornado.escape.json_encode(user_info_json))
        return tornado.escape.json_encode(user_info_json)
