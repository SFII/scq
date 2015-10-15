from remodel.models import Model

class Survey_response(Model):
    has_many = ('Answer',)
    has_one = ('User', 'Survey',)
