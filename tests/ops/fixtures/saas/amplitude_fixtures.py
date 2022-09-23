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

secrets = get_secrets("amplitude")


@pytest.fixture(scope="function")
def amplitude_secrets(saas_config):
    return {
        "domain": pydash.get(saas_config, "amplitude.domain") or secrets["domain"],
        "api_key": pydash.get(saas_config, "amplitude.api_key") or secrets["api_key"],
        "secret_key": pydash.get(saas_config, "amplitude.secret_key") or secrets["secret_key"],
    }


@pytest.fixture(scope="function")
def amplitude_identity_email(saas_config):
    return (
        pydash.get(saas_config, "amplitude.user_id") or secrets["user_id"]
    )


@pytest.fixture
def amplitude_config() -> Dict[str, Any]:
    return load_config_with_replacement(
        "data/saas/config/amplitude_config.yml",
        "<instance_fides_key>",
        "amplitude_instance",
    )


@pytest.fixture
def amplitude_dataset() -> Dict[str, Any]:
    return load_dataset_with_replacement(
        "data/saas/dataset/amplitude_dataset.yml",
        "<instance_fides_key>",
        "amplitude_instance",
    )[0]


@pytest.fixture(scope="function")
def amplitude_connection_config(
    db: session, amplitude_config, amplitude_secrets
) -> Generator:
    fides_key = amplitude_config["fides_key"]
    connection_config = ConnectionConfig.create(
        db=db,
        data={
            "key": fides_key,
            "name": fides_key,
            "connection_type": ConnectionType.saas,
            "access": AccessLevel.write,
            "secrets": amplitude_secrets,
            "saas_config": amplitude_config,
        },
    )
    yield connection_config
    connection_config.delete(db)


@pytest.fixture
def amplitude_dataset_config(
    db: Session,
    amplitude_connection_config: ConnectionConfig,
    amplitude_dataset,
    amplitude_config,
) -> Generator:
    fides_key = amplitude_config["fides_key"]
    amplitude_connection_config.name = fides_key
    amplitude_connection_config.key = fides_key
    amplitude_connection_config.save(db=db)
    dataset = DatasetConfig.create(
        db=db,
        data={
            "connection_config_id": amplitude_connection_config.id,
            "fides_key": fides_key,
            "dataset": amplitude_dataset,
        },
    )
    yield dataset
    dataset.delete(db=db)
