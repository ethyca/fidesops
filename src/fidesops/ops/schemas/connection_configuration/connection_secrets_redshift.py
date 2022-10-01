from typing import List, Optional

from fidesops.ops.schemas.base_class import NoValidationSchema
from fidesops.ops.schemas.connection_configuration.connection_secrets import (
    ConnectionConfigSecretsSchema,
)


class RedshiftSchema(ConnectionConfigSecretsSchema):
    """Schema to validate the secrets needed to connect to an Amazon Redshift cluster"""

    host: Optional[str] = None  # Endpoint of the Amazon Redshift server
    port: Optional[int] = None
    database: Optional[str] = None
    user: Optional[str] = None
    password: Optional[str] = None
    db_schema: Optional[str] = None

    _required_components: List[str] = ["host", "user", "password"]

    class Config:
        """Add example for each field"""
        schema_extra = {
            "example": {
                "host": "localhost",
                "port": 5439,
                "database": "my_db",
                "user": "Mahmoud",
                "password": "my_super_duper_secret_password",
                "db_schema": "test_schema",
            }
        }


class RedshiftDocsSchema(RedshiftSchema, NoValidationSchema):
    """Redshift Secrets Schema for API Docs"""
