import unittest
from test.test_runner import BaseAsyncTest
import time
import rethinkdb as r
import logging
from models.basemodel import BaseModel


class MockModel(BaseModel):
    def requiredFields(self):
        return ['a', 'b', 'c', 'x']

    def strictSchema(self):
        return True

    def default(self):
        return {
            'a': 1,
            'b': 'two',
            'c': ['falsey', False, 'or', 0, 'Strings']
        }

    def fields(self):
        b = super(MockModel, self)
        return {
            'a': (b.is_int, ),
            'b': (b.is_string, ),
            'c': (b.is_list, b.is_not_empty, b.schema_list_check(
                b.schema_or(b.is_falsey, b.is_string),),),
            'x': (b.is_timestamp,)
        }


class TestBaseModel(BaseAsyncTest):
    mock_data = {}
    mock_id = ""
    mock_x = 0

    def setUpClass():
        # logging.disable(logging.CRITICAL)
        # Initializes Mockmodel Table
        MockModel().init(BaseAsyncTest.database_name, BaseAsyncTest.conn)
        return

    def setup():
        mock_data = {}
        mock_id = ""
        mock_x = 0

    def test_is_int(self):
        try:
            BaseModel().is_int(3)
        except AssertionError:
            self.fail('Error: 3 is not recognized as a number from is_int')
        try:
            BaseModel().is_int(15.235232)
        except AssertionError:
            self.fail('Error: 15.235232 is not recognized as a number from is_int')
        for i in ['string', [1, 2, 3], False, True]:
            with self.assertRaises(AssertionError):
                BaseModel().is_int(i)

    def test_is_truthy(self):
        try:
            BaseModel().is_truthy(True)
            BaseModel().is_truthy(1)
            BaseModel().is_truthy("string")
        except:
            self.fail('Error: data as True or 1 should be Truthy')
        for i in [False, 0, None]:
            with self.assertRaises(AssertionError):
                BaseModel().is_truthy(i)

    def test_is_falsey(self):
        try:
            BaseModel().is_falsey(False)
            BaseModel().is_falsey(0)
            BaseModel().is_falsey(None)
        except:
            self.fail('Error: data should be falsey?')
        for i in [True, 1, "string"]:
            with self.assertRaises(AssertionError):
                BaseModel().is_falsey(i)

    def test_not_empty(self):
        try:
            BaseModel().is_not_empty('fdsa')
            BaseModel().is_not_empty([1, 2, 3])
        except:
            self.fail('Error: data should not be empty / have length > 0')
        with self.assertRaises(AssertionError):
            BaseModel().is_not_empty([])
        with self.assertRaises(AssertionError):
            BaseModel().is_not_empty('')

    def test_is_timestamp(self):
        try:
            BaseModel().is_timestamp(123456789)
        except:
            self.fail('Error: timestamp should be valid')
        try:
            BaseModel().is_timestamp(time.time())
        except:
            self.fail('Error: timestamp should be valid')
        try:
            BaseModel().is_timestamp(123456789.54321)
        except:
            self.fail('Error: timestamp should be valid')
        with self.assertRaises(AssertionError):
            BaseModel().is_timestamp('Friday December 24 12:34:56 GMT 2015')
        with self.assertRaises(AssertionError):
            BaseModel().is_timestamp('Sun Jan 32 23:00:00 GMT 1980')
        with self.assertRaises(AssertionError):
            BaseModel().is_timestamp('Sat Apr 9 24:00:00 MST 2012')
        with self.assertRaises(AssertionError):
            BaseModel().is_timestamp(-12345)
        with self.assertRaises(AssertionError):
            BaseModel().is_timestamp(True)
        with self.assertRaises(AssertionError):
            BaseModel().is_timestamp(False)
        with self.assertRaises(AssertionError):
            BaseModel().is_timestamp(-123321123.321)

    def test_is_string(self):
        try:
            BaseModel().is_string('hello')
        except:
            self.fail('Error: hello should be a valid string')
        with self.assertRaises(AssertionError):
            BaseModel().is_string(123)
        with self.assertRaises(AssertionError):
            BaseModel().is_string(15.2)
        with self.assertRaises(AssertionError):
            BaseModel().is_string(True)
        with self.assertRaises(AssertionError):
            BaseModel().is_string(False)
        with self.assertRaises(AssertionError):
            BaseModel().is_string([1, 2, 3])
        with self.assertRaises(AssertionError):
            BaseModel().is_string(['this', 'is', 'string', 'array'])

    def test_is_valid_email(self):
        try:
            BaseModel().is_valid_email('suba8204@colorado.edu')
        except:
            self.fail('Error: this should be a valid colorado school email')
        try:
            BaseModel().is_valid_email('sung.bae@colorado.edu')
        except:
            self.fail('Error: first.last@colorado.edu should be a valid email')
        try:
            BaseModel().is_valid_email('someUserName@someEmailDomain.something')
        except:
            self.fail('Error: this has the correct syntax for a valid email')
        try:
            BaseModel().is_valid_email('user.user.user123456789@colorado.edu')
        except:
            self.fail('Error: this has the correct syntax for a valid email')
        with self.assertRaises(AssertionError):
            BaseModel().is_valid_email('thisEmailShouldNotWork!@colorado.edu')
        with self.assertRaises(AssertionError):
            BaseModel().is_valid_email('invalidEmail@yahoo!.com')
        with self.assertRaises(AssertionError):
            BaseModel().is_valid_email('hello')
        with self.assertRaises(Exception):
            BaseModel().is_valid_email(1)
        with self.assertRaises(Exception):
            BaseModel().is_valid_email(1.5)
        with self.assertRaises(Exception):
            BaseModel().is_valid_email(True)
        with self.assertRaises(Exception):
            BaseModel().is_valid_email([1, 2, 3])
        with self.assertRaises(Exception):
            BaseModel().is_valid_email(['a', 'b', 'c'])

    def test_is_list(self):
        try:
            BaseModel().is_list([1, 2, 3])
        except:
            self.fail('Error: [1, 2, 3] should be a valid list')
        try:
            BaseModel().is_list(['a'])
        except:
            self.fail('Error: this should be a valid list of one string entry')
        try:
            BaseModel().is_list(['hello', 1, 2.5, False, [1, 2, 3]])
        except:
            self.fail('Error: a list can consist of multiple data types')
        try:
            BaseModel().is_list(('hi', 1, True))
        except:
            self.fail('Error: tuples should be valid')
        with self.assertRaises(AssertionError):
            BaseModel().is_list(1)
        with self.assertRaises(AssertionError):
            BaseModel().is_list('hi')
        with self.assertRaises(AssertionError):
            BaseModel().is_list(True)

    def test_is_none(self):
        try:
            BaseModel().is_none(None)
        except:
            self.fail('Error: None should be empty')
        with self.assertRaises(AssertionError):
            BaseModel().is_none('')
        with self.assertRaises(AssertionError):
            BaseModel().is_none(0)
        with self.assertRaises(AssertionError):
            BaseModel().is_none([])
        with self.assertRaises(AssertionError):
            BaseModel().is_none(True)

    def test_is_in_list(self):
        try:
            BaseModel().is_in_list([1, 2, 3])(1)
            BaseModel().is_in_list([1, 2, 3])(2)
            BaseModel().is_in_list([1, 2, 3])(3)
        except:
            self.fail('Error: is_in_list should work with integers')
        try:
            BaseModel().is_in_list([1.2, 2.3, 3.4])(1.2)
            BaseModel().is_in_list([1.2, 2.3, 3.4])(2.3)
            BaseModel().is_in_list([1.2, 2.3, 3.4])(3.4)
        except:
            self.fail('Error: is_in_list should work with floats')
        try:
            BaseModel().is_in_list(['hello', 'world', 'KITTY'])('hello')
            BaseModel().is_in_list(['hello', 'world', 'KITTY'])('world')
            BaseModel().is_in_list(['hello', 'world', 'KITTY'])('KITTY')
        except:
            self.fail('Error: is_in_list should work with strings')
        test_list = BaseModel.is_in_list(['Hello', 'World', True, 456])
        for i in ['Goodbye', 'WORLD', False, 123]:
            with self.assertRaises(AssertionError):
                test_list(i)

    def test_is_in_range(self):
        try:
            test_range = BaseModel().is_in_range(0, 4)
            test_range(0)
            test_range(1)
            test_range(2)
            test_range(3)
            test_range(4)
        except:
            self.fail('Error: is_in_range should work with integers')
        try:
            test_range = BaseModel().is_in_range(0, 4.5)
            test_range(0.5)
            test_range(1.9)
            test_range(2.2456767)
            test_range(3.9999)
            test_range(4.4999999)
        except:
            self.fail('Error: is_in_range should work with floats')
        test_range = BaseModel().is_in_range(0.5, 4.5)
        with self.assertRaises(AssertionError):
            test_range(0.49)
        with self.assertRaises(AssertionError):
            test_range(4.50001)

    def test_schema_list_check(self):
        b = BaseModel()
        check_or = b.schema_list_check(b.schema_or(b.is_falsey, b.is_string))
        check_int = b.schema_list_check(b.is_int)
        check_truthy = b.schema_list_check(b.is_truthy)
        or_data = ['falsey', 0, 'or', False, 'string']
        int_data = [-1, -34.55, 0, 4321, 1, 1004.567]
        truthy_data = ["Truthy", True, 1, "data"]
        try:
            check_or(or_data)
            check_int(int_data)
            check_truthy(truthy_data)
        except:
            self.fail('Error: schema_list_check should succeed')
        for i in [or_data, int_data]:
            with self.assertRaises(AssertionError):
                check_truthy(i)
        for i in [or_data, truthy_data]:
            with self.assertRaises(AssertionError):
                check_int(i)
        for i in [truthy_data, int_data]:
            with self.assertRaises(AssertionError):
                check_or(i)

    def test_schema_or(self):
        is_truthy = BaseModel().is_truthy
        is_falsey = BaseModel().is_falsey
        is_int = BaseModel().is_int
        is_string = BaseModel().is_string
        true_or_false = BaseModel().schema_or(is_truthy, is_falsey)
        int_or_str = BaseModel().schema_or(is_int, is_string)
        try:
            true_or_false(False)
            true_or_false(True)
            true_or_false("True")
            true_or_false(0)
        except:
            self.fail('Error: schema_or(is_truthy, is_falsey) should succeed')
        try:
            int_or_str("salad")
            int_or_str(-99.345)
            int_or_str("True")
            int_or_str(0)
        except:
            self.fail('Error: schema_or(is_int, is_string) should succeed for this value')
        for i in [True, False, None, MockModel()]:
            with self.assertRaises(AssertionError):
                int_or_str(i)

    def test_requiredFields(self):
        self.assertEqual(BaseModel().requiredFields(), [])
        self.assertEqual(MockModel().requiredFields(), ['a', 'b', 'c', 'x'])

    def test_strictSchema(self):
        self.assertEqual(BaseModel().strictSchema(), False)
        self.assertEqual(MockModel().strictSchema(), True)

    def test_is_unique(self):
        MockModel().purge(BaseAsyncTest.database_name, BaseAsyncTest.conn)
        mock_data = MockModel().default()
        mock_data['x'] = time.time()
        is_unique_a = MockModel().is_unique('a')
        is_unique_b = MockModel().is_unique('b')
        is_unique_c = MockModel().is_unique('c')
        try:
            is_unique_a(mock_data)
            is_unique_b(mock_data)
            is_unique_c(mock_data)
        except:
            self.fail('Error: is_unique should succeed')
        mock_id = MockModel().create_item(mock_data)
        time.sleep(0.1)
        self.assertIsNotNone(mock_id)
        for is_unique in [is_unique_a, is_unique_b, is_unique_c]:
            with self.assertRaises(AssertionError):
                is_unique(mock_data)

    def test_exists_in_table(self):
        mock_data = MockModel().default()
        mock_data['x'] = time.time()
        exists_in_table = MockModel().exists_in_table('MockModel')
        with self.assertRaises(AssertionError):
            exists_in_table('0')
        mock_id = MockModel().create_item(mock_data)
        try:
            exists_in_table(mock_id)
        except:
            self.fail('Error: exists_in_table should succeed')

    def test_verify(self):
        # Check MockModel().default() doesn't verify by default
        mock_data = MockModel().default()
        verified = MockModel().verify(mock_data)
        self.assertIn(('x', 'Missing field: x'), verified)
        # Check strictSchema prohibits extraneous fields
        mock_data['z'] = 1
        verified = MockModel().verify(mock_data)
        self.assertIn(('z', 'Extraneous field: z'), verified)
        # Check id doesn't count as an extraneous field
        mock_data = MockModel().default()
        mock_data['id'] = '4321fdsa'
        verified = MockModel().verify(mock_data)
        self.assertNotIn(('id', 'Extraneous field: id'), verified)
        # Check schema_list_check
        mock_data['c'].append(True)
        mock_data['x'] = time.time()
        verified = MockModel().verify(mock_data)
        self.assertNotEqual(len(verified), 0)
        self.assertIn('c', verified[0])
        # check a correct datatset passes
        mock_data['c'].pop()
        verified = MockModel().verify(mock_data)
        self.assertEqual(len(verified), 0)

    def test_get_item(self):
        mock_data = MockModel().default()
        mock_data['x'] = time.time()
        mock_id = MockModel().create_item(mock_data)
        item = MockModel().get_item(mock_id)
        self.assertEqual(item['a'], mock_data['a'])
        self.assertEqual(item['b'], mock_data['b'])
        self.assertEqual(item['c'], mock_data['c'])
        self.assertEqual(item['x'], mock_data['x'])
        self.assertEqual(item['id'], mock_id)

    def test_find_item(self):
        mock_data = MockModel().default()
        mock_time = time.time()
        mock_data['x'] = mock_time
        mock_id = MockModel().create_item(mock_data)
        found = MockModel().find_item({'x': (mock_time - 10)})
        self.assertEqual(len(found), 0)
        found = MockModel().find_item({'x': (mock_time)})
        self.assertEqual(len(found), 1)
        item = found[0]
        self.assertEqual(item['a'], mock_data['a'])
        self.assertEqual(item['b'], mock_data['b'])
        self.assertEqual(item['c'], mock_data['c'])
        self.assertEqual(item['x'], mock_data['x'])
        self.assertEqual(item['id'], mock_id)

    def test_delete_item(self):
        mock_data = MockModel().default()
        mock_time = time.time()
        mock_data['x'] = mock_time
        mock_id = MockModel().create_item(mock_data)
        item = MockModel().get_item(mock_id)
        self.assertIsNotNone(item)
        MockModel().delete_item(mock_id)
        item = MockModel().get_item(mock_id)
        self.assertIsNone(item)

    def test_create_item(self):
        mock_data = MockModel().default()
        mock_id = MockModel().create_item(mock_data)
        self.assertIsNone(mock_id)
        mock_data['x'] = time.time()
        mock_id = MockModel().create_item(mock_data)
        self.assertIsNotNone(mock_id)

    def test_search_items(self):
        mock_data = [
            {'a': 1, 'b': 'John Black csci-1300', 'x': time.time(), 'c': ['computer', 'science', 'introduction', 'csci', '1300']},
            {'a': 2, 'b': 'Muffins engl-2300', 'x': time.time(), 'c': ['introduction', 'literature', 'engl', '2300', 'Muffins']},
            {'a': 3, 'b': 'snickers candy geen-1000', 'x': time.time(), 'c': ['underwater', 'basket', 'weaving', 'elective']},
            {'a': 4, 'b': 'Boese csci-2300', 'x': time.time(), 'c': ['Elizabeth', 'Boese', 'object', 'oriented', 'programming', 'csci', '2300', 'computer', 'science']},
            {'a': 5, 'b': 'Republican Political Science poli-1100', 'x': time.time(), 'c': ['John', 'Boehner', 'Republican', 'values', 'intensive']},
            {'a': 6, 'b': 'Democratic Political Science poli-1200', 'x': time.time(), 'c': ['John', 'Adams', 'Democratic', 'values', 'intensive']},
            {'a': 7, 'b': 'Finding your soul through clay; arts-1300', 'x': time.time(), 'c': ['introduction', 'art', 'nonmajors', 'arts', '1300']},
            {'a': 8, 'b': 'Advanced Computer Science Topics; csci-2700', 'x': time.time(), 'c': ['advanced', 'computer', 'science', 'topics', '2700']},
            {'a': 9, 'b': 'Netflix Studies poli-1300', 'x': time.time(), 'c': ['Elizabeth', 'Hale', 'pragmatic', 'values', 'intensive']},
            {'a': 10, 'b': 'fuckbois', 'x': time.time(), 'c': ['bad', 'data', None, False, 0]}
        ]
        for data in mock_data:
            MockModel().create_item(data)
        searchfields = ['b', 'c']
        returnfields = ['id', 'a']
        results = MockModel().search_items('Intro to literature', searchfields, returnfields)
        self.assertEqual(len(results), 1)
        result = results[0]
        self.assertEqual(result['a'], 2)
        results = MockModel().search_items('Elizabeth Boese', searchfields, returnfields)
        self.assertEqual(len(results), 1)
        result = results[0]
        self.assertEqual(result['a'], 4)
        results = MockModel().search_items('Political Science Intensive', searchfields, returnfields)
        self.assertEqual(len(results), 2)
        items = list(map(lambda foo: foo['a'], results))
        self.assertIn(5, items)
        self.assertIn(6, items)
        results = MockModel().search_items('', searchfields, returnfields)
        self.assertEqual(len(results), 0)

    def teardown():
        if (mock_id is not None) or (mock_id is not ""):
            MockModel.delete_item(mock_id)

    def tearDownClass():
        logging.disable(logging.NOTSET)
        # Drop the database
        MockModel().drop(BaseAsyncTest.database_name, BaseAsyncTest.conn)

if __name__ == '__main__':
    unittest.main()
