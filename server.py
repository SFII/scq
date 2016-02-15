import subprocess
import os.path
import tornado.ioloop
import tornado.options
import tornado.web
import logging
import rethinkdb as r
import signal
import time
from tornado.httpserver import HTTPServer
from test.test_runner import run_tests
from config.application import make_application
from tornado import ioloop, gen
from tornado.concurrent import Future, chain_future
from tornado.options import define, options

application = None

define('debug', default=True, help='set True for debug mode', type=bool)
define('test', default=False, help='set True to run Tests', type=bool)
define('port', default=8000, help='run on the given port', type=int)
define('database_name', default='scq', help='rethink database name', type=str)
define('database_host', default='localhost', help='rethink database host', type=str)
define('database_port', default=28015, help='rethink database port', type=int)


def main():
    tornado.options.parse_command_line()
    application = make_application()
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
        return run_tests(application)
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


# def initialize_db(db=options.database_name):
#     """
#     Initializes a database for use in the project with a specified name
#     Specified name defaults to options.database_name
#     """
#     logging.info("Connecting")
#     try:
#         conn = r.connect(host=options.database_host, port=options.database_port)
#         BaseModel.DB = db
#         BaseModel.conn = conn
#         logging.info("Creating database '{0}'".format(db))
#         r.db_create(db).run(conn)
#     except r.errors.ReqlOpFailedError as e:
#         logging.warning(e.message)
#     except Exception as e:
#         logging.error(e.message)
#     logging.info('Initializing tables')
#     Course().init(db, conn)
#     Instructor().init(db, conn)
#     Question().init(db, conn)
#     Section().init(db, conn)
#     Student().init(db, conn)
#     Survey().init(db, conn)
#     User().init(db, conn)
#     SurveyResponse().init(db, conn)
#     QuestionResponse().init(db, conn)


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
