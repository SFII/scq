import subprocess
import os.path
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import logging
import rethinkdb as r
from config.config import application
from models.answer import Answer
from models.basemodel import BaseModel
from models.course import Course
from models.instructor import Instructor
from models.question import Question
from models.section import Section
from models.student import Student
from models.survey import Survey
from models.user import User
from models.response import Response
from tornado import ioloop, gen
from tornado.concurrent import Future, chain_future
from tornado.options import define, options
import time

def main():
    initialize_db()
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    print("Listening for connections on localhost:{0}".format(options.port))
    tornado.ioloop.IOLoop.instance().start()

def initialize_db(db = options.database_name):
    """
    Initializes a database for use in the project with a specified name
    Specified name defaults to options.database_name
    """
    logging.info("Connecting")
    try:
        conn = r.connect(host=options.database_host, port=options.database_port)
        BaseModel.DB = db
        BaseModel.conn = conn
        print("Creating database '{0}'".format(db))
        r.db_create(db).run(conn)
    except r.errors.ReqlOpFailedError as e:
        print(e.message)
    except Exception as e:
        logging.error(e.message)
    print('Initializing tables')
    Answer().init(db, conn)
    Course().init(db, conn)
    Instructor().init(db, conn)
    Question().init(db, conn)
    Section().init(db, conn)
    Student().init(db, conn)
    Survey().init(db, conn)
    User().init(db, conn)
    Response().init(db, conn)

def bootstrap_data(user_id):
    initialize_db()
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
