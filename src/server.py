import subprocess
import os.path
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import logging
import rethinkdb as r
from models.answer import Answer
from models.basemodel import BaseModel
from models.course import Course
from models.instructor import Instructor
from models.question import Question
from models.section import Section
from models.student import Student
from models.survey import Survey
from models.user import User
from tornado import ioloop, gen
from tornado.concurrent import Future, chain_future
from tornado.options import define, options
from config.config import application
import time


def main():
    initialize_db()
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    print("Listening for connections on localhost:{0}".format(options.port))
    tornado.ioloop.IOLoop.instance().start()

def initialize_db():
    logging.info("Connecting")
    try:
        connection = BaseModel.conn
        DB = BaseModel.DB
        logging.info("Creating DB")
        r.db_create(DB).run(connection)
    except r.errors.ReqlOpFailedError as e:
        logging.info(e.message)
    except Exception as e:
        logging.error(e.message)

    logging.info("Initializing tables")
    Answer().init(connection)
    Course().init(connection)
    Instructor().init(connection)
    Question().init(connection)
    Section().init(connection)
    Student().init(connection)
    Survey().init(connection)
    User().init(connection)

def bootstrap_data():
    user_id = 'e64ad721-964a-436f-86c1-a516518c1440'
    user_data = User().get_item(user_id)
    if user_data is None:
        print("user_id {0} does not correspond to a valid user in the database!".format(user_id))
        return
    course_id = Course().create_generic_item()
    Course().subscribe_user(user_id, course_id)
    survey_id = Survey().create_generic_item(user_id, course_id)
    print('survey id:\n'+survey_id)
    return




if __name__ == "__main__":
    main()
