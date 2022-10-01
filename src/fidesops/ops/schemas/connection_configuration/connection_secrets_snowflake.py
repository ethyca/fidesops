from typing import List, Optional

from fidesops.ops.schemas.base_class import NoValidationSchema
from fidesops.ops.schemas.connection_configuration.connection_secrets import (
    ConnectionConfigSecretsSchema,
)


class SnowflakeSchema(ConnectionConfigSecretsSchema):
    """Schema to validate the secrets needed to connect to Snowflake"""

    user_login_name: Optional[str] = None
    password: Optional[str] = None
    account_identifier: Optional[
        str
    ] = None  # Do not include the snowflakecomputing.com domain name as part of your account identifier.
    database_name: Optional[str] = None
    schema_name: Optional[str] = None
    warehouse_name: Optional[str] = None
    role_name: Optional[str] = None

    _required_components: List[str] = [
        "user_login_name",
        "password",
        "account_identifier",
    ]

    class Config:
        """Add example for each field"""
        schema_extra = {
            "example": {
                "user_login_name": "Mahmoud",
                "password": "my_super_duper_secret_password",
                "account_identifier": "account_identifier",
                "database_name": "my_db",
                "schema_name": "test_schema",
                "warehouse_name": "testing",
                "role_name": "test_role",
            }
        }


class SnowflakeDocsSchema(SnowflakeSchema, NoValidationSchema):
    """Snowflake Secrets Schema for API Docs"""
