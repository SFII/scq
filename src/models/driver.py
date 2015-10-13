import rethinkdb as r
from remodel.models import Model
from remodel.helpers import create_tables, create_indexes

# import classes within the same directory
from course import Course
from section import Section


def main():
    conn = r.connect(host='localhost', port=28015, db='testdb')

    # Creates all database tables defined by models
    create_tables()
    # Creates all table indexes based on model relations
    create_indexes()

    test_course = course.create(name='MATH 1300')
    test_course['sections'].add(section(name='8AM - DOE'), section(name='2PM - CHANG'))
    
    print section.section_count()
    print "did it work?"





if __name__ == '__main__':
	main()
