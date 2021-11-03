from typing import Optional, List

from fidesops.schemas.base_class import DocsOnlySchema
from fidesops.schemas.connection_configuration.connection_secrets import (
    ConnectionConfigSecretsSchema,
)


class PostgreSQLSchema(ConnectionConfigSecretsSchema):
    """Schema to validate the secrets needed to connect to a PostgreSQL Database"""

    username: Optional[str] = None
    password: Optional[str] = None
    dbname: Optional[str] = None
    host: Optional[
        str
    ] = None  # Either the entire "url" *OR* the "host" should be supplied.
    port: Optional[int] = None

    _required_components: List[str] = ["host"]


class PostgreSQLDocsSchema(PostgreSQLSchema, DocsOnlySchema):
    """Postgres Secrets Schema for API Docs"""
