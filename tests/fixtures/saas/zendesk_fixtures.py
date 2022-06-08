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
def zendesk_secrets():
    return {
        "domain": pydash.get(saas_config, "zendesk.domain")
        or os.environ.get("ZENDESK_DOMAIN"),
        "app_username": pydash.get(saas_config, "zendesk.app_username")
        or os.environ.get("ZENDESK_USERNAME"),
        "app_password": pydash.get(saas_config, "zendesk.app_password")
        or os.environ.get("ZENDESK_API_KEY"),
    }


@pytest.fixture(scope="function")
def zendesk_identity_email():
    return pydash.get(saas_config, "zendesk.identity_email") or os.environ.get(
        "ZENDESK_IDENTITY_EMAIL"
    )


@pytest.fixture
def zendesk_config() -> Dict[str, Any]:
    return load_config("data/saas/config/zendesk_config.yml")


@pytest.fixture
def zendesk_dataset() -> Dict[str, Any]:
    return load_dataset("data/saas/dataset/zendesk_dataset.yml")[0]


@pytest.fixture(scope="function")
def zendesk_connection_config(
    db: session, zendesk_config, zendesk_secrets
) -> Generator:
    fides_key = zendesk_config["fides_key"]
    connection_config = ConnectionConfig.create(
        db=db,
        data={
            "key": fides_key,
            "name": fides_key,
            "connection_type": ConnectionType.saas,
            "access": AccessLevel.write,
            "secrets": zendesk_secrets,
            "saas_config": zendesk_config,
        },
    )
    yield connection_config
    connection_config.delete(db)


@pytest.fixture
def zendesk_dataset_config(
    db: Session,
    zendesk_connection_config: ConnectionConfig,
    zendesk_dataset: Dict[str, Any],
) -> Generator:
    fides_key = zendesk_dataset["fides_key"]
    zendesk_connection_config.name = fides_key
    zendesk_connection_config.key = fides_key
    zendesk_connection_config.save(db=db)
    dataset = DatasetConfig.create(
        db=db,
        data={
            "connection_config_id": zendesk_connection_config.id,
            "fides_key": fides_key,
            "dataset": zendesk_dataset,
        },
    )
    yield dataset
    dataset.delete(db=db)


@pytest.fixture(scope="function")
def reset_zendesk_data(
    zendesk_connection_config, zendesk_identity_email
) -> Generator:
    """
    Gets the current value of the resource and restores it after the test is complete.
    Used for erasure tests.
    """
    connector = SaaSConnector(zendesk_connection_config)
    request: SaaSRequestParams = SaaSRequestParams(
        method=HTTPMethod.GET,
        path="/3.0/search-members",
        query_params={"query": zendesk_identity_email},
    )
    response = connector.create_client().send(request)
    body = response.json()
    member = body["exact_matches"]["members"][0]
    yield member
    request: SaaSRequestParams = SaaSRequestParams(
        method=HTTPMethod.PUT,
        headers={"Content-Type": "application/json"},
        path=f'/3.0/lists/{member["list_id"]}/members/{member["id"]}',
        body=json.dumps(member),
    )
    connector.create_client().send(request)
