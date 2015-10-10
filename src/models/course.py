from remodel.models import Model
class Course(Model):
    has_many = ('Section',)
