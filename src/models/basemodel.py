import rethinkdb as r
import re
import time
from datetime import datetime
import tornado.gen as gen
from tornado.options import options, define
import logging


class BaseModel:
    conn = None
    DB = 'scq'

    def is_int(self, data):
        assert data is not True, "value '{0}' Must be a number".format(data)
        assert data is not False, "value '{0}' Must be a number".format(data)
        assert isinstance(data, (int, float)), "value '{0}' Must be a number".format(data)

    def is_truthy(self, data):
        assert (data and True), "data '{0}' Must be Truthy".format(data)

    def is_falsey(self, data):
        assert not (data or False), "data '{0}' Must be Falsey".format(data)

    def is_not_empty(self, data):
        assert (len(data) != 0), "data '{0}' Must not be empty".format(data)

    def is_timestamp(self, data):
        self.is_int(data)
        assert data >= 0, "timestamp '{0}' is negative:".format(data)
        try:
            datetime.fromtimestamp(data)
        except Exception as e:
            raise AssertionError("timestamp '{0}' could not be parsed into date object:".format(data))

    def is_string(self, data):
        assert isinstance(data, (str,)), "value '{0}' Must be a string".format(data)

    def is_valid_email(self, data):
        assert re.match(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$", data) is not None, "Must be a valid email address"

    def is_list(self, data):
        assert isinstance(data, (list, tuple)), "data '{0}' Must be a list".format(data)

    def is_unique(self, data, key):
        def _unique(data):
            assert len(self.find({key: data})) == 0, "data '{0}' Must must be a unique value in the database with respect to key {1}".format(data, key)
        return _unique

    def is_none(self, data):
        assert data is None, "Must be empty"

    def is_in_list(self, alias=[]):
        def _in_list(data):
            assert data in alias, "Must be in {}".format(alias)
        return _in_list

    def is_in_range(self, low, high=None):
        def _in_range(data):
            if high is None:
                assert low <= data, "Must be larger than {}".format(low)
            else:
                assert low <= data <= high, "Must be between {} and {}".format(low, high)
        return _in_range

    def schema_recurse(self, fields, required_fields=[]):
        def _recurse(data):
            errors = list(check_data(data, fields, required_fields))
            if errors:
                raise Exception(errors)
        return _recurse

    def schema_or(self, method_a, method_b):
        def _or(data):
            try:
                method_a(data)
            except Exception as exa:
                try:
                    method_b(data)
                except Exception as exb:
                    raise AssertionError("Must be one of the following:\n\t {}\n or\n\t {}".format(exa, exb))
        return _or

    def requiredFields(self):
        return []

    def strictSchema(self):
        return False

    def init(self, DB, conn):
        table = self.__class__.__name__
        try:
            r.db(DB).table_create(table).run(conn)
        except:
            pass

    def get_item(self, idnum):
        table = self.__class__.__name__
        return r.db(BaseModel.DB).table(table).get(idnum).run(BaseModel.conn)

    def update_item(self, idnum, data):
        table = self.__class__.__name__
        return r.db(BaseModel.DB).table(table).get(idnum).update(data).run(BaseModel.conn)

    def subscribe_user(self, user_id, row_id, user_subscription_name=None):
        """
        adds a user id to a model's subscription list.
        """
        row_table = self.__class__.__name__
        user_table = 'User'
        user_data = r.db(BaseModel.DB).table(user_table).get(user_id).run(BaseModel.conn)
        row_data = r.db(BaseModel.DB).table(row_table).get(row_id).run(BaseModel.conn)
        if user_data is None:
            logging.error("User {0} does not exist".format(user_data))
            return False
        if user_data is None:
            logging.error("{0} {1} does not exist".format(table, row_data))
            return False
        try:
            if user_subscription_name is not None:
                user_subscription = user_data[user_subscription_name]
                user_subscription.append(row_id)
                r.db(BaseModel.DB).table(user_table).get(user_id).update({user_subscription_name: user_subscription}).run(BaseModel.conn)
        except KeyError:
            logging.error("user subscription {0} not known in user data".format(user_subscription_name))
            return False
        subscribers = row_data['subscribers']
        subscribers.append(user_id)
        return r.db(BaseModel.DB).table(row_table).get(row_id).update({'subscribers': subscribers}).run(BaseModel.conn)

    # adds a survey_id to a user's unanswered_surveys list.
    # maybe this should live somewhere else? like user? or survey?
    def send_user_survey(self, user_id, survey_id, survey_key='unanswered_surveys'):
        survey_table = 'Survey'
        user_table = 'User'
        user_data = r.db(BaseModel.DB).table(user_table).get(user_id).run(BaseModel.conn)
        survey_data = r.db(BaseModel.DB).table(survey_table).get(survey_id).run(BaseModel.conn)
        if user_data is None:
            logging.error("User {0} does not exist".format(user_data))
            return False
        if survey_data is None:
            logging.error("Survey {0} does not exist".format(survey_data))
            return False
        try:
            user_survey_list = user_data[survey_key]
        except KeyError:
            logging.error("survey key {0} not known in user data".format(survey_key))
            return False
        user_survey_list.append(survey_id)
        return r.db(BaseModel.DB).table(user_table).get(user_id).update({survey_key: user_survey_list}).run(BaseModel.conn)

    def find(self, key):
        table = self.__class__.__name__
        return list(r.db(BaseModel.DB).table(table).filter(key).run(BaseModel.conn))

    # create a new database item from given data, if the data passes the validator
    def create_item(self, data):
        table = self.__class__.__name__
        verified = self.verify(data)
        if len(verified) == 0:
            o = r.db(BaseModel.DB).table(table).insert(data).run(BaseModel.conn)
            return o['generated_keys'][0]
        logging.error(verified)
        return None

    def delete_item(self, item_id):
        table = self.__class__.__name__
        return r.db(BaseModel.DB).table(table).get(item_id).delete().run(BaseModel.conn)

    def schema_list_check(self, method):
        def _list_check(data):
            try:
                all(method(d) for d in data)
            except Exception as e:
                raise AssertionError("Not all elements satisfy:\n\t {}".format(e))
        return _list_check

    def check_data(data, fields, required_fields=[]):
        for field in required_fields:
            if field not in data:
                yield (field, 'Missing field: {}'.format(field))
        for key, methods in fields.items():
            if key in data:
                for method in methods:
                    try:
                        if method in [BaseModel.is_unique]:
                            method(data[key], key)
                        else:
                            method(data[key])
                    except Exception as e:
                        if isinstance(getattr(e, 'message', None), (list, tuple)):
                            for error in e.message:
                                yield error
                        else:
                            yield (key, "{}: {}".format(key, e))

    def verify(self, data):
        return list(BaseModel.check_data(data, self.fields(), self.requiredFields()))

    def get_all(self):
        table = self.__class__.__name__
        return list(r.db(BaseModel.DB).table(table).run(BaseModel.conn))
