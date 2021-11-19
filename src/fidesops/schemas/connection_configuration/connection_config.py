from datetime import datetime
from typing import Optional, List

from fideslang.validation import FidesKey
from pydantic import BaseModel, Extra

from fidesops.schemas.api import BulkResponse, BulkUpdateFailed
from fidesops.models.connectionconfig import ConnectionType, AccessLevel


class CreateConnectionConfiguration(BaseModel):
    """
    Schema for creating a ConnectionConfiguration

    Note that secrets are *NOT* allowed to be supplied here.
    """

    name: str
    key: Optional[FidesKey]
    connection_type: ConnectionType
    access: AccessLevel

    class Config:
        """Restrict adding other fields through this schema and set orm_mode to support mapping to ConnectionConfig"""

        orm_mode = True
        use_enum_values = True
        extra = Extra.forbid


class ConnectionConfigurationResponse(BaseModel):
    """
    Describes the returned schema for a ConnectionConfiguration.

    Do *NOT* add "secrets" to this schema.
    """

    name: str
    key: FidesKey
    connection_type: ConnectionType
    access: AccessLevel
    created_at: datetime
    updated_at: Optional[datetime]
    last_test_timestamp: Optional[datetime]
    last_test_succeeded: Optional[bool]

    class Config:
        """Set orm_mode to support mapping to ConnectionConfig"""

        orm_mode = True


class BulkPutConnectionConfiguration(BulkResponse):
    """Schema with mixed success/failure responses for Bulk Create/Update of ConnectionConfiguration responses."""

    succeeded: List[ConnectionConfigurationResponse]
    failed: List[BulkUpdateFailed]
