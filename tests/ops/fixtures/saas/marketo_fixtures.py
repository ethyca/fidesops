from typing import Any, Dict, Generator

import pydash
import pytest
import requests
from fideslib.cryptography import cryptographic_util
from sqlalchemy.orm import Session

from fidesops.ops.models.connectionconfig import (
    AccessLevel,
    ConnectionConfig,
    ConnectionType,
)
from fidesops.ops.models.datasetconfig import DatasetConfig
from fidesops.ops.util.saas_util import load_config
from tests.ops.fixtures.application_fixtures import load_dataset
from tests.ops.test_helpers.vault_client import get_secrets

secrets = get_secrets("marketo")


@pytest.fixture(scope="session")
def marketo_secrets(saas_config):
    return {
        "domain": pydash.get(saas_config, "marketo.domain") or secrets["domain"],
        "client_id": pydash.get(saas_config, "marketo.client_id") or secrets["client_id"],
        "client_secret": pydash.get(saas_config, "marketo.client_secret") or secrets["client_secret"],
        "access_token": pydash.get(saas_config, "marketo.access_token") or secrets["access_token"],
    }


@pytest.fixture(scope="session")
def marketo_identity_email(saas_config):
    return (
        pydash.get(saas_config, "marketo.identity_email") or secrets["identity_email"]
    )


@pytest.fixture(scope="function")
def marketo_erasure_identity_email() -> str:
    return f"{cryptographic_util.generate_secure_random_string(13)}@email.com"


@pytest.fixture
def marketo_config() -> Dict[str, Any]:
    return load_config("data/saas/config/marketo_config.yml")


@pytest.fixture
def marketo_dataset() -> Dict[str, Any]:
    return load_dataset("data/saas/dataset/marketo_dataset.yml")[0]


@pytest.fixture(scope="function")
def marketo_connection_config(
    db: Session, marketo_config, marketo_secrets
) -> Generator:
    fides_key = marketo_config["fides_key"]
    connection_config = ConnectionConfig.create(
        db=db,
        data={
            "key": fides_key,
            "name": fides_key,
            "connection_type": ConnectionType.saas,
            "access": AccessLevel.write,
            "secrets": marketo_secrets,
            "saas_config": marketo_config,
        },
    )
    yield connection_config
    connection_config.delete(db)


@pytest.fixture
def marketo_dataset_config(
    db: Session,
    marketo_connection_config: ConnectionConfig,
    marketo_dataset: Dict[str, Any],
) -> Generator:
    fides_key = marketo_dataset["fides_key"]
    marketo_connection_config.name = fides_key
    marketo_connection_config.key = fides_key
    marketo_connection_config.save(db=db)
    dataset = DatasetConfig.create(
        db=db,
        data={
            "connection_config_id": marketo_connection_config.id,
            "fides_key": fides_key,
            "dataset": marketo_dataset,
        },
    )
    yield dataset
    dataset.delete(db=db)
