from remodel.models import Model

class Survey(Model):
    has_many = ('Question', 'Instructor',)
    has_one = ('Course', 'Creator',)
