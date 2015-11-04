from models.basemodel import BaseModel

class Survey(BaseModel):

    def requiredFields():
        return ['question_id', 'course_id', 'user_id']

    def fields():
        b = super(User, self)
        return {
            'survey_id' : (is_int, ),
            'question_id' : (is_int, ),
            'course_id' : (is_int, ),
            'user_id' : (is_int, )
        }
