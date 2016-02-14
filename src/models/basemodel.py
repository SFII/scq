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

    def is_unique(self, key):
        def _unique(data):
            value = data[key]
            assert len(self.find_item({key: value})) == 0, "data '{0}' Must must be a unique value in the database with respect to key {1}".format(data, key)
        return _unique

    def exists_in_table(self, table):
        def _exists(data):
            assert r.db(BaseModel.DB).table(table).get(data).run(BaseModel.conn) is not None, "id '{0}' does not exist in table {1}".format(data, table)
        return _exists

    def is_none(self, data):
        assert data is None, "Must be empty"

    def is_not_none(self, data):
        assert data is not None, "Must not be empty"

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
                    raise AssertionError("Must be one of the following: {}\n or {}".format(exa, exb))
        return _or

    def requiredFields(self):
        return []

    def strictSchema(self):
        return False

    def default(self):
        return {}

    def init(self, DB, conn):
        """
        Initializes a new Table in the database, named after the model that calls it.
        """
        table = self.__class__.__name__
        try:
            r.db(DB).table_create(table).run(conn)
        except:
            pass

    def drop(self, DB, conn):
        """
        Drops the table in the rethink database that corresponds with the model that called it.
        This will wipe all data in that table, and drop the table from the db
        """
        table = self.__class__.__name__
        try:
            r.db(DB).table_drop(table).run(conn)
        except:
            pass

    def purge(self, DB, conn):
        """
        Deletes every row from a table in the db
        """
        table = self.__class__.__name__
        try:
            r.db(DB).table(table).delete().run(conn)
        except:
            pass

    def get_item(self, idnum):
        """
        Given an id number number of an item in the database, retrieve the data
        the idnum corresponds to in the database
        """
        table = self.__class__.__name__
        return r.db(BaseModel.DB).table(table).get(idnum).run(BaseModel.conn)

    def update_item(self, idnum, data, skip_verify=False):
        """
        Given an id number number of an item in the database and a data hash,
        update the fields of the data in the database with the fields in the
        data hash
        """
        table = self.__class__.__name__
        if not skip_verify:
            verified = self.verify(data)
            if len(verified):
                logging.error("Verification errors: {0}".format(verified))
                return None
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

    def find_item(self, data):
        """
        Given a dictionary of data, find the items in the database that match
        those fields and values.
        """
        table = self.__class__.__name__
        return list(r.db(BaseModel.DB).table(table).filter(data).run(BaseModel.conn))

    def create_item(self, data, skip_verify=False):
        """
        Given data, creates a new database item if the data passes the validator
        Returns an id of the created item, or None if it fails to pass the validator
        """
        table = self.__class__.__name__
        if not skip_verify:
            verified = self.verify(data)
            if len(verified):
                logging.error("Verification errors: {0}".format(verified))
                return None
        o = r.db(BaseModel.DB).table(table).insert(data).run(BaseModel.conn)
        return o['generated_keys'][0]

    # TODO: Write Test for this
    # TODO: spec out skip_verify for other skip_verify calls
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
        result = r.db(BaseModel.DB).table(table).insert(batch_data).run(BaseModel.conn)
        return result['generated_keys']

    def delete_item(self, item_id):
        table = self.__class__.__name__
        return r.db(BaseModel.DB).table(table).get(item_id).delete().run(BaseModel.conn)

    def append_item_to_listfield(self, idnum, listfield, value):
        """
        Given an id number of an item in the database, a listfield of that item, and
        a value, this will append that value to the list.
        """
        table = self.__class__.__name__
        return r.db(self.DB).table(table).get(idnum).update({
            listfield: r.row[listfield].append(value)
        }).run(self.conn)

    def remove_item_from_listfield(self, idnum, listfield, value):
        """
        Given an id number of an item in the database, a listfield of that item, and
        a value, this will remove that value from the listfield
        """
        table = self.__class__.__name__
        return r.db(self.DB).table(table).get(idnum).update({
            listfield: r.row[listfield].set_difference([value])
        }).run(self.conn)

    def schema_list_check(self, method_or_list):
        method = method_or_list

        def _method_check(list_data):
            try:
                for d in list_data:
                    method(d)
            except Exception as e:
                raise AssertionError("Not all elements satisfy: {}".format(e))

        def _list_check(list_data):
            for method in method_or_list:
                try:
                    for d in list_data:
                        method(d)
                except Exception as e:
                    raise AssertionError("Not all elements satisfy: {}".format(e))
        # switch on case
        if callable(method_or_list):
            return _method_check
        if isinstance(method_or_list, (list, tuple)):
            return _list_check
        raise AssertionError("Not all elements satisfy: {}".format(e))
        return None

    def check_data(data, fields, required_fields=[], strict_schema=False):
        if strict_schema:
            for field in data.keys():
                if field not in (required_fields + ['id']):
                    yield (field, 'Extraneous field: {}'.format(field))
        for field in required_fields:
            if field not in data:
                yield (field, 'Missing field: {}'.format(field))
        for key, methods in fields.items():
            if key in data:
                for method in methods:
                    try:
                        method(data[key])
                    except Exception as e:
                        if isinstance(getattr(e, 'message', None), (list, tuple)):
                            for error in e.message:
                                yield error
                        else:
                            yield (key, "{}: {}".format(key, e))

    def verify(self, data, skipRequiredFields=False, skipStrictSchema=False):
        requiredFields = [] if skipRequiredFields else self.requiredFields()
        strictSchema = False if skipStrictSchema else self.strictSchema()
        return list(BaseModel.check_data(data, self.fields(), requiredFields, strictSchema))

    def get_all(self):
        table = self.__class__.__name__
        return list(r.db(BaseModel.DB).table(table).run(BaseModel.conn))
