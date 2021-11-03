from typing import List

from fidesops.schemas.base_class import DocsOnlySchema
from fidesops.schemas.connection_configuration.connection_secrets import (
    ConnectionConfigSecretsSchema,
)


class HttpsSchema(ConnectionConfigSecretsSchema):
    """Schema to validate the secrets needed to connect to a client api"""

    url: str
    authorization: str

    _required_components: List[str] = ["url", "authorization"]


class HttpsDocsSchema(HttpsSchema, DocsOnlySchema):
    """HTTPS Secrets Schema for API Docs"""
