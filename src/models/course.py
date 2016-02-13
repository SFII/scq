from models.basemodel import BaseModel
import random
import logging


class Course(BaseModel):

    def requiredFields(self):
        return ['course_name', 'department', 'average_grade', 'credit_hours', 'active_surveys', 'inactive_surveys']

    def fields(self):
        return {
            'course_name': (self.is_string, self.is_not_empty,),
            'department': (self.is_string, ),
            'average_grade': (self.is_int, ),
            'credit_hours': (self.is_int, ),
            'active_surveys': (self.is_list, ),
            'inactive_surveys': (self.is_list,),
            'subscribers': (self.is_list,),
        }

    # returns default survey data, that can be overwritten. Good for templating a new user
    def default(self):
        return {
            'course_name': "",
            'department': "",
            'average_grade': 0,
            'credit_hours': 0,
            'active_surveys': [],
            'inactive_surveys': [],
            'subscribers': []
        }

    def subscribe_user(self, user_id, course_id):
        super(Course, self).subscribe_user(user_id, course_id, 'courses')
        course_data = self.get_item(course_id)
        for survey_id in course_data['active_surveys']:
            self.send_user_survey(user_id, survey_id)

    def create_generic_item(self):
        data = self.default()
        data['course_name'] = 'test_course'
        data['department'] = 'test_dept'
        data['average_grade'] = random.random() * 4
        return self.create_item(data)
