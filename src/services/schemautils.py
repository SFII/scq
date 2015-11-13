#!/usr/bin/env python3.4

from lib import database as db

def is_int(data):
    assert isinstance(data, (int, float)), "Must be a number"

def is_string(data):
    assert isinstance(data, (str, unicode)), "Must be a string"

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

def is_material(node_id):
    pass

def is_in_range(low, high=None):
    def _in_range(data):
        if high is None:
            assert low <= data, "Must be larger than {}".format(low)
        else:
            assert low <= data <= high, "Must be between {} and {}".format(low, high)
    return _in_range

def schema_recurse(fields, require_all_fields=True):
    def _recurse(data):
        errors = list(check_data(data, fields, require_all_fields))
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

def is_knowledge_graph(data):
    pass

def check_data(data, fields, require_all_fields=True):
    if require_all_fields:
        for field in fields:
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


user_node_child_fields = {
    "type" : (is_in_list(["user_node", "content_node"]),),
    "id" : (schema_or(is_user_node, is_content_node),),
    "start_time" : (schema_or(is_none, is_in_range(0)),),
    "end_time" : (schema_or(is_none, is_in_range(0)),),
    "title" : (is_string, ),
}

user_node_fields = {
    "id" : (is_int, ),
    "title" : (is_string, ),
    "parent" : (schema_or(is_none, is_user_node), ),
    "owner" : (is_user, ),
    "created_on" : (is_int, ),
    "base_node" : (schema_or(is_none, is_user_node), ),
    "children" : (is_list, schema_list_check(schema_recurse(user_node_child_fields))),
}

user_fields = {
    "id" : (is_int, ),
    "name" : (is_string, ),
    "type" : (is_in_list(['admin', 'teacher', 'student']), ),
    "user_nodes" : (is_list, schema_list_check(is_user_node)),
    "completed_content" : (is_list, schema_list_check(is_content_node)),
    "owned_materials" : (is_list, schema_list_check(is_material)),
}

content_node_fields = {
    'id' : (is_int, ),
    'title' : (is_string, ),
    'text' : (is_string, ),
    'description' : (is_string, ),
    'creator' : (is_user, ),
    'knowledge_graph' : (is_knowledge_graph, ),
    'base_node' : (schema_or(is_none, is_content_node), ),
    'grade_level' : (is_int, is_in_range(0, 12)),
    'recommended_time' : (is_int, is_in_range(0)) ,
    'materials' : (is_list, schema_list_check(is_material)),
    'standards' : (is_list, schema_list_check(is_in_list(db.STANDARDS.keys(), alias="CORE Standards"))),
}
