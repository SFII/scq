from tornado.options import define, options
from tornado.web import Application
from config.routes import routes
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
import logging
import rethinkdb as r

settings = {
    'cookie_secret': "8goWPH9uTyO+9e2NzuaW6pbR6WKH1EbmrXIfxttXq00=",
    'autoreload': True,
    'template_path': 'templates/',
    'static_path': 'static/',
    'login_url': '/login',
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
    if options.test:
        database_name += '_test'
    elif options.debug:
        database_name += '_debug'
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
        settings['meta'] = settings['user'].create_item(meta_data, skip_verify=True)


def make_application():
    initialize()
    return Application(handlers=routes, **settings)
