from __future__ import annotations

from datetime import datetime
from typing import Any

from fideslib.cryptography.cryptographic_util import generate_salt, hash_with_salt
from fideslib.db.base_class import Base
from fideslib.models.audit_log import AuditLog
from sqlalchemy import Column, DateTime, ForeignKey, String
from sqlalchemy.orm import Session, relationship

from fidesops.ops.models.privacy_request import ProvidedIdentity
from fidesops.ops.util.regulations import regulations


class Consent(Base):
    """The DB ORM model for Consent."""

    identity = Column(
        String, ForeignKey(ProvidedIdentity.id), nullable=False, unique=True
    )
    regulations = 

    username = Column(String, unique=True, index=True)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    hashed_password = Column(String, nullable=False)
    salt = Column(String, nullable=False)
    last_login_at = Column(DateTime(timezone=True), nullable=True)
    password_reset_at = Column(DateTime(timezone=True), nullable=True)

    # passive_deletes="all" prevents audit logs from having their
    # privacy_request_id set to null when a privacy_request is deleted.
    # We want to retain for record-keeping.
    audit_logs = relationship(
        AuditLog,
        backref="fides_user",
        lazy="dynamic",
        passive_deletes="all",
        primaryjoin="foreign(AuditLog.user_id)==FidesUser.id",
    )

    client = relationship(  # type: ignore
        "ClientDetail", backref="user", cascade="all, delete", uselist=False
    )

    @classmethod
    def hash_password(cls, password: str, encoding: str = "UTF-8") -> tuple[str, str]:
        """Utility function to hash a user's password with a generated salt"""
        salt = generate_salt()
        hashed_password = hash_with_salt(
            password.encode(encoding),
            salt.encode(encoding),
        )
        return hashed_password, salt
