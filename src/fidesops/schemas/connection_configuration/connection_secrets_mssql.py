from typing import Optional, List

from fidesops.schemas.base_class import NoValidationSchema
from fidesops.schemas.connection_configuration.connection_secrets import (
    ConnectionConfigSecretsSchema,
)


class MicrosoftSQLServerSchema(ConnectionConfigSecretsSchema):
    """Schema to validate the secrets needed to connect to a MS SQL Database

    connection string takes the format:
    mssql://[Server_Name[:Portno]]/[Database_Instance_Name]/[Database_Name]?FailoverPartner=[Partner_Server_Name]&InboundId=[Inbound_ID]

    Will probably change some depending on SQLAlchemy dialect/DBAPI option used

    """

    username: Optional[str] = None
    password: Optional[str] = None
    host: Optional[str] = None
    port_no: Optional[int] = None
    database_name: Optional[str] = None
    driver: Optional[str] = None
    driver_authentication: Optional[str] = None


    _required_components: List[str] = ["host"]


class MSSQLDocsSchema(MicrosoftSQLServerSchema, NoValidationSchema):
    """MS SQL Secrets Schema for API Docs"""
