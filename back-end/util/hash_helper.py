import hashlib


def hash_password(pw: str) -> bytes:
    return hashlib.sha256(pw.encode()).digest()
