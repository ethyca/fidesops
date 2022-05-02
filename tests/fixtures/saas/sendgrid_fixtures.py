import json
from fidesops.core.config import load_toml
from fidesops.db import session
from fidesops.models.connectionconfig import (
    AccessLevel,
    ConnectionConfig,
    ConnectionType,
)
from fidesops.models.datasetconfig import DatasetConfig
import pytest
import pydash
import os
from typing import Any, Dict, Generator
from fidesops.schemas.saas.shared_schemas import HTTPMethod, SaaSRequestParams
from fidesops.service.connectors.saas_connector import SaaSConnector
from tests.fixtures.application_fixtures import load_dataset
from tests.fixtures.saas_example_fixtures import load_config
from sqlalchemy.orm import Session

saas_config = load_toml("saas_config.toml")


@pytest.fixture(scope="function")
def sendgrid_secrets():
    return {
        "host": pydash.get(saas_config, "sendgrid.host")
        or os.environ.get("SENDGRID_HOST"),
        "api_key": pydash.get(saas_config, "sendgrid.api_key")
        or os.environ.get("SENDGRID_API_KEY"),
    }


@pytest.fixture(scope="function")
def sendgrid_identity_email():
    return pydash.get(saas_config, "sendgrid.identity_email") or os.environ.get(
        "SENDGRID_IDENTITY_EMAIL"
    )


@pytest.fixture
def sendgrid_config() -> Dict[str, Any]:
    return load_config("data/saas/config/sendgrid_config.yml")


@pytest.fixture
def sendgrid_dataset() -> Dict[str, Any]:
    return load_dataset("data/saas/dataset/sendgrid_dataset.yml")[0]


@pytest.fixture(scope="function")
def sendgrid_connection_config(
    db: session, sendgrid_config, sendgrid_secrets
) -> Generator:
    fides_key = sendgrid_config["fides_key"]
    connection_config = ConnectionConfig.create(
        db=db,
        data={
            "key": fides_key,
            "name": fides_key,
            "connection_type": ConnectionType.saas,
            "access": AccessLevel.write,
            "secrets": sendgrid_secrets,
            "saas_config": sendgrid_config,
        },
    )
    yield connection_config
    connection_config.delete(db)


@pytest.fixture
def sendgrid_dataset_config(
    db: Session,
    sendgrid_connection_config: ConnectionConfig,
    sendgrid_dataset: Dict[str, Any],
) -> Generator:
    fides_key = sendgrid_dataset["fides_key"]
    sendgrid_connection_config.name = fides_key
    sendgrid_connection_config.key = fides_key
    sendgrid_connection_config.save(db=db)
    dataset = DatasetConfig.create(
        db=db,
        data={
            "connection_config_id": sendgrid_connection_config.id,
            "fides_key": fides_key,
            "dataset": sendgrid_dataset,
        },
    )
    yield dataset
    dataset.delete(db=db)


@pytest.fixture(scope="function")
def reset_sendgrid_data(
    sendgrid_connection_config, sendgrid_identity_email
) -> Generator:
    """
    Gets the current value of the resource and restores it after the test is complete.
    Used for erasure tests.
    """
    connector = SaaSConnector(sendgrid_connection_config)
    request_body = {"query": f"email = '{sendgrid_identity_email}'"}
    request: SaaSRequestParams = SaaSRequestParams(
        method=HTTPMethod.GET,
        path="/v3/marketing/contacts/search",
        body=json.dumps(request_body),
    )
    response = connector.create_client().send(request)
    body = response.json()
    contact = body["result"][0]
    yield contact
    request_body = {}
    if "list_ids" in contact:
        request_body["list_ids"] = contact["list_ids"]
        contact.pop("list_ids", None)  # remove list_ids from contact object
    request_body["contacts"] = [contact]
    request: SaaSRequestParams = SaaSRequestParams(
        method=HTTPMethod.PUT,
        path="/v3/marketing/contacts",
        body=json.dumps(request_body),
    )
    connector.create_client().send(request)
