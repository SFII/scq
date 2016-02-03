import tornado.web
from handlers.base_handler import BaseHandler
from models.user import User
from models.basemodel import BaseModel

class UserInfoUpdateHandler(BaseHandler):

    def get(self, input=None, errors=[]):
        user_info_dict = self.current_user
        verified = User().verify(user_info_dict)
        if len(verified) != 0:
            logging.error('User: verification errors!')
            logging.error(verified)
            return self.verifyCULdapRegistrationPage(user_info_dict['username'], verified)
        username = user_info_dict['username']
        email = user_info_dict['email']
        status = user_info_dict['status']
        dob = user_info_dict['dob']
        major1 = user_info_dict['major1']
        major2 = user_info_dict['major2']
        major3 = user_info_dict['major3']
        major4 = user_info_dict['major4']
        minor1 = user_info_dict['minor1']
        minor2 = user_info_dict['minor2']
        courses = user_info_dict['courses']
        if len(courses) == 0:
            courses = ['']
        departments = user_info_dict['departments']
        primary_affiliation = user_info_dict['primary_affiliation']
        self.render('userupdate.html',
        errors=errors,
        next=self.get_argument("next","/"),
        user_genders=User().USER_GENDERS,
        user_ethnicities=User().USER_ETHNICITIES,
        user_native_languages=User().USER_NATIVE_LANGUAGES,
        email = email,
        username = username,
        dob= self.get_argument('dob','%s' %dob,strip = True),
        gender= self.get_argument('gender','',strip = True),
        ethnicity= self.get_argument('ethnicity','',strip = True),
        native_language= self.get_argument('native_language','',strip = True),
        status= self.get_argument('status','%s'%status,strip = True),
        major1= self.get_argument('major1','%s'%major1,strip = True),
        major2= self.get_argument('major2','%s'%major2,strip = True),
        major3= self.get_argument('major3','%s'%major3,strip = True),
        major4= self.get_argument('major4','%s'%major4,strip = True),
        minor1= self.get_argument('minor1','%s'%minor1,strip = True),
        minor2= self.get_argument('minor2','%s'%minor2,strip = True),
        courses = self.get_argument('courses', '%s'%courses,strip = True),
        departments = self.get_argument('departments', '%s'%departments, strip = True),
        primary_affiliation = self.get_argument('primary_affiliation', '%s'%primary_affiliation,strip = True)
        )

    def post(self):
        data = User().default()
        data['username'] = self.current_user['username']
        data['email']           = self.get_argument('email',None,strip = True)
        data['dob']             = self.get_argument('dob',None,strip = True)
        data['gender']          = self.get_argument('gender',None,strip = True)
        data['ethnicity']       = self.get_argument('ethnicity',None,strip = True)
        data['native_language'] = self.get_argument('native_language',None,strip = True)
        data['status']          = self.get_argument('status',None,strip = True)
        data['major1']          = self.get_argument('major1',None,strip = True)
        data['major2']          = self.get_argument('major2',None,strip = True)
        data['major3']          = self.get_argument('major3',None,strip = True)
        data['major4']          = self.get_argument('major4',None,strip = True)
        data['minor1']          = self.get_argument('minor1',None,strip = True)
        data['minor2']          = self.get_argument('minor2',None,strip = True)
        data['courses']         = self.get_arguments('courses',strip = True)
        data['departments']     = self.get_arguments('departments',strip = True)
        data['primary_affiliation'] = self.get_arguments('primary_affiliation',strip = True)
        User().verify(data)
        User().update_item(self.current_user['id'], data)
        return self.redirect(self.get_argument("next", "/dashboard"))
