from models.basemodel import BaseModel
import time
import random
import logging
from models.user import User


class Group(BaseModel):

    def requiredFields(self):
        return ['id', 'active_surveys', 'inactive_surveys', 'subscribers']

    def fields(self):
        return {
            'id': (self.is_string, self.is_not_empty,),
            'creator_id': (self.is_string, self.is_not_empty,),
            'active_surveys': (self.is_list, ),
            'inactive_surveys': (self.is_list,),
            'subscribers': (self.is_list,),
        }

    def default(self):
        return {
            'id': '',
            'creator_id': '',
            'active_surveys': [],
            'inactive_surveys': [],
            'subscribers': []
        }

    def create_item(self, data, skip_verify=False):
        creator_id = data['creator_id']
        group_id = super(Group, self).create_item(data, skip_verify=skip_verify)
        if group_id is None:
            return None
        self.subscribe_user(creator_id, group_id)
        return group_id

    def subscribe_user(self, user_id, group_id):
        result = super(Group, self).subscribe_user(user_id, group_id, 'subscribed_groups')
        group_data = self.get_item(group_id)
        if group_data is None:
            message = "group_id {0} does not correspond to a value in the database".format(group_id)
            return logging.error(message)
        for survey_id in group_data.get('active_surveys', []):
            self.send_user_survey(user_id, survey_id)
        return result

    def unsubscribe_user(self, user_id, group_id):
        return super(Group, self).unsubscribe_user(user_id, group_id, 'subscribed_groups')

    def create_generic_item(self, user_id=None):
        data = self.default()
        if user_id is None:
            user_id = User().create_generic_item()
        data['id'] = str(time.time())
        data['creator_id'] = user_id
        return self.create_item(data)
