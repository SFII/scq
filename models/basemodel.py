import rethinkdb as r
import re
import time
from datetime import datetime
import tornado.gen as gen
import logging

# Stopwords from https://pypi.python.org/pypi/stop-words

STOPWORDS = ['', 'a', 'about', 'above', 'after', 'again', 'against', 'all', 'am',
             'an', 'and', 'any', 'are', "aren't", 'as', 'at', 'be', 'because', 'been',
             'before', 'being', 'below', 'between', 'both', 'but', 'by', "can't", 'cannot',
             'could', "couldn't", 'did', "didn't", 'do', 'does', "doesn't", 'doing', "don't",
             'down', 'during', 'each', 'few', 'for', 'from', 'further', 'had', "hadn't",
             'has', "hasn't", 'have', "haven't", 'having', 'he', "he'd", "he'll", "he's",
             'her', 'here', "here's", 'hers', 'herself', 'him', 'himself', 'his', 'how',
             "how's", 'i', "i'd", "i'll", "i'm", "i've", 'if', 'in', 'into', 'is', "isn't",
             'it', "it's", 'its', 'itself', "let's", 'me', 'more', 'most', "mustn't", 'my',
             'myself', 'no', 'nor', 'not', 'of', 'off', 'on', 'once', 'only', 'or', 'other',
             'ought', 'our', 'ours', 'ourselves', 'out', 'over', 'own', 'same', "shan't",
             'she', "she'd", "she'll", "she's", 'should', "shouldn't", 'so', 'some', 'such',
             'than', 'that', "that's", 'the', 'their', 'theirs', 'them', 'themselves',
             'then', 'there', "there's", 'these', 'they', "they'd", "they'll", "they're",
             "they've", 'this', 'those', 'through', 'to', 'too', 'under', 'until', 'up',
             'very', 'was', "wasn't", 'we', "we'd", "we'll", "we're", "we've", 'were',
             "weren't", 'what', "what's", 'when', "when's", 'where', "where's", 'which',
             'while', 'who', "who's", 'whom', 'why', "why's", 'with', "won't", 'would',
             "wouldn't", 'you', "you'd", "you'll", "you're", "you've", 'your', 'yours',
             'yourself', 'yourselves']


