import hashlib

class Hashing:
    hashing256 = hashlib.sha256()
    def sha256(password):
        encoding = str.encode(password)
        hashing256.update(encoding)
        hashing256.digest()
