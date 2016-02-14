import subprocess
import os.path
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import logging
import rethinkdb as r
from config.config import application
from models.basemodel import BaseModel
from models.course import Course
from models.instructor import Instructor
from models.question import Question
from models.section import Section
from models.student import Student
from models.survey import Survey
from models.user import User
from models.survey_response import SurveyResponse
from models.question_response import QuestionResponse
from tornado import ioloop, gen
from tornado.concurrent import Future, chain_future
from tornado.options import define, options
import time

define('debug', default=True, help='set True for debug mode', type=bool)
define('test', default=False, help='set True to run Tests', type=bool)
define('port', default=8000, help='run on the given port', type=int)
define('database_name', default='scq', help='rethink database name', type=str)
define('database_host', default='localhost', help='rethink database host', type=str)
define('database_port', default=28015, help='rethink database port', type=int)

SETTINGS = {
    'cookie_secret': "8goWPH9uTyO+9e2NzuaW6pbR6WKH1EbmrXIfxttXq00=",
    'autoreload': True,
    'template_path': 'templates/',
    'static_path': 'static/',
    'login_url': '/login'
    'user': User(),
    'survey': Survey(),
    'question': Question(),
    'surveyResponse': SurveyResponse(),
    'questionResponse': QuestionResponse(),
    'instructor': Instructor(),
    'course': Course()
}

def initialize():
    settings['debug'] = options.debug
    settings['site_port'] = options.port
    database_name = options.database_name
    database_port = options.database_port
    database_host = options.database_host
    if options.debug:
        database_name += '_debug'
    if options.test:
        database_name += '_test'
    settings['database_name'] = database_name
    try:
        conn = r.connect(host=options.database_host, port=options.database_port)
        settings['conn'] = conn
        r.db_create(database_name).run(conn)
    except Exception as e:
        logging.warning(e.message)
    settings['user'].init(database_name, conn)
    settings['instructor'].init(database_name, conn)
    settings['course'].init(database_name, conn)
    settings['survey'].init(database_name, conn)
    settings['question'].init(database_name, conn)
    settings['questionResponse'].init(database_name, conn)
    settings['surveyResponse'].init(database_name, conn)
    settings['meta'] = settings['user'].get_item('meta')
    if settings['meta'] is None:
        meta_data = settings['user'].default()
        meta_data['id'] = 'meta'
        meta_data['registration'] = User().REGISTRATION_DENY
        meta_data['username'] = 'Campus Consensus Team'
        meta_data['accepted_tos'] = True
        meta_data['email'] = 'xxx@colorado.edu'
        settings[meta] = settings['user'].create_item(meta_data)


def main():
    tornado.options.parse_command_line()
    initialize()
    application = tornado.web.Application(handlers=routes, **settings)
    httpserver = HTTPServer(application, xheaders=True)
    MAX_WAIT_SECONDS_BEFORE_SHUTDOWN = 0

    # signal handler
    def sig_handler(sig, frame):
        logging.warn("Caught Signal: %s" % sig)
        tornado.ioloop.IOLoop.instance().add_callback(shutdown)

    # signal handler's callback
    def shutdown():
        logging.info("Stopping HttpServer ...")
        httpserver.stop()  # No longer accept new http traffic
        instance = tornado.ioloop.IOLoop.instance()
        deadline = time.time() + MAX_WAIT_SECONDS_BEFORE_SHUTDOWN
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
        testsuite = unittest.TestLoader().discover('test')
        return unittest.TextTestRunner(verbosity=2).run(testsuite)
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


def initialize_db(db=options.database_name):
    """
    Initializes a database for use in the project with a specified name
    Specified name defaults to options.database_name
    """
    logging.info("Connecting")
    try:
        conn = r.connect(host=options.database_host, port=options.database_port)
        BaseModel.DB = db
        BaseModel.conn = conn
        logging.info("Creating database '{0}'".format(db))
        r.db_create(db).run(conn)
    except r.errors.ReqlOpFailedError as e:
        logging.warning(e.message)
    except Exception as e:
        logging.error(e.message)
    logging.info('Initializing tables')
    Course().init(db, conn)
    Instructor().init(db, conn)
    Question().init(db, conn)
    Section().init(db, conn)
    Student().init(db, conn)
    Survey().init(db, conn)
    User().init(db, conn)
    SurveyResponse().init(db, conn)
    QuestionResponse().init(db, conn)


def bootstrap_data(user_id):
    initialize_db()
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
    initialize_db()
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
