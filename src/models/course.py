from models.basemodel import BaseModel
import random

class Course(BaseModel):

    def requiredFields(self):
        return ['course_name', 'department', 'average_grade', 'credit_hours', 'active_surveys', 'inactive_surveys']

    def fields(self):
        b = super(Course, self)
        return {
            'course_name' : (b.is_string, b.is_not_empty,),
            'department' : (b.is_string, ),
            'average_grade' : (b.is_int, ),
            'credit_hours' : (b.is_int, ),
            'active_surveys' : (b.is_list, ),
            'inactive_surveys' : (b.is_list,),
            'subscribers' : (b.is_list,),
        }

    # returns default survey data, that can be overwritten. Good for templating a new user
    def default(self):
        return {
            'course_name' : "",
            'department' : "",
            'average_grade' : 0,
            'credit_hours' : 0,
            'active_surveys' : [],
            'inactive_surveys' : [],
            'subscribers' : []
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
        return super(Course, self).create_item(data)
