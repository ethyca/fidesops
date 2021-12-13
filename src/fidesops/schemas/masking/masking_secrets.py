from enum import Enum
from typing import TypeVar, Generic, Callable

from fidesops.schemas.base_class import BaseSchema


T = TypeVar("T")


class SecretType(Enum):
    """Enum that holds all possible types of secrets across all masking strategies"""
    key = "key"
    salt = "salt"
    # the below types are used by the AES algorithm, when it calls HMAC to generate the nonce
    key_hmac = "key_hmac"
    salt_hmac = "salt_hmac"


class MaskingSecretMeta(BaseSchema, Generic[T]):
    """Holds metadata describing one secret"""
    masking_strategy: str
    secret_type: SecretType
    generate_secret: Callable[[], T]


class MaskingSecretCache(BaseSchema, Generic[T]):
    """Information required to cache a secret"""
    secret: T
    masking_strategy: str
    secret_type: SecretType
