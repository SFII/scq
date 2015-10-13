from remodel.models import Model
from services import hashing
class User(Model):
    HASHEDPASSWORDKEY = 'hashedpassword_sha256'

    def validatePassword(password):
        hashedpassword = hashing.sha256(password)
        return self[HASHEDPASSWORDKEY] == hashedpassword
