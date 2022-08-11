import json
from typing import Any, Dict, Generator

import pydash
import pytest
from fideslib.core.config import load_toml
from fideslib.cryptography import cryptographic_util
from fideslib.db import session
from sqlalchemy.orm import Session

from fidesops.models.connectionconfig import (
    AccessLevel,
    ConnectionConfig,
    ConnectionType,
)
from fidesops.models.datasetconfig import DatasetConfig
from fidesops.schemas.saas.shared_schemas import HTTPMethod, SaaSRequestParams
from fidesops.service.connectors import SaaSConnector
from fidesops.util.saas_util import format_body, load_config
from tests.ops.fixtures.application_fixtures import load_dataset
from tests.ops.test_helpers.saas_test_utils import poll_for_existence
from tests.ops.test_helpers.vault_client import get_secrets

saas_config = load_toml(["saas_config.toml"])
secrets = get_secrets("datadog")


@pytest.fixture(scope="session")
def datadog_secrets():
    return {
        "domain": pydash.get(saas_config, "datadog.domain") or secrets["domain"],
        "api_key": pydash.get(saas_config, "datadog.api_key") or secrets["api_key"],
        "app_key": pydash.get(saas_config, "datadog.app_key") or secrets["app_key"],
    }


@pytest.fixture(scope="function")
def datadog_identity_email():
    return (
        pydash.get(saas_config, "datadog.identity_email") or secrets["identity_email"]
    )


@pytest.fixture
def datadog_config() -> Dict[str, Any]:
    return load_config("data/saas/config/datadog_config.yml")[0]


@pytest.fixture
def datadog_dataset() -> Dict[str, Any]:
    return load_dataset("data/saas/dataset/datadog_dataset.yml")[0]


@pytest.fixture(scope="function")
def datadog_connection_config(
        db: session,
        datadog_config,
        datadog_secrets
) -> Generator:
    fides_key = datadog_config["fides_key"]
    connection_config = ConnectionConfig.create(
        db=db,
        data={
            "key": fides_key,
            "name": fides_key,
            "connection_type": ConnectionType.saas,
            "access": AccessLevel.write,
            "secrets": datadog_secrets,
            "saas_config": datadog_config,
        },
    )
    yield connection_config
    connection_config.delete(db)

@pytest.fixture
def dataset_config_datadog(
    db: Session,
    datadog_connection_config: ConnectionConfig,
    datadog_dataset,
    datadog_config,
) -> Generator:
    fides_key = datadog_config["fides_key"]
    datadog_connection_config.name = fides_key
    datadog_connection_config.key = fides_key
    datadog_connection_config.save(db=db)
    dataset = DatasetConfig.create(
        db=db,
        data={
            "connection_config_id": datadog_connection_config.id,
            "fides_key": fides_key,
            "dataset": datadog_dataset,
        },
    )
    yield dataset
    dataset.delete(db=db)