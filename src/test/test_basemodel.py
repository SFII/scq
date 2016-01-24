import unittest
import tornado.testing
import time
from models.basemodel import BaseModel
from models.user import User
from models.answer import Answer
from config.config import application


class MockModel(BaseModel):
    def requiredFields(self):
        return ['a', 'b', 'c']

    def strictSchema(self):
        return True


class TestBaseModel(tornado.testing.AsyncHTTPTestCase):
    def get_app(self):
        return application

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

    def test_schema_recurse(self):
        pass

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
        self.assertEqual(MockModel().requiredFields(), ['a', 'b', 'c'])

    def test_strictSchema(self):
        self.assertEqual(BaseModel().strictSchema(), False)
        self.assertEqual(MockModel().strictSchema(), True)

    def test_get_item(self):
        pass

    def test_find(self):
        pass

    def test_create_item(self):
        pass

if __name__ == '__main__':
    unittest.main()
