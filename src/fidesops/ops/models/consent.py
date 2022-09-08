from __future__ import annotations

from fideslib.db.base_class import Base
from sqlalchemy import Boolean, Column, Enum, ForeignKey, String
from sqlalchemy.orm import backref, relationship

from fidesops.ops.models.privacy_request import ProvidedIdentity
from fidesops.ops.util.regulations import Regulations


class Consent(Base):
    """The DB ORM model for Consent."""

    identity = Column(
        String, ForeignKey(ProvidedIdentity.id), nullable=False, unique=True
    )
    regulation = Column(Enum(Regulations))
    data_use = Column(String)
    data_use_description = Column(String)
    opt_in = Column(Boolean, nullable=False)

    privided_identity = relationship(
        ProvidedIdentity,
        backref=backref("consent", cascade="all, delete-orphan"),
    )
