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

define('port', default=8000, help='run on the given port', type=int)
define('database_name', default='scq', help='rethink database name', type=str)
define('database_host', default='localhost', help='rethink database host', type=str)
define('database_port', default=28015, help='rethink database port', type=int)


def main():
    tornado.options.parse_command_line()
    initialize_db()
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    logging.info("Listening for connections on localhost:{0}".format(options.port))
    tornado.ioloop.IOLoop.instance().start()


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
    update_response = User().update_item(user_id, user_data)
    logging.info(update_response)
    return

if __name__ == "__main__":
    main()
