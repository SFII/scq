import rethinkdb as r
import logging
import time
import services.culdapauth as culdapauth
from models.basemodel import BaseModel


class User(BaseModel):

    TESTING_PASSWORD = 't3sT1ng U$er P4ssw0rd'
    REGISTRATION_TESTING = 'registration_testing'
    REGISTRATION_CULDAP = 'registration_culdap'
    REGISTRATION_DENY = 'registration_deny'
    REGISTRATION_METHODS = [REGISTRATION_TESTING, REGISTRATION_CULDAP]
    NO_DISCLOSURE = 'Prefer Not to Disclose'
    USER_GENDERS = ['Male', 'Female', 'Other', NO_DISCLOSURE]
    USER_ETHNICITIES = ['American Indian or Alaska Native', 'Asian', 'Black or African American', 'Hispanic or Latino', 'Native Hawaiian or Other Pacific Islander', 'White', 'Other', NO_DISCLOSURE]
    USER_NATIVE_LANGUAGES = ['English', 'Spanish', 'French', 'German', 'Korean', 'Chinese', 'Japanese', 'Russian', 'Arabic', 'Portuguese', 'Hindi', 'Other', NO_DISCLOSURE]
    USER_PRIMARY_AFFILIATION = ['Student', 'Faculty', 'Both']
    USER_STATUS = ['Freshman', 'Sophomore', 'Junior', 'Senior']

    # must be overridden
    def requiredFields(self):
        return ['registration', 'username', 'email', 'accepted_tos', 'date_registered']

    # must be overrriden
    def fields(self):
        b = super(User, self)
        return {
            'registration': (b.is_in_list(self.REGISTRATION_METHODS),),
            'username': (b.is_string, b.is_not_empty,),
            'email': (b.is_string, b.is_valid_email, ),
            'accepted_tos': (b.is_truthy,),
            'gender': (b.is_in_list(self.USER_GENDERS),),
            'ethnicity': (b.is_in_list(self.USER_ETHNICITIES),),
            'native_language': (b.is_in_list(self.USER_NATIVE_LANGUAGES),),
            'date_registered': (b.is_timestamp,),
            'last_sign_in': (b.is_timestamp,),
            'subscribed_groups': (b.is_list,),
            'created_surveys': (b.is_list,),
            'unanswered_surveys': (b.is_list,),
            'answered_surveys': (b.is_list,),
            'survey_responses': (b.is_list,),
            'answers': (b.is_list,),
            'primary_affiliation': (b.is_string, b.is_in_list(self.USER_PRIMARY_AFFILIATION)),
            'status': (b.is_string, b.is_in_list(self.USER_STATUS)),
        }

    # returns default user data, that can be overwritten. Good for templating a new user
    # str(datetime.fromtimestamp(time.time()))
    def default(self):
        return {
            'registration': self.REGISTRATION_TESTING,
            'username': '',
            'email': '',
            'accepted_tos': True,
            'gender': self.USER_GENDERS[-1],
            'ethnicity': self.USER_ETHNICITIES[-1],
            'native_language': self.USER_NATIVE_LANGUAGES[-1],
            'date_registered': time.time(),
            'last_sign_in': time.time(),
            'subscribed_groups': [],
            'unanswered_surveys': [],
            'answered_surveys': [],
            'created_surveys': [],
            'survey_responses': [],
            'answers': [],
            'primary_affiliation': self.USER_PRIMARY_AFFILIATION[-1],
            'status': self.USER_STATUS[-1],
        }

    def create_generic_item(self):
        data = self.default()
        data = User().default()
        username = str(time.time())
        data['username'] = username
        data['accepted_tos'] = True
        data['email'] = 'xxx@colorado.edu'
        return self.create_item(data)

    def authenticate_test_user(self, username, password):
        return password == self.TESTING_PASSWORD

    def authenticate_deny(self, username, password):
        return False

    def authenticate(self, user_id, password):
        """
        Given user_id and possible password, lookup how to authenticate the user
        and attempt to authenticate the user
        returns True / False whether the authentication is successful
        """
        user_data = self.get_item(user_id)
        username = user_data['username']
        registration = user_data['registration']
        return {
            self.REGISTRATION_TESTING: self.authenticate_test_user,
            self.REGISTRATION_CULDAP: culdapauth.auth_user_ldap,
            self.REGISTRATION_DENY: self.authenticate_deny
        }[registration](username, password)
