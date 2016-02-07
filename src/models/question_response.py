from models.basemodel import BaseModel
from models.course import Course
from models.user import User
from models.question import Question
import random


class QuestionResponse(BaseModel):

    def requiredFields(self):
        return ['response_data', 'question_id', 'response_format']

    def strictSchema(self):
        return True

    def fields(self):
        return {
            'response_format': (self.is_string, self.is_in_list(Question().USER_RESPONSE_FORMAT),),
            'question_id': (self.is_string, self.is_not_empty, self.exists_in_table('Question'),),
            'response_data': (self.is_not_none, )
        }

    def create_batch(self, batch_data, skip_verify=False):
        """
        Given batch data, creates a new database item for each value in batch_data
        Returns an array of ids of the created items if they all pass verification
        otherwise returns None
        """
        table = self.__class__.__name__
        if not skip_verify:
            for data in batch_data:
                verified = self.verify(data)
                if len(verified):
                    logging.error("Verification errors: {0}".format(verified))
                    return None
        result = r.db(BaseModel.DB).table(table).insert(data).run(BaseModel.conn)
        return result['generated_keys']
