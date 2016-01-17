import unittest
import tornado.testing
from models.basemodel import BaseModel
from models.user import User
from models.answer import Answer
from config.config import application

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

        with self.assertRaises(AssertionError):
            BaseModel().is_int('string')
        #with self.assertRaises(Exception):
        #    BaseModel().is_int(True)
        #with self.assertRaises(Exception):
        #    BaseModel().is_int(False)
        with self.assertRaises(AssertionError):
            BaseModel().is_int([1,2,3])

    def test_is_truthy(self):
        try:
            BaseModel().is_truthy(True)
            BaseModel().is_truthy(1)
        except:
            self.fail('Error: data as True or 1 should be Truthy')
        with self.assertRaises(AssertionError):
            BaseModel().is_truthy(False)
        with self.assertRaises(AssertionError):
            BaseModel().is_truthy(0)

    def test_is_falsey(self):
        try:
            BaseModel().is_falsey(True)
            BaseModel().is_falsey(1)
        except:
            self.fail('Error: data should be falsey?')
        with self.assertRaises(AssertionError):
            BaseModel().is_truthy(False)
        with self.assertRaises(AssertionError):
            BaseModel().is_truthy(0)

    def test_not_empty(self):
        try:
            BaseModel().is_not_empty('fdsa')
            BaseModel().is_not_empty([1,2,3])
        except:
            self.fail('Error: data should not be empty / have length > 0')
        with self.assertRaises(AssertionError):
            BaseModel().is_not_empty([])
        with self.assertRaises(AssertionError):
            BaseModel().is_not_empty('')

    def test_is_date_string(self):
        try:
            BaseModel().is_date_string('Thu Nov 12 23:07:03 MST 2015')
        except:
            self.fail('Error: date string should be valid')
        try:
            BaseModel().is_date_string('wed feb 1 20:30:00 gmt 2016')
        except:
            self.fail('Error: date string should be valid')
        try:
            BaseModel().is_date_string('MON MAR 01 00:00:00 GMT 2017')
        except:
            self.fail('Error: date string should be valid')
        with self.assertRaises(Exception):
            BaseModel().is_date_string('Friday December 24 12:34:56 GMT 2015')
        with self.assertRaises(Exception):
            BaseModel().is_date_string('Sun Jan 32 23:00:00 GMT 1980')
        with self.assertRaises(Exception):
            BaseModel().is_date_string('Sat Apr 9 24:00:00 MST 2012')
        # TODO: This is a bug in python
        # This shouldn't raise an exception, it should be a valid date string
        # but it doesn't like 'PST', 'EST'
        #with self.assertRaises(Exception):
        #    BaseModel().is_date_string('Sat Aug 25 23:00:00 PST 2013')
        #with self.assertRaises(Exception):
        #    BaseModel().is_date_string('Tue Oct 10 10:50:46 EST 2012')
        with self.assertRaises(Exception):
            BaseModel().is_date_string(123)
        with self.assertRaises(Exception):
            BaseModel().is_date_string(True)
        with self.assertRaises(Exception):
            BaseModel().is_date_string(False)
        with self.assertRaises(Exception):
            BaseModel().is_date_string(123.123)

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
            BaseModel().is_string([1,2,3])
        with  self.assertRaises(AssertionError):
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
        #data_types = ['hello', 1, 1.5, True, [1,2,3], ['a','b','c']]
        #with self.assertRaises(AssertionError):
        #    for n in data_types:
        #        BaseModel().is_valid_email(n)
        with self.assertRaises(AssertionError):
            BaseModel().is_valid_email('hello')
        with self.assertRaises(Exception):
           BaseModel().is_valid_email(1)
        with self.assertRaises(Exception):
           BaseModel().is_valid_email(1.5)
        with self.assertRaises(Exception):
           BaseModel().is_valid_email(True)
        with self.assertRaises(Exception):
           BaseModel().is_valid_email([1,2,3])
        with self.assertRaises(Exception):
           BaseModel().is_valid_email(['a','b','c'])

    def test_is_list(self):
        try:
            BaseModel().is_list([1,2,3])
        except:
            self.fail('Error: [1,2,3] should be a valid list')
        try:
            BaseModel().is_list(['a'])
        except:
            self.fail('Error: this should be a valid list of one string entry')
        try:
            BaseModel().is_list(['hello', 1, 2.5, False, [1,2,3]])
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

    def test_is_user(self):
        # look into this method, its giving me error 'db is note defined'
        #try:
        #    BaseModel().is_user(123456)
        #except:
        #    self.fail('Error: user is not in database')
        pass

    def test_is_content_node(self):
        pass

    def test_is_user_node(self):
        pass

    def test_is_in_list(self):
        try:
            BaseModel().is_in_list([1,2,3])(1)
            BaseModel().is_in_list([1,2,3])(2)
            BaseModel().is_in_list([1,2,3])(3)
            f = BaseModel().is_in_list([1,2,3])
            f(1)
            f(2)
            f(3)
        except:
            self.fail('Error: is_in_list should work with integers')
        try:
            BaseModel().is_in_list([1.2,2.3,3.4])(1.2)
            BaseModel().is_in_list([1.2,2.3,3.4])(2.3)
            BaseModel().is_in_list([1.2,2.3,3.4])(3.4)
            f = BaseModel().is_in_list([1.2,2.3,3.4])
            f(1.2)
            f(2.3)
            f(3.4)
        except:
            self.fail('Error: is_in_list should work with floats')
        try:
            BaseModel().is_in_list(['hello', 'world', 'KITTY'])('hello')
            BaseModel().is_in_list(['hello', 'world', 'KITTY'])('world')
            BaseModel().is_in_list(['hello', 'world', 'KITTY'])('KITTY')
            BaseModel().is_in_list(['hello', 'world', 'KITTY'])('KITTY')
            f = BaseModel().is_in_list(['hello', 'world', 'KITTY'])
            f('hello')
            f('world')
            f('KITTY')
        except:
            self.fail('Error: is_in_list should work with strings')
        test_list = BaseModel.is_in_list(['Hello', 'World'])
        with self.assertRaises(AssertionError):
            test_list('hello')
        with self.assertRaises(AssertionError):
            test_list('world')

    def test_is_in_range(self):
        try:
            BaseModel().is_in_range(0,4)(2)
            test_range = BaseModel().is_in_range(0,4)
            test_range(0)
            test_range(1)
            test_range(2)
            test_range(3)
            test_range(4)
        except:
            self.fail('Error: is_in_range should work with integers')
        try:
            BaseModel().is_in_range(0,4.5)(2.2)
            test_range = BaseModel().is_in_range(0,4.5)
            test_range(0.5)
            test_range(1.9)
            test_range(2.2456767)
            test_range(3.9999)
            test_range(4.4999999)
        except:
            self.fail('Error: is_in_range should work with floats')
        test_range = BaseModel().is_in_range(0.5,4.5)
        with self.assertRaises(AssertionError):
            test_range(0.49)
        with self.assertRaises(AssertionError):
            test_range(4.50001)

    def test_schema_recurse(self):
        #try:
        #    schema = BaseModel().schema_recurse(Answer().fields(), Answer().requiredFields())
        #except:
        #    self.fail('Error: check the schema of answer model')
        pass

    def test_schema_or(self):
        pass

    def test_requiredFields(self):
        #try:
        #    print(Answer().requiredFields())
        #except:
        #    self.fail('Error: Did not return valid answer model required fields')
        pass

    def test_isValid(self):
        pass

    def test_get_item(self):
        # How do I get the table name to be what I want?
        #try:
        #    BaseModel().table = 'User'
        #    print(BaseModel().get_item('20efb55a-2dcb-4210-8fcc-b45624bce472'))
        #except:
        #    self.fail('Error: get_item doesnt work')
        pass

    def test_find(self):
        # guess this method can use either the rethinkdb key or any table column name
        # this works, but I do not know how to specify table name
        #try:
        #    print(BaseModel().find('user_id'))
        #except:
        #    self.fail('Error: find doesnt work')
        pass


    def test_create_item(self):
        # this does work, but how do you specify the table name?
        #try:
        #    User().create_item({'user_id':789})
        #except:
        #    self.fail('Error: create_item didnt work')
        pass

if __name__ == '__main__':
    unittest.main()
