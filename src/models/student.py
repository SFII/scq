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
        return ['college']

    # must be overrriden
    def fields():
        b = super(User, self)
        return {
            'student_id' : (b.is_string, ),
            'email' : (b.is_string, b.is_valid_email, ),
            'college' : (b.is_in_list(REGISTRATION_METHODS), ),
            'majors' : (b.is_list, schema_list_check(is_major),),
            'minors' : (b.is_list, schema_list_check(is_minor),),
            'gpa' : (b.is_int, ),
            'course_history' : (b.is_list, ),
            'credits_earned' : (b.is_int, )
        }
