from models.basemodel import BaseModel

class Survey(BaseModel):

    def requiredFields():
        return ['question_id', 'course_id', 'user_id']

    def fields():
        b = super(User, self)
        return {
            'survey_id' : (b.is_string, ),
            'question_id' : (b.is_int, ),
            'course_id' : (b.is_int, ),
            'user_id' : (b.is_int, )
        }
