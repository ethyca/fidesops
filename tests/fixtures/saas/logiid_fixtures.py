import os
from typing import Any, Dict, Generator

import pydash
import pytest
import requests
from fideslib.core.config import load_toml
from sqlalchemy.orm import Session

from fidesops.db import session
from fidesops.models.connectionconfig import (
    AccessLevel,
    ConnectionConfig,
    ConnectionType,
)
from fidesops.models.datasetconfig import DatasetConfig
from fidesops.util import cryptographic_util
from tests.fixtures.application_fixtures import load_dataset
from tests.fixtures.saas_example_fixtures import load_config

saas_config = load_toml(["saas_config.toml"])


@pytest.fixture(scope="session")
def logiid_secrets():
    return {
        "domain": pydash.get(saas_config, "logiid.domain")
        or os.environ.get("LOGIID_DOMAIN"),
        "client_id": pydash.get(saas_config, "logiid.client_id")
        or os.environ.get("LOGIID_CLIENT_ID"),
        "client_secret": pydash.get(saas_config, "logiid.client_secret")
        or os.environ.get("LOGIID_CLIENT_SECRET")
    }


@pytest.fixture(scope="session")
def logiid_identity_email():
    return pydash.get(saas_config, "logiid.identity_email") or os.environ.get(
        "LOGIID_IDENTITY_EMAIL"
    )


@pytest.fixture(scope="session")
def logiid_erasure_identity_email():
    return f"{cryptographic_util.generate_secure_random_string(13)}@email.com"


@pytest.fixture(scope="session")
def logiid_token(logiid_secrets) -> str:
    body = {
        "client_id": logiid_secrets["client_id"],
        "client_secret": logiid_secrets["client_secret"],
        "grant_type": "client_credentials",
    }
    response = requests.post(
        "https://" + logiid_secrets["domain"] + "/identity/oauth2/token", body
    )
    return response.json()["access_token"]


@pytest.fixture
def logiid_config() -> Dict[str, Any]:
    return load_config("data/saas/config/logiid_config.yml")


@pytest.fixture
def logiid_dataset() -> Dict[str, Any]:
    return load_dataset("data/saas/dataset/logiid_dataset.yml")[0]


@pytest.fixture(scope="function")
def logiid_connection_config(
    db: session,
    logiid_config,
    logiid_secrets,
    logiid_token,
) -> Generator:
    fides_key = logiid_config["fides_key"]
    logiid_secrets["access_token"] = logiid_token
    connection_config = ConnectionConfig.create(
        db=db,
        data={
            "key": fides_key,
            "name": fides_key,
            "connection_type": ConnectionType.saas,
            "access": AccessLevel.write,
            "secrets": logiid_secrets,
            "saas_config": logiid_config,
        },
    )
    yield connection_config
    connection_config.delete(db)


@pytest.fixture
def logiid_dataset_config(
    db: Session,
    logiid_connection_config: ConnectionConfig,
    logiid_dataset: Dict[str, Any],
) -> Generator:
    fides_key = logiid_dataset["fides_key"]
    logiid_connection_config.name = fides_key
    logiid_connection_config.key = fides_key
    logiid_connection_config.save(db=db)
    dataset = DatasetConfig.create(
        db=db,
        data={
            "connection_config_id": logiid_connection_config.id,
            "fides_key": fides_key,
            "dataset": logiid_dataset,
        },
    )
    yield dataset
    dataset.delete(db=db)
