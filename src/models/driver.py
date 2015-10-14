import rethinkdb as r
from remodel.models import Model
from remodel.helpers import create_tables, create_indexes

# import classes within the same directory
from course import Course
from section import Section
from user import User
from question import Question
from survey import Survey

def main():
    #conn = r.connect(host='localhost', port=28015, db='testdb')

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
