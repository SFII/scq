import rethinkdb as r
import re

class BaseModel:
    def is_int(data):
        assert isinstance(data, (int, float)), "Must be a number"

    def is_truthy(data):
        assert (data and True), "Must be Truthy"

    def is_falsey(data):
        assert (data or False), "Must be Falsey"

    def is_date_string(data):
        try:
            time.strptime(data, '%a %b %d %H:%M:%S %Z %Y')
        except Exception, ex:
            raise Exception("datestring '{0}' could not be parsed into date object".format(data))

    def is_string(data):
        assert isinstance(data, (str, unicode)), "Must be a string"

    def is_valid_email(data):
        assert re.match(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$", data) is not None, "Must be a valid email address"

    def is_list(data):
        assert isinstance(data, (list, tuple)), "Must be a list"

    def is_none(data):
        assert data is None, "Must be empty"

    def is_user(user_id):
        assert db.exists('user', user_id), "Must be a valid user ID"

    def is_content_node(node_id):
        assert db.exists('content_node', node_id), "Must be a valid content node"

    def is_user_node(node_id):
        assert db.exists('user_node', node_id), "Must be a valid user node"

    def is_in_list(master_list, alias=None):
        def _in_list(data):
            assert data in master_list, "Must be in {}".format(alias or master_list)
        return _in_list

    def is_in_range(low, high=None):
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
            except Exception, exa:
                try:
                    method_b(data)
                except Exception, exb:
                    raise Exception("Must be one of the following: {} or {}".format(exa, exb))
        return _or

    def schema_list_check(method):
        def _list_check(data):
            try:
                all(method(d) for d in data)
            except Exception, e:
                raise Exception("Not all elements satisfy: {}".format(e))
        return _list_check

    def check_data(data, fields, required_fields=[]):
        for field in required_fields:
            if field not in data:
                yield (field, 'Missing field: {}'.format(field))
        for key, methods in fields.iteritems():
            if key in data:
                for method in methods:
                    try:
                        method(data[key])
                    except Exception, e:
                        if isinstance(e.message, (list, tuple)):
                            for error in e.message:
                                yield error
                        else:
                            yield (key, "{}: {}".format(key, e))

    # critical methods

    def fields():
        {'id' : (is_string, )}

    def requiredFields():
        ['id']

    def init(self, conn):
        try:
            yield r.table_create(__name__).run(conn)
        except:
            print "Table {0} already exist".format(__name__)

    def verify(self, data):
        return list(check_data(data, fields(), requiredFields()))
