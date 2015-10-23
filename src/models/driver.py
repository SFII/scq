import rethinkdb as r
from tornado import gen
from tornado import ioloop

# import classes within the same directory
from answer import Answer
from basemodel import BaseModel
from course import Course
from instructor import Instructor
from question import Question
from section import Section
from student import Student
from survey import Survey
from surveyresponse import SurveyResponse
from user import User

DB = "scq"

r.set_loop_type("tornado")
connection = r.connect(host='localhost', port=28015)

@gen.engine
def init():
    conn = yield connection
    print "Connecting"
    try:
        print "Creating DB"
        yield r.db_create(DB).run(conn)
    except:
        print "database already exists"

    print "Initializing tables"
    conn.use(DB)
    Answer.init()
    Course.init()
    Instructor.init()
    Question.init()
    Section.init()
    Student.init()
    Survey.init()
    SurveyResponse.init()
    User.init()

ioloop.IOLoop().instance().add_callback(init)

@gen.coroutine
def user(data):
    conn = yield connection
    conn.use(DB)
    result = yield r.table('users').insert(
            data,
            conflict='update',
            ).run(conn)
    raise gen.Return(result)

