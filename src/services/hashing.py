import hashlib


def sha256(password):
    # encoding = str.encode(password)
    hashing256 = hashlib.sha256()
    hashing256.update(password)
    return hashing256.hexdigest()
