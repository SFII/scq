import subprocess
import os.path
import tornado.ioloop
import tornado.options
import tornado.web
import logging
import rethinkdb as r
import signal
import time
from handlers.base_handler import BaseHandler
from models.basemodel import BaseModel
from models.course import Course
from models.instructor import Instructor
from models.question import Question
from models.section import Section
from models.student import Student
from models.survey import Survey
from models.user import User
from tornado.httpserver import HTTPServer
from test.test_runner import run_tests
from config.application import make_application, initialize_settings
from tornado import ioloop, gen
from tornado.concurrent import Future, chain_future
from tornado.options import define, options

application = None
settings = {}

define('debug', default=True, help='set True for debug mode', type=bool)
define('test', default=False, help='set True to run Tests', type=bool)
define('wipe_user_data', default=False, help='set True to violently wipe user survey and course data', type=bool)
define('bootstrap_data', default=False, help='set True to provision a user with surveys and courses', type=bool)
define('port', default=8000, help='run on the given port', type=int)
define('database_name', default='scq', help='rethink database name', type=str)
define('database_host', default='localhost', help='rethink database host', type=str)
define('database_port', default=28015, help='rethink database port', type=int)


def main():
    tornado.options.parse_command_line()
    settings = initialize_settings()
    application = make_application(settings)
    httpserver = HTTPServer(application, xheaders=True)

    # signal handler
    def sig_handler(sig, frame):
        logging.warn("Caught Signal: %s" % sig)
        tornado.ioloop.IOLoop.instance().add_callback(shutdown)

    # signal handler's callback
    def shutdown():
        logging.info("Stopping HttpServer ...")
        httpserver.stop()  # No longer accept new http traffic
        instance = tornado.ioloop.IOLoop.instance()
        deadline = time.time() + settings['sigint_timeout']
        # recursion for terminate IOLoop.instance()

        def terminate():
            now = time.time()
            if now < deadline and (instance._callbacks or instance._timeouts):
                instance.add_timeout(now + 1, terminate)
            else:
                instance.stop()  # After process all _callbacks and _timeouts, break IOLoop.instance()
                logging.info('Shutdown ...')
        # process recursion
        terminate()
    if options.test:
        return run_tests(application)
    if options.bootstrap_data or options.wipe_user_data:
        username = input("please input username: ")
        cursor = User().find_item({'username': username})
        for user_data in cursor:
            user_id = user_data['id']
            logging.info('user_id: ' + user_id)
            if options.wipe_user_data:
                return wipe_data(user_id)
            if options.bootstrap_data:
                return bootstrap_data(user_id)
        return logging.error('no found user with username: ' + username)
    if options.debug:
        httpserver.listen(settings['site_port'])
        signal.signal(signal.SIGINT, sig_handler)
        signal.signal(signal.SIGTERM, sig_handler)
    else:
        httpserver.bind(settings['site_port'])  # port
        httpserver.start(0)
    logging.info("Now serving on http://localhost:{0}".format(settings['site_port']))
    tornado.ioloop.IOLoop.instance().start()
    logging.info('Exit ...')


def bootstrap_data(user_id):
    """
    Creates new course and survey objects, and associates all of this data
    """
    user_data = User().get_item(user_id)
    if user_data is None:
        logging.error("user_id {0} does not correspond to a valid user in the database!".format(user_id))
        return
    course_id = Course().create_generic_item()
    Course().subscribe_user(user_id, course_id)
    survey_id = Survey().create_generic_item(user_id, course_id)
    logging.info('survey id:\n' + survey_id)
    return


def wipe_data(user_id):
    """
    Wipes the data associated with a users surveys, classes and courses
    Warning: Does not disassociate surveys with courses, user with courses, etc.
    It just makes a user fresh and ready for new data
    """
    user_data = User().get_item(user_id)
    if user_data is None:
        logging.error("user_id {0} does not correspond to a valid user in the database!".format(user_id))
        return
    user_data['courses'] = []
    user_data['created_surveys'] = []
    user_data['unanswered_surveys'] = []
    update_response = User().update_item(user_id, user_data, skip_verify=True)
    logging.info(update_response)
    return

if __name__ == "__main__":
    main()
