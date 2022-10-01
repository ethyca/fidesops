from typing import List, Optional

from pydantic.main import BaseModel

from fidesops.ops.schemas.base_class import NoValidationSchema
from fidesops.ops.schemas.connection_configuration.connection_secrets import (
    ConnectionConfigSecretsSchema,
)


class KeyfileCreds(BaseModel):
    """Schema that holds BigQuery keyfile key/vals"""

    type: Optional[str] = None
    project_id: str
    private_key_id: Optional[str] = None
    private_key: Optional[str] = None
    client_email: Optional[str] = None
    client_id: Optional[str] = None
    auth_uri: Optional[str] = None
    token_uri: Optional[str] = None
    auth_provider_x509_cert_url: Optional[str] = None
    client_x509_cert_url: Optional[str] = None

    class Config:
        """Add example for each field"""
        schema_extra = {
            "example": {
                "type": "service_account",
                "project_id": "XXXXXXXXXXXXXXXXXXXX",
                "private_key_id": "key-id",
                "private_key": "-----BEGIN PRIVATE KEY-----\nprivate-key\n-----END PRIVATE KEY-----\n",
                "client_email": "service-account-email",
                "client_id": "XXXXXXXXXXXXXXXXXXXX",
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://accounts.google.com/o/oauth2/token",
                "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/service-account-email"
            }
        }


class BigQuerySchema(ConnectionConfigSecretsSchema):
    """Schema to validate the secrets needed to connect to BigQuery"""

    dataset: Optional[str] = None
    keyfile_creds: KeyfileCreds

    _required_components: List[str] = ["keyfile_creds"]

    class Config:
        """Add example for each field"""
        schema_extra = {
            "example": {
                "dataset": None,
                "keyfile_creds": KeyfileCreds(project_id="XXXXXXXXXXXXXXXXXXXX")
            }
        }


class BigQueryDocsSchema(BigQuerySchema, NoValidationSchema):
    """BigQuery Secrets Schema for API Docs"""
