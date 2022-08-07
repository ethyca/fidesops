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
from fidesops.util.saas_util import load_config
from tests.ops.fixtures.application_fixtures import load_dataset
from tests.ops.test_helpers.vault_client import get_secrets

saas_config = load_toml(["saas_config.toml"])
secrets = get_secrets("ownbackup")


@pytest.fixture(scope="session")
def ownbackup_secrets():
    return {
        "domain": pydash.get(saas_config, "ownbackup.domain") or secrets["domain"],
        "username": pydash.get(saas_config, "ownbackup.username")
        or secrets["username"],
        "password": pydash.get(saas_config, "ownbackup.client_id")
        or secrets["password"],
    }


@pytest.fixture(scope="session")
def ownbackup_identity_email():
    return (
        pydash.get(saas_config, "ownbackup.identity_email") or secrets["identity_email"]
    )


@pytest.fixture(scope="function")
def ownbackup_erasure_identity_email() -> str:
    return f"{cryptographic_util.generate_secure_random_string(13)}@email.com"


@pytest.fixture
def ownbackup_config() -> Dict[str, Any]:
    return load_config("data/saas/config/ownbackup_config.yml")


@pytest.fixture
def ownbackup_dataset() -> Dict[str, Any]:
    return load_dataset("data/saas/dataset/ownbackup_dataset.yml")[0]


@pytest.fixture(scope="function")
def ownbackup_connection_config(
    db: session, ownbackup_config, ownbackup_secrets
) -> Generator:
    fides_key = ownbackup_config["fides_key"]
    connection_config = ConnectionConfig.create(
        db=db,
        data={
            "key": fides_key,
            "name": fides_key,
            "connection_type": ConnectionType.saas,
            "access": AccessLevel.write,
            "secrets": ownbackup_secrets,
            "saas_config": ownbackup_config,
        },
    )
    yield connection_config
    connection_config.delete(db)


@pytest.fixture
def ownbackup_dataset_config(
    db: Session,
    ownbackup_connection_config: ConnectionConfig,
    ownbackup_dataset: Dict[str, Any],
) -> Generator:
    fides_key = ownbackup_dataset["fides_key"]
    ownbackup_connection_config.name = fides_key
    ownbackup_connection_config.key = fides_key
    ownbackup_connection_config.save(db=db)
    dataset = DatasetConfig.create(
        db=db,
        data={
            "connection_config_id": ownbackup_connection_config.id,
            "fides_key": fides_key,
            "dataset": ownbackup_dataset,
        },
    )
    yield dataset
    dataset.delete(db=db)
