from sqlalchemy import (
    Column,
    ForeignKey,
    String,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.mutable import MutableDict

from fidesops.models.connectionconfig import ConnectionConfig


class SaaSConnectionConfig(ConnectionConfig):
    """An extension of the base ConnectionConfig used to store SaaS Connector configs"""

    connection_config_id = Column(
        String, ForeignKey(ConnectionConfig.id_field_path), nullable=False
    )
    fides_key = Column(String, index=True, unique=True, nullable=False)
    saas_config = Column(
        MutableDict.as_mutable(JSONB), index=False, unique=False, nullable=False
    )
