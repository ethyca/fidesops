from enum import Enum

from pydantic import BaseModel


class SecretType(Enum):
    key = "key"
    salt = "salt"


class MaskingSecret(BaseModel):
    secret: str
    masking_strategy: str
    secret_type: SecretType


