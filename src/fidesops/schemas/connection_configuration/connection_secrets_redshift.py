from typing import Optional, List

from fidesops.schemas.connection_configuration.connection_secrets import (
    ConnectionConfigSecretsSchema,
)


class RedshiftSchema(ConnectionConfigSecretsSchema):
    """Schema to validate the secrets needed to connect to an Amazon Redshift cluster"""

    host: str  # Endpoint of the Amazon Redshift server
    port: Optional[int] = None
    database: Optional[str] = None
    user: str
    password: str

    _required_components: List[str] = ["host", "user", "password"]
