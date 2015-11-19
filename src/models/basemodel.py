import rethinkdb as r
import re
import time
import tornado.gen as gen
import logging

class BaseModel:
    conn = r.connect(host='localhost', port=28015)
    DB = "scq"

    def is_int(self, data):
        assert isinstance(data, (int, float)), "Must be a number"

    def is_truthy(self, data):
        assert (data and True), "Must be Truthy"

    def is_falsey(self, data):
        assert (data or False), "Must be Falsey"

    def is_date_string(self, data):
        try:
            time.strptime(data, '%a %b %d %H:%M:%S %Z %Y')
        except Exception as e:
            raise Exception("datestring '{0}' could not be parsed into date object:".format(data))

    def is_string(self, data):
        assert isinstance(data, (str,)), "Must be a string"

    def is_valid_email(self, data):
        assert re.match(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$", data) is not None, "Must be a valid email address"

    def is_list(self, data):
        assert isinstance(data, (list, tuple)), "Must be a list"

    def is_none(self, data):
        assert data is None, "Must be empty"

    def is_user(self, user_id):
        assert db.exists('user', user_id), "Must be a valid user ID"

    def is_content_node(self, node_id):
        assert db.exists('content_node', node_id), "Must be a valid content node"

    def is_user_node(self, node_id):
        assert db.exists('user_node', node_id), "Must be a valid user node"

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

    def schema_recurse(fields, required_fields=[]):
        def _recurse(data):
            errors = list(check_data(data, fields, required_fields))
            if errors:
                raise Exception(errors)
        return _recurse

    def schema_or(method_a, method_b):
        def _or(data):
            try:
                method_a(data)
            except Exception as exa:
                try:
                    method_b(data)
                except Exception as exb:
                    raise Exception("Must be one of the following: {} or {}".format(exa, exb))
        return _or

    def requiredFields(self):
        return []


    def init(self, conn):
        table = self.__class__.__name__
        try:
            r.db(BaseModel.DB).table_create(table).run(conn)
        except:
            pass

    def isValid(self, data):
        return True


    def get_item(self, idnum):
        table = self.__class__.__name__
        return r.db(BaseModel.DB).table(table).get(idnum).run(BaseModel.conn)

    def find(self, key):
        table = self.__class__.__name__
        return list(r.db(BaseModel.DB).table(table).filter(key).run(BaseModel.conn))

    def create_item(self, data):
        table = self.__class__.__name__
        if self.isValid(data):
            o = r.db(BaseModel.DB).table(table).insert(data).run(BaseModel.conn)
            return o['generated_keys'][0]
