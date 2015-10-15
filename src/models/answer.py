from remodel.models import Model

class Answer(Model):
    has_one = ('Question', 'Response',)
    #belongs_to = ('Survey_respose',)
