from typing import List

from fidesops.ops.schemas.base_class import NoValidationSchema
from fidesops.ops.schemas.connection_configuration.connection_secrets import (
    ConnectionConfigSecretsSchema,
)


class HttpsSchema(ConnectionConfigSecretsSchema):
    """Schema to validate the secrets needed to connect to a client api"""

    url: str
    authorization: str

    _required_components: List[str] = ["url", "authorization"]

    class Config:
        """Add example for each field"""
        schema_extra = {
            "example": {
                "url": "https://username:password@www.example.com/",
                "authorization": "Basic SAHdhdtfqywtef1256ftSADqw"
            }
        }


class HttpsDocsSchema(HttpsSchema, NoValidationSchema):
    """HTTPS Secrets Schema for API Docs"""
