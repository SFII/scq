from remodel.models import Model

class Instructor(Model):
    has_many = ('Section',)
