from enum import Enum

from fidesops.schemas.base_class import BaseSchema


class SecretType(Enum):
    key = "key"
    salt = "salt"


class MaskingSecretGeneration(BaseSchema):
    secret: str
    masking_strategy: str
    secret_type: SecretType
