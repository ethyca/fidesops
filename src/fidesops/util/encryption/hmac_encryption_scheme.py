import base64
import hashlib
import hmac
from typing import Optional, Callable

from cryptography.hazmat.primitives.ciphers.aead import AESGCM

from fidesops.core.config import config
from fidesops.schemas.masking.masking_configuration import HmacMaskingConfiguration
from fidesops.util.cryptographic_util import bytes_to_b64_str


# def encrypt_to_bytes(plain_value: Optional[str], key: bytes, nonce: bytes) -> bytes:
#     """Encrypts the value using the AES GCM Algorithm. Note that provided nonce must be 12 bytes.
#     Returns encrypted value in bytes"""
#     if plain_value is None:
#         raise ValueError("plain_value cannot be null")
#     verify_encryption_key(key)
#     verify_nonce(nonce)
#
#     gcm = AESGCM(key)
#     value_bytes = plain_value.encode(config.security.ENCODING)
#     encrypted_bytes = gcm.encrypt(nonce, value_bytes, nonce)
#     return encrypted_bytes
#
#
# def encrypt(plain_value: Optional[str], key: bytes, nonce: bytes) -> str:
#     """Encrypts the value using the HMAC Algorithm. Note that provided nonce must be 12 bytes.
#     Returns encrypted value as a string"""
#     encrypted: bytes = encrypt_to_bytes(plain_value, key, nonce)
#     return bytes_to_b64_str(encrypted)
#


def hmac_encrypt_return_bytes(value: str, hmac_key: str, salt: str, hashing_algorithm: HmacMaskingConfiguration.Algorithm) -> bytes:
    return _hmac_encrypt(value, hmac_key, salt, hashing_algorithm).digest()


def hmac_encrypt_return_str(value: str, hmac_key: str, salt: str, hashing_algorithm: HmacMaskingConfiguration.Algorithm) -> str:
    return _hmac_encrypt(value, hmac_key, salt, hashing_algorithm).hexdigest()


def _hmac_encrypt(value: str, hmac_key: str, salt: str, hashing_algorithm: HmacMaskingConfiguration.Algorithm) -> hmac.HMAC:
    """Generic HMAC algorithm"""

    algorithm_function_mapping = {
        HmacMaskingConfiguration.Algorithm.sha_256: _hmac_sha256,
        HmacMaskingConfiguration.Algorithm.sha_512: _hmac_sha512,
    }

    algorithm_function: Callable = algorithm_function_mapping.get(hashing_algorithm)
    return algorithm_function(value, hmac_key, salt)


def _hmac_sha256(value: str, hmac_key: str, salt: str) -> hmac.HMAC:
    """Creates a new hmac object using the sh256 hash algorithm and the hmac_key and then returns the hexdigest."""
    return _hmac(
        value=value, hmac_key=hmac_key, salt=salt, hashing_alg=hashlib.sha256
    )


def _hmac_sha512(value: str, hmac_key: str, salt: str) -> hmac.HMAC:
    """Creates a new hmac object using the sha512 hash algorithm and the hmac_key and then returns the hexdigest."""
    return _hmac(
        value=value, hmac_key=hmac_key, salt=salt, hashing_alg=hashlib.sha512
    )


def _hmac(value: str, hmac_key: str, salt: str, hashing_alg: Callable) -> hmac.HMAC:
    return hmac.new(
        key=hmac_key.encode(config.security.ENCODING),
        msg=(value + salt).encode(config.security.ENCODING),
        digestmod=hashing_alg,
    )


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
