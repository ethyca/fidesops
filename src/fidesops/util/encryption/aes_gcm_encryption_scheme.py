import base64
from typing import Optional

from cryptography.hazmat.primitives.ciphers.aead import AESGCM

from fidesops.core.config import config


def encrypt(plain_value: Optional[str], key: bytes, nonce: bytes) -> str:
    """Encrypts the value using the AES GCM Algorithm. Note that provided nonce must be 12 bytes"""
    if plain_value is None:
        raise ValueError("plain_value cannot be null")
    verify_encryption_key(key)
    verify_nonce(nonce)

    gcm = AESGCM(key)
    value_bytes = plain_value.encode(config.security.ENCODING)
    encrypted_bytes = gcm.encrypt(nonce, value_bytes, nonce)
    encrypted_str = base64.b64encode(encrypted_bytes).decode(config.security.ENCODING)
    return encrypted_str


def decrypt(encrypted_value: str, key: bytes, nonce: bytes) -> str:
    """Decrypts the value using the AES GCM Algorithm"""
    verify_encryption_key(key)
    verify_nonce(nonce)

    gcm = AESGCM(key)
    encrypted_bytes = base64.b64decode(encrypted_value)
    decrypted_bytes = gcm.decrypt(nonce, encrypted_bytes, nonce)
    decrypted_str = decrypted_bytes.decode(config.security.ENCODING)
    return decrypted_str


def verify_nonce(nonce: bytes) -> None:
    if len(nonce) != config.security.AES_GCM_NONCE_LENGTH:
        raise ValueError(
            f"Nonce must be {config.security.AES_GCM_NONCE_LENGTH} bytes long"
        )


def verify_encryption_key(key: bytes) -> None:
    if len(key) != config.security.AES_ENCRYPTION_KEY_LENGTH:
        raise ValueError(
            f"Encryption key must be {config.security.AES_ENCRYPTION_KEY_LENGTH} bytes long"
        )
