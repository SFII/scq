from models.basemodel import BaseModel

class Student(BaseModel):
    'college'
    'majors'
    'minors'
    'gpa'
    'course_history'
    'academic_years'
    'credits_earned'
    COLLEGE_ARTS_AND_SCIENCES = 'College of Arts and Sciences'
    COLLEGE_ENGINEERING = 'College of Engineering and Applied Science'
    COLLEGE_BUSINESS = 'Leeds School of Business'
    COLLEGE_EDUCATION = 'School of Education'
    COLLEGE_GRAD = 'Graduate School'
    COLLEGE_LAW = 'School of Law'
    COLLEGE_MEDIA = 'College of Media, Communication and Information'
    COLLEGE_MUSIC = 'College of Music'
    COLLEGE_CONTINUE = 'Continuing Education and Professional Studies'
    COLLEGE_ENVIRONMENTAL = 'Program in Environmental Design'
    COLLEGES = [COLLEGE_ARTS_AND_SCIENCES, COLLEGE_ENGINEERING, COLLEGE_BUSINESS, COLLEGE_EDUCATION, COLLEGE_GRAD, COLLEGE_LAW, COLLEGE_MEDIA, COLLEGE_MUSIC, COLLEGE_CONTINUE, COLLEGE_ENVIRONMENTAL]

    def is_major(data):
        pass

    def is_minor(data):
        pass

    # must be overridden
    def requiredFields():
        super + ['student_id', 'college']

    # must be overrriden
    def fields():
        super.update({
            'student_id' : (is_int, ),
            'email' : (is_string, is_valid_email, ),
            'college' : (is_in_list(REGISTRATION_METHODS), ),
            'majors' : (is_list, schema_list_check(is_major),),
            'minors' : (is_list, schema_list_check(is_minor),),
            'gpa' : (is_int, ),
            'course_history' : (is_list, ),
            'credits_earned' : (is_int, )
        })
