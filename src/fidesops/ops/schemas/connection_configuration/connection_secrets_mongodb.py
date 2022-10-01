from typing import List, Optional

from fidesops.ops.schemas.base_class import NoValidationSchema
from fidesops.ops.schemas.connection_configuration.connection_secrets import (
    ConnectionConfigSecretsSchema,
)


class MongoDBSchema(ConnectionConfigSecretsSchema):
    """Schema to validate the secrets needed to connect to a MongoDB Database"""

    username: Optional[str] = None
    password: Optional[str] = None
    host: Optional[str] = None
    port: Optional[int] = None
    defaultauthdb: Optional[str] = None

    _required_components: List[str] = ["host"]

    class Config:
        """Add example for each field"""
        schema_extra = {
            "example": {
                "username": "Mahmoud",
                "password": "my_super_duper_secret_password",
                "host": "localhost",
                "port": 27017,
                "defaultauthdb": "SCRAM-SHA-256"
            }
        }


class MongoDBDocsSchema(MongoDBSchema, NoValidationSchema):
    """Mongo DB Secrets Schema for API docs"""
