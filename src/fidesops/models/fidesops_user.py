from sqlalchemy import Column, String
from sqlalchemy_utils import StringEncryptedType
from sqlalchemy_utils.types.encrypted.encrypted_type import AesGcmEngine

from fidesops.core.config import config
from fidesops.db.base_class import Base


class FidesopsUser(Base):
    """The DB ORM model for FidesopsUser"""

    username = Column(String, unique=True, index=True)
    password = Column(
        StringEncryptedType(
            String,
            config.security.APP_ENCRYPTION_KEY,
            AesGcmEngine,
            "pkcs5",
        ),
        nullable=False,
    )
