from models.basemodel import BaseModel
from models.course import Course

class Survey(BaseModel):

    def requiredFields(self):
        return ['question_id', 'course_id', 'creator_id']

    def fields():
        b = super(Survey, self)
        return {
            'survey_id' : (b.is_string, b.is_not_empty,),
            'questions' : (b.is_list, schema_list_check(b.is_string)),
            'course_id' : (b.is_string, b.is_not_empty,),
            'creator_id' : (b.is_string, b.is_not_empty,)
        }

    def create_item(self, data):
        survey_id = super(Survey, self).create_item(data)
        course_id = data['course_id']
        course_data = Course().get_item(course_id)
        active_surveys = course_data['active_surveys']
        active_surveys.append(survey_id)
        subscribers = course_data['subscribers']
        Course().update_item(course_id, {'active_surveys' : active_surveys })
        for subscriber_id in subscribers:
            self.send_user_survey(subscriber_id, survey_id)


    # returns default survey data, that can be overwritten. Good for templating a new user
    def default(self):
        return {
            'questions' : [],
            'course_id' : "",
            'creator_id' : ""
        }
