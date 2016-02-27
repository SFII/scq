from models.basemodel import BaseModel
import time
import random
import logging


class Group(BaseModel):

    def requiredFields(self):
        return ['name', 'active_surveys', 'inactive_surveys', 'subscribers']

    def fields(self):
        return {
            'name': (self.is_string, self.is_not_empty,),
            'active_surveys': (self.is_list, ),
            'inactive_surveys': (self.is_list,),
            'subscribers': (self.is_list,),
        }

    def default(self):
        return {
            'name': "",
            'active_surveys': [],
            'inactive_surveys': [],
            'subscribers': []
        }

    def subscribe_user(self, user_id, course_id):
        self.subscribe_user(user_id, course_id, 'courses')
        course_data = self.get_item(course_id)
        for survey_id in course_data['active_surveys']:
            self.send_user_survey(user_id, survey_id)

    def create_generic_item(self):
        data = self.default()
        data['name'] = time.time()
        return self.create_item(data)
