from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.mutable import MutableDict

from fidesops.models.connectionconfig import ConnectionConfig, ConnectionType


class SaaSConnectionConfig(ConnectionConfig):
    """Extends the base ConnectionConfig to be able to store the SaaS config schema"""

    id = Column(String, ForeignKey(ConnectionConfig.id), nullable=False)
    saas_config = Column(
        MutableDict.as_mutable(JSONB), index=False, unique=False, nullable=False
    )

    __mapper_args__ = {"polymorphic_identity": ConnectionType.saas}
