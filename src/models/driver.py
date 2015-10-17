import rethinkdb as r

# import classes within the same directory
from course import Course
from section import Section
from user import User
from question import Question
from survey import Survey

DB = "scq"

r.set_loop_type("tornado")

@gen.engine
def init():
    conn = yield connection
    print "Connecting"
    try:
        print "Creating DB"
        yield r.db_create(DB).run(conn)
    except:
        print "database already exists"
    print "initializing"
    conn.use(DB)
    Course.init()
    User.init()
    Section.init()
    Question.init()
    Survey.init()

ioloop.IOLoop().instance().add_callback(init)

@gen.coroutine
def exists(table, ):
    conn = yield connection
    conn.use(DB)
    result = yield r.table('users').insert(
            data,
            conflict='update',
            ).run(conn)
    raise gen.Return(result)

def main():
    connection = r.connect(host='localhost', port=28015)

    #create_indexes()

    # Test out course
    #test_course = Course.create(name='MATH 1300')
    #id = [['math01', 'math 1300', 5]
    #     ['biol1', 'biolo 1100', 4]]
    #course_id_list =
    test_course = Course.create(course_id='MATH-01', name='MATH 1300', department='mathematics', credit_hours=5)
    test_course['sections'].add(Section(name='8AM - DOE'), Section(name='2PM - CHANG'))
    print Course.get_course_name(test_course)
    print Course.get_department_name(test_course)
    print Course.get_course_id(test_course)
    print Course.get_credit_hours(test_course)
    print Course.get_section_count(test_course)


    # Test out Survey/Question
    create_tables()
    s = Survey.create(name="another survey")
    s['questions'].add(Question(text="Does our teacher suck?", response_format="free response"))

    # Test out section
    #test_section = Section.create(section_id='001', course_id='MATH-01', course_name='MATH 1300', department_name='mathematics', credit_hours=5)
    #print Section.get_section_id(test_section)
    #print Section.get_course_id(test_section)
    #print Section.get_course_name(test_section)
    #print Section.get_department_name(test_section)
    #print Section.get_credit_hours(test_section)


if __name__ == '__main__':
	main()
