from models.basemodel import BaseModel
from models.course import Course
from models.user import User
from models.question import Question
import random

class Survey(BaseModel):

    def requiredFields(self):
        return ['questions', 'course_id', 'creator_id', 'course_name', 'creator_name']

    def fields(self):
        b = super(Survey, self)
        return {
            'questions' : (b.is_list, ),
            'survey_id' : (b.is_string, b.is_not_empty,),
            'questions' : (b.is_list, self.schema_list_check(b.is_string)),
            'course_id' : (b.is_string, b.is_not_empty,),
            'course_name' : (b.is_string, b.is_not_empty,),
            'creator_id' : (b.is_string, b.is_not_empty,),
            'creator_name' : (b.is_string, b.is_not_empty,)
        }

    def create_item(self, data):
        print(data)
        course_id = data['course_id']
        creator_id = data['creator_id']
        creator_data = User().get_item(creator_id)
        course_data = Course().get_item(course_id)
        data['course_name'] = course_data['course_name']
        data['creator_name'] = creator_data['username']
        survey_id = super(Survey, self).create_item(data)
        active_surveys = course_data['active_surveys']
        active_surveys.append(survey_id)
        subscribers = course_data['subscribers']
        Course().update_item(course_id, {'active_surveys' : active_surveys })
        self.send_user_survey(creator_id, survey_id, 'created_surveys')
        for subscriber_id in subscribers:
            self.send_user_survey(subscriber_id, survey_id)
        return survey_id


    # returns default survey data, that can be overwritten. Good for templating a new user
    def default(self):
        return {
            'questions' : [],
            'course_id' : "",
            'creator_id' : "",
            'course_name' : "",
            'creator_name' : ""
        }

    def create_generic_item(self, creator_id, course_id=None):
        data = self.default()
        data['course_id'] = course_id if course_id else Course().create_generic_item()
        data['creator_id'] = creator_id
        for i in range(4):
            data['questions'].append(Question().create_generic_item())
        return self.create_item(data)

    def decompose(self, survey_id):
        survey_data = self.get_item(survey_id)
        decomposed_data = survey_data.copy()
        decomposed_question_data = []
        question_ids = survey_data['questions']
        for question_id in question_ids:
            question_data = Question().get_item(question_id)
            decomposed_question_data.append(question_data)
        decomposed_data['questions'] = decomposed_question_data
        return decomposed_data
