from typing import Any, Dict, Generator

import pydash
import pytest
from fideslib.db import session
from sqlalchemy.orm import Session

from fidesops.ops.models.connectionconfig import (
    AccessLevel,
    ConnectionConfig,
    ConnectionType,
)
from fidesops.ops.models.datasetconfig import DatasetConfig
from fidesops.ops.util.saas_util import (
    load_config_with_replacement,
    load_dataset_with_replacement,
)
from tests.ops.test_helpers.vault_client import get_secrets

secrets = get_secrets("square")


@pytest.fixture(scope="session")
def square_secrets(saas_config):
    return {
        "domain": pydash.get(saas_config, "square.domain") or secrets["domain"],
        "access_token": pydash.get(saas_config, "square.access_token")
        or secrets["access_token"],
    }


@pytest.fixture(scope="session")
def square_identity_email(saas_config):
    return pydash.get(saas_config, "square.identity_email") or secrets["identity_email"]


@pytest.fixture
def square_config() -> Dict[str, Any]:
    return load_config_with_replacement(
        "data/saas/config/square_config.yml",
        "<instance_fides_key>",
        "square_instance",
    )


@pytest.fixture
def square_dataset() -> Dict[str, Any]:
    return load_dataset_with_replacement(
        "data/saas/dataset/square_dataset.yml",
        "<instance_fides_key>",
        "square_instance",
    )[0]


@pytest.fixture(scope="function")
def square_connection_config(db: session, square_config, square_secrets) -> Generator:
    fides_key = square_config["fides_key"]
    connection_config = ConnectionConfig.create(
        db=db,
        data={
            "key": fides_key,
            "name": fides_key,
            "connection_type": ConnectionType.saas,
            "access": AccessLevel.write,
            "secrets": square_secrets,
            "saas_config": square_config,
        },
    )
    yield connection_config
    connection_config.delete(db)


@pytest.fixture
def square_dataset_config(
    db: Session,
    square_connection_config: ConnectionConfig,
    square_dataset,
    square_config,
) -> Generator:
    fides_key = square_config["fides_key"]
    square_connection_config.name = fides_key
    square_connection_config.key = fides_key
    square_connection_config.save(db=db)
    dataset = DatasetConfig.create(
        db=db,
        data={
            "connection_config_id": square_connection_config.id,
            "fides_key": fides_key,
            "dataset": square_dataset,
        },
    )
    yield dataset
    dataset.delete(db=db)
