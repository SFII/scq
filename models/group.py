from models.basemodel import BaseModel
import time
import random
import logging
from models.user import User
import rethinkdb as r


class Group(BaseModel):

    def requiredFields(self):
        return ['id', 'active_surveys', 'inactive_surveys', 'subscribers', 'tags']

    def fields(self):
        return {
            'id': (self.is_string, self.is_not_empty,),
            'creator_id': (self.is_string, self.is_not_empty,),
            'active_surveys': (self.is_list, ),
            'inactive_surveys': (self.is_list,),
            'subscribers': (self.is_list,),
            'tags': (self.is_list, self.schema_list_check(self.is_string,),),
        }

    def default(self):
        return {
            'id': '',
            'creator_id': '',
            'active_surveys': [],
            'inactive_surveys': [],
            'subscribers': [],
            'penders': [],
            'tags': []
        }

    def create_item(self, data, skip_verify=False):
        creator_id = data['creator_id']
        group_id = super(Group, self).create_item(data, skip_verify=skip_verify)
        if group_id is None:
            return None
        self.subscribe_user(creator_id, group_id)
        return group_id

    def subscribe_user(self, user_id, group_id):
        # TODO: edit this method. Need to add another parameter to see if an actual
        # id is being passed or if a username is passed instead.
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

    def remove_pending_user(self, user_id, group_id):
        return super(Group, self).remove_pending_user(user_id, group_id, 'pending_groups')

    def create_generic_item(self, user_id=None):
        data = self.default()
        if user_id is None:
            user_id = User().create_generic_item()
        data['id'] = str(time.time())
        data['creator_id'] = user_id
        return self.create_item(data)

    def popular_groups(self):
        results = r.db(self.DB).table('Group').order_by(lambda group: group['subscribers'].count()).limit(10)["id"].run(self.conn)
        return list(results)

    def relevant_groups(self, user):
        results = []
        for major in user['majors']:
            results.append(self.get_item(major)['id'])

        for minor in user['minors']:
            results.append(self.get_item(minor)['id'])

        return list(results)
