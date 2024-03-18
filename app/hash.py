import hashlib, os

def hash_password(password):
    hashpassword = hashlib.md5((password + os.getenv("SALT_PASSWORD")).encode()).hexdigest()
    return hashpassword
