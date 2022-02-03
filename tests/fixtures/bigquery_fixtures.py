import os
from typing import Generator
from uuid import uuid4

import pytest

from sqlalchemy.orm import Session

from fidesops.models.connectionconfig import AccessLevel, ConnectionType, ConnectionConfig
from fidesops.schemas.connection_configuration import BigQuerySchema
from fixtures.application_fixtures import integration_config


@pytest.fixture(scope="function")
def bigquery_connection_config(db: Session) -> Generator:
    connection_config = ConnectionConfig.create(
        db=db,
        data={
            "name": str(uuid4()),
            "key": "my_bigquery_config",
            "connection_type": ConnectionType.bigquery,
            "access": AccessLevel.write,
        },
    )
    uri = integration_config.get("bigquery", {}).get("external_uri") or os.environ.get(
        "BIGQUERY_TEST_URI"
    )
    db_schema = integration_config.get("bigquery", {}).get(
        "db_schema"
    ) or os.environ.get("BIGQUERY_TEST_DB_SCHEMA")
    if uri and db_schema:
        schema = BigQuerySchema(url=uri, db_schema=db_schema)
        connection_config.secrets = schema.dict()
        connection_config.save(db=db)

    yield connection_config
    connection_config.delete(db)
