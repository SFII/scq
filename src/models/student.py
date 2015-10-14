from remodel.models import Model

class Student(Model):
    has_many = ('Section',)
