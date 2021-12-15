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

    server_name: Optional[str] = None
    port_no: Optional[int] = None
    database_instance_name: Optional[str] = None
    database_name: Optional[str] = None
    partner_server_name: Optional[str] = None
    inbound_id: Optional[str] = None

    _required_components: List[str] = ["server_name"]


class MSSQLDocsSchema(MicrosoftSQLServerSchema, NoValidationSchema):
    """MS SQL Secrets Schema for API Docs"""
