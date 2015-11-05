import subprocess
import os.path
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import logging
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

def main():
    init()
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    print("Listening for connections on localhost:{0}".format(options.port))
    tornado.ioloop.IOLoop.instance().start()

def init():
    logging.info("Connecting")
    try:
        logging.info("Creating DB")
        r.db_create(DB).run(conn)
    except:
        logging.info("database already exists")
    logging.info("Initializing tables")
    connection = BaseModel.conn
    Answer().init(connection)
    Course().init(connection)
    Instructor().init(connection)
    Question().init(connection)
    Section().init(connection)
    Student().init(connection)
    Survey().init(connection)
    User().init(connection)

if __name__ == "__main__":
    main()
