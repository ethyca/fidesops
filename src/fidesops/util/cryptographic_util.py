import math

import hashlib
import secrets
import bcrypt

from fidesops.core.config import config


def hash_with_salt(text: bytes, salt: bytes) -> str:
    """Hashes the text using SHA-512 with the provided salt and returns the hex string
    representation"""
    return hashlib.sha512(text + salt).hexdigest()


def generate_secure_random_string(length: int) -> str:
    """Generates a securely random string using Python secrets library that is the length of the specified input

    We halve the input here to create a string of specified length, since token_string returns a string
    twice as long as nbytes
    """
    return secrets.token_hex(math.floor(length / 2))


def generate_salt() -> str:
    """Generates a salt using bcrypt and returns a string using the configured default encoding"""
    return bcrypt.gensalt().decode(config.security.ENCODING)