class BaseModel:

    def is_int(self, data):
        assert data is not True, "value '{0}' Must be a number".format(data)
        assert data is not False, "value '{0}' Must be a number".format(data)
        assert isinstance(data, (int, float)), "value '{0}' Must be a number".format(data)

    def is_truthy(self, data):
        assert (data and True), "data '{0}' Must be Truthy".format(data)

    def is_boolean(self, data):
        assert (data == True or data == False)

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
            try:
                value = data[key]
            except TypeError:
                value = data
            assert len(self.find_item({key: value})) == 0, "data '{0}' Must must be a unique value in the database with respect to key {1}".format(data, key)
        return _unique

    def exists_in_table(self, table):
        def _exists(data):
            assert r.db(self.DB).table(table).get(data).run(self.conn) is not None, "id '{0}' does not exist in table {1}".format(data, table)
        return _exists

    def is_id(self, data):
        self.is_string(data)
        assert (len(data) < 127), "id '{0}' must be 127 characters or fewer".format(data)

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
        this = self.__class__
        table = this.__name__
        this.conn = conn
        this.DB = DB
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
        return r.db(self.DB).table(table).get(idnum).run(self.conn)

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
        return r.db(self.DB).table(table).get(idnum).update(data).run(self.conn)

    """
    Something weird is going on in this method, or in Group.subscribe_user method.
    The first call to this method gives an actual 'id' of the user, but the calls
    after that will give username instead. That is why I have popped off the first
    member in group_api_hander (that is the first name in the field of members
    which is a duplicate of the creator).
    """
    def subscribe_user(self, user_id, row_id, user_subscription_name=None):
        """
        adds a user id to a User() and Group() models' subscription/pending list.
        """
        if user_id is None:
            logging.error("user_id cannot be None")
            return False
        if row_id is None:
            logging.error("row_id cannot be None")
            return False
        submember = False
        user_table = 'User'
        row_table = self.__class__.__name__
        if user_id[:4].isalpha() and len(user_id) == 8:
            # Since all username is unique, we have only one entry in the list
            user_list = list(r.db(self.DB).table(user_table).filter({"username": user_id}).run(self.conn))
            if user_list is None:
                logging.error("User {0} does not exist".format(user_id))
                return False
            user_dict = user_list[0]
            user_id = user_dict['id']
            submember = True
        user_data = r.db(self.DB).table(user_table).get(user_id).run(self.conn)
        row_data = r.db(self.DB).table(row_table).get(row_id).run(self.conn)
        if user_data is None:
            logging.error("User {0} does not exist".format(user_id))
            return False
        if row_data is None:
            logging.error("{0} {1} does not exist".format(row_table, row_data))
            return False
        try:
            if (user_subscription_name is not None) and (submember is False):
                user_subscription = user_data.get(user_subscription_name, [])
                user_subscription.append(row_id)
                user_subscription = list(set(user_subscription))
                r.db(self.DB).table(user_table).get(user_id).update({user_subscription_name: user_subscription}).run(self.conn)
            else:
                user_pending = user_data.get("pending_groups", [])
                user_pending.append(row_id)
                user_pending = list(set(user_pending))
                r.db(self.DB).table(user_table).get(user_id).update({"pending_groups": user_pending}).run(self.conn)
        except KeyError:
            logging.error("user subscription {0} not known in user data".format(user_subscription_name))
            return False
        if submember is False:
            subscribers = row_data['subscribers']
            subscribers.append(user_id)
            subscribers = list(set(subscribers))
            return r.db(self.DB).table(row_table).get(row_id).update({'subscribers': subscribers}).run(self.conn)
        else:
            penders = row_data['penders']
            penders.append(user_id)
            penders = list(set(penders))
            return r.db(self.DB).table(row_table).get(row_id).update({'penders': penders}).run(self.conn)

    def unsubscribe_user(self, user_id, row_id, user_subscription_name=None):
        """
        removes a user id to a model's subscription list.
        """
        if user_id is None:
            logging.error("user_id cannot be None")
            return False
        if row_id is None:
            logging.error("row_id cannot be None")
            return False
        row_table = self.__class__.__name__
        user_table = 'User'
        user_data = r.db(self.DB).table(user_table).get(user_id).run(self.conn)
        row_data = r.db(self.DB).table(row_table).get(row_id).run(self.conn)
        if user_data is None:
            logging.error("User {0} does not exist".format(user_data))
            return False
        if row_data is None:
            logging.error("{0} {1} does not exist".format(row_table, row_data))
            return False
        if user_subscription_name is not None:
            user_subscription = user_data.get(user_subscription_name, [])
            try:
                user_subscription.remove(row_id)
            except ValueError:
                logging.warn("row_id {0} not in user {1}".format(row_id, user_subscription_name))
                pass
            r.db(self.DB).table(user_table).get(user_id).update({user_subscription_name: user_subscription}).run(self.conn)
        active_surveys = r.db(self.DB).table('Group').get(row_id).get_field('active_surveys').run(self.conn)
        unanswered_surveys = r.db(self.DB).table(user_table).get(user_id).get_field('unanswered_surveys').run(self.conn)
        answered_surveys = r.db(self.DB).table(user_table).get(user_id).get_field('answered_surveys').run(self.conn)
        for survey in active_surveys:
            if survey in unanswered_surveys:
                unanswered_surveys = [x for x in unanswered_surveys if x != survey]
            elif survey in answered_surveys:
                answered_surveys = [x for x in answered_surveys if x != survey]
        r.db(self.DB).table(user_table).get(user_id).update({'unanswered_surveys': unanswered_surveys}).run(self.conn)
        r.db(self.DB).table(user_table).get(user_id).update({'answered_surveys': answered_surveys}).run(self.conn)
        subscribers = row_data['subscribers']
        try:
            subscribers.remove(user_id)
        except ValueError:
            pass
        return r.db(self.DB).table(row_table).get(row_id).update({'subscribers': subscribers}).run(self.conn)

    def remove_pending_user(self, user_id, row_id, user_pending_name=None):
        """
        removes a user id to a model's pending list.
        """
        if user_id is None:
            logging.error("user_id cannot be None")
            return False
        if row_id is None:
            logging.error("row_id cannot be None")
            return False
        row_table = self.__class__.__name__
        user_table = 'User'
        user_data = r.db(self.DB).table(user_table).get(user_id).run(self.conn)
        row_data = r.db(self.DB).table(row_table).get(row_id).run(self.conn)
        if user_data is None:
            logging.error("User {0} does not exist".format(user_data))
            return False
        if row_data is None:
            logging.error("{0} {1} does not exist".format(row_table, row_data))
            return False
        if user_pending_name is not None:
            user_pending = user_data.get(user_pending_name, [])
            try:
                user_pending.remove(row_id)
            except ValueError:
                logging.warn("row_id {0} not in user {1}".format(row_id, user_pending_name))
                pass
            r.db(self.DB).table(user_table).get(user_id).update({user_pending_name: user_pending}).run(self.conn)
        penders = row_data['penders']
        try:
            penders.remove(user_id)
        except ValueError:
            pass
        return r.db(self.DB).table(row_table).get(row_id).update({'penders': penders}).run(self.conn)

    # adds a survey_id to a user's unanswered_surveys list.
    # maybe this should live somewhere else? like user? or survey?
    def send_user_survey(self, user_id, survey_id, survey_key='unanswered_surveys'):
        survey_table = 'Survey'
        user_table = 'User'
        user_data = r.db(self.DB).table(user_table).get(user_id).run(self.conn)
        survey_data = r.db(self.DB).table(survey_table).get(survey_id).run(self.conn)
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
        return r.db(self.DB).table(user_table).get(user_id).update({survey_key: user_survey_list}).run(self.conn)

    def find_item(self, data):
        """
        Given a dictionary of data, find the items in the database that match
        those fields and values.
        """
        table = self.__class__.__name__
        return list(r.db(self.DB).table(table).filter(data).run(self.conn))

    # TODO: write test for generated keys returning when 'id' fields are given
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
        result = r.db(self.DB).table(table).insert(data).run(self.conn)
        generated_keys = result.get('generated_keys')
        if generated_keys is None:
            return data.get('id')
        return generated_keys[0]

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
        result = r.db(self.DB).table(table).insert(batch_data).run(self.conn)
        return result.get('generated_keys')

    def delete_item(self, item_id):
        table = self.__class__.__name__
        return r.db(self.DB).table(table).get(item_id).delete().run(self.conn)

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
        fields = self.fields()
        fields.update({'id': (self.is_id, )})
        return list(BaseModel.check_data(data, fields, requiredFields, strictSchema))

    def get_all(self):
        table = self.__class__.__name__
        return list(r.db(self.DB).table(table).run(self.conn))

    def search_items(self, searchstring, searchfields=['tags'], returnfields=['id']):
        """
        Searches through the Table
        1) search all alternate_titles for full searchstring
        2) if searchstring contains a number > 99, search course_numbers for that number
        3) if searchstring contains a ngram with four or fewer characters, looks through course_subject
        """

        DB = self.DB
        table = self.__class__.__name__
        lowercase_searchstring = searchstring.lower()
        lowercase_searchstring.replace('-', ' ')
        splitwords = lowercase_searchstring.split(' ')
        words = list(filter(lambda word: word not in STOPWORDS, splitwords))

        if not len(words):
            return []

        logging.info(words)

        def sequence_search(searchfield, words):
            return r.expr(words).concat_map(
                lambda word: r.db(DB).table(table).filter(
                    lambda doc: doc[searchfield].map(
                        lambda title: title.do(
                            lambda matcher: matcher.coerce_to('STRING').match('(?i)' + word)
                        )
                    ).reduce(lambda left, right: left | right)
                ).coerce_to('array').map(lambda doc: doc['id'])
            )

        def static_search(searchfield, words):
            return r.expr(words).concat_map(
                lambda word: r.db(DB).table(table).filter(
                    lambda doc: doc[searchfield].coerce_to('STRING').match('(?i)' + word)
                ).coerce_to('array').map(lambda doc: doc['id'])
            )

        def search(searchfield, words):
            if isinstance(self.default()[searchfield], (list, tuple)):
                return sequence_search(searchfield, words)
            return static_search(searchfield, words)

        searches = [search(searchfield, words) for searchfield in searchfields]
        total_results = r.add(r.args(searches)).run(self.conn)

        searchresults = (r.expr(total_results)).group(r.row).count().ungroup().order_by('reduction').run(self.conn)

        if not len(searchresults):
            return []

        best_score = searchresults[-1]['reduction']

        best_ids = r.expr(searchresults).filter({'reduction': best_score}).get_field('group').run(self.conn)

        if 'id' not in returnfields:
            logging.warn("'id' is not in listed returnfields. It's recomended this field is included")
        if not len(returnfields):
            logging.error("returnfields cannot be empty")
            return []
        try:
            return list(r.db(DB).table(table).get_all(r.args(best_ids)).pluck(r.args(returnfields)).run(self.conn))
        except err:
            logging.error(err)
            return []
