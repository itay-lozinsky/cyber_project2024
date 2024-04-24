import hashlib


def encrypted_password(password):

    return hashlib.md5(password.encode()).hexdigest()[::-1]