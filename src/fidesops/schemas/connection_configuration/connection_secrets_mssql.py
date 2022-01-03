from typing import Optional, List

from fidesops.schemas.base_class import NoValidationSchema
from fidesops.schemas.connection_configuration.connection_secrets import (
    ConnectionConfigSecretsSchema,
)


class MicrosoftSQLServerSchema(ConnectionConfigSecretsSchema):
    """Schema to validate the secrets needed to connect to a MS SQL Database

    connection string takes the format:
    mssql+pyodbc://[username]:[password]@[host]:[port_no]/[database_name]?driver=ODBC+Driver+17+for+SQL+Server

    """

    username: Optional[str] = None
    password: Optional[str] = None
    host: Optional[str] = None
    port_no: Optional[int] = None
    database_name: Optional[str] = None

    _required_components: List[str] = ["host"]


class MSSQLDocsSchema(MicrosoftSQLServerSchema, NoValidationSchema):
    """MS SQL Secrets Schema for API Docs"""
