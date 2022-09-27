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

secrets = get_secrets("braze")


@pytest.fixture(scope="session")
def braze_secrets(saas_config):
    return {
        "domain": pydash.get(saas_config, "braze.domain") or secrets["domain"],
        "api_key": pydash.get(saas_config, "braze.api_key") or secrets["api_key"],
        "external_id": pydash.get(saas_config, "braze.external_id")
        or secrets["external_id"],
    }


@pytest.fixture(scope="session")
def braze_identity_email(saas_config):
    return pydash.get(saas_config, "braze.identity_email") or secrets["identity_email"]


@pytest.fixture
def braze_config() -> Dict[str, Any]:
    return load_config_with_replacement(
        "data/saas/config/braze_config.yml",
        "<instance_fides_key>",
        "braze_instance",
    )


@pytest.fixture
def braze_dataset() -> Dict[str, Any]:
    return load_dataset_with_replacement(
        "data/saas/dataset/braze_dataset.yml",
        "<instance_fides_key>",
        "braze_instance",
    )[0]


@pytest.fixture(scope="function")
def braze_connection_config(db: session, braze_config, braze_secrets) -> Generator:
    fides_key = braze_config["fides_key"]
    connection_config = ConnectionConfig.create(
        db=db,
        data={
            "key": fides_key,
            "name": fides_key,
            "connection_type": ConnectionType.saas,
            "access": AccessLevel.write,
            "secrets": braze_secrets,
            "saas_config": braze_config,
        },
    )
    yield connection_config
    connection_config.delete(db)


@pytest.fixture
def braze_dataset_config(
    db: Session,
    braze_connection_config: ConnectionConfig,
    braze_dataset,
    braze_config,
) -> Generator:
    fides_key = braze_config["fides_key"]
    braze_connection_config.name = fides_key
    braze_connection_config.key = fides_key
    braze_connection_config.save(db=db)
    dataset = DatasetConfig.create(
        db=db,
        data={
            "connection_config_id": braze_connection_config.id,
            "fides_key": fides_key,
            "dataset": braze_dataset,
        },
    )
    yield dataset
    dataset.delete(db=db)
