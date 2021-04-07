import hashlib
import secrets


def hash_password(pw: str) -> bytes:
    return hashlib.sha256(pw.encode()).digest()


def generate_token() -> str:
    return secrets.token_hex(16)
