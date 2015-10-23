from basemodel import BaseModel

class Survey(BaseModel):

    def requiredFields():
        super + ['survey_id', 'question_id', 'course_id', 'user_id']

    def fields():
        super.update({
            'survey_id' : (is_int, ),
            'question_id' : (is_int, ),
            'course_id' : (is_int, ),
            'user_id' : (is_int, )
        })
