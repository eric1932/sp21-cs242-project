"""
Deal with user info security.
"""
import hashlib
import secrets


def hash_password(password: str) -> bytes:
    """
    hash the input using sha256 and return the bytes
    :param password: raw text of password
    :return: bytes as the hash
    """
    return hashlib.sha256(password.encode()).digest()


def generate_token() -> str:
    """
    generate a random token of 16 digits
    :return: a hex string with length of 16
    """
    return secrets.token_hex(16)
