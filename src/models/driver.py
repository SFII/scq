import rethinkdb as r
from tornado import gen
from tornado import ioloop

# import classes within the same directory
#from surveyresponse import SurveyResponse
from models.answer import Answer
from models.basemodel import BaseModel
from models.course import Course
from models.instructor import Instructor
from models.question import Question
from models.section import Section
from models.student import Student
from models.survey import Survey
from models.user import User

DB = "scq"

r.set_loop_type("tornado")
connection = r.connect(host='localhost', port=28015)

@gen.engine
def init():
    print("Connecting")
    conn = yield connection
    print("Connecting")
    try:
        print("Creating DB")
        yield r.db_create(DB).run(conn)
    except:
        print("database already exists")

    print("Initializing tables")
    conn.use(DB)
    Answer().init(conn)
    Course().init(conn)
    Instructor().init(conn)
    Question().init(conn)
    Section().init(conn)
    Student().init(conn)
    Survey().init(conn)
    User().init(conn)

@gen.coroutine
def user(data):
    conn = yield connection
    conn.use(DB)
    result = yield r.table('users').insert(
            data,
            conflict='update',
            ).run(conn)
    raise gen.Return(result)

    create_tables()
    create_indexes()

    test_course = Course.create(course_id='MATH-01', name='MATH 1300', department='mathematics', credit_hours=5)
    test_course['sections'].add(Section(name='8AM - DOE'), Section(name='2PM - CHANG'))
    print(Course.get_course_name(test_course))
    print(Course.get_department_name(test_course))
    print(Course.get_course_id(test_course))
    print(Course.get_credit_hours(test_course))


    s = Survey.create(name="another survey")
    s['questions'].add(Question(text="Do you think our teacher is good?", response_format="free response"))
    print(Survey.get(name="another survey"))
    #l = s['questions'].all()[0].get("text")

init()
