from tornado.testing import AsyncHTTPTestCase
import unittest


def run_tests(application):
    BaseAsyncTest.application = application
    BaseAsyncTest.database_name = application.settings['database_name']
    BaseAsyncTest.conn = application.settings['conn']
    testsuite = unittest.TestLoader().discover('test')
    return unittest.TextTestRunner(verbosity=2).run(testsuite)


class BaseAsyncTest(AsyncHTTPTestCase):
    application = None
    conn = None
    database_name = ''

    def get_app(self):
        return self.application
