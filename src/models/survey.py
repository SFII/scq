from models.basemodel import BaseModel

class Survey(BaseModel):

    def requiredFields():
        return ['question_id', 'course_id', 'creator_id']

    def fields():
        b = super(User, self)
        return {
            'survey_id' : (b.is_string, ),
            'questions' : (b.is_list, schema_list_check(b.is_string)),
            'course_id' : (b.is_string, ),
            'creator_id' : (b.is_string, )
        }
