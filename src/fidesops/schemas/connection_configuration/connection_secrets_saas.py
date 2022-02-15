from typing import List
from pydantic import Extra

from fidesops.schemas.base_class import NoValidationSchema
from fidesops.schemas.connection_configuration.connection_secrets import (
    ConnectionConfigSecretsSchema,
)


class SaaSSchema(ConnectionConfigSecretsSchema):
    """Schema to validate the secrets needed to connect to a SaaS API"""

    _required_components: List[str] = []

    class Config:
        """Only permit selected secret fields to be stored."""

        extra = Extra.allow
        orm_mode = True


class SaaSDocsSchema(SaaSSchema, NoValidationSchema):
    """SaaS Secrets Schema for API Docs"""
