from typing import Any, Dict, Generator

import pydash
import pytest
from fideslib.cryptography import cryptographic_util
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

# from tests.ops.test_helpers.saas_test_utils import poll_for_existence
from tests.ops.test_helpers.vault_client import get_secrets

secrets = get_secrets("fullstory")


@pytest.fixture(scope="function")
def fullstory_secrets(saas_config):
    return {
        "domain": pydash.get(saas_config, "fullstory.domain") or secrets["domain"],
        "access_token": pydash.get(saas_config, "fullstory.access_token")
        or secrets["access_token"],
    }


@pytest.fixture(scope="function")
def fullstory_identity_email(saas_config):
    return (
        pydash.get(saas_config, "fullstory.identity_email") or secrets["identity_email"]
    )


@pytest.fixture(scope="function")
def fullstory_uid(saas_config):
    return pydash.get(saas_config, "fullstory.uid") or secrets["uid"]


# @pytest.fixture(scope="session")
# def fullstory_erasure_identity_email():
#     return f"{cryptographic_util.generate_secure_random_string(13)}@email.com"


@pytest.fixture
def fullstory_config() -> Dict[str, Any]:
    return load_config_with_replacement(
        "data/saas/config/fullstory_config.yml",
        "<instance_fides_key>",
        "fullstory_instance",
    )


@pytest.fixture
def fullstory_dataset() -> Dict[str, Any]:
    return load_dataset_with_replacement(
        "data/saas/dataset/fullstory_dataset.yml",
        "<instance_fides_key>",
        "fullstory_instance",
    )[0]


@pytest.fixture(scope="function")
def fullstory_connection_config(
    db: session, fullstory_config, fullstory_secrets
) -> Generator:
    fides_key = fullstory_config["fides_key"]
    connection_config = ConnectionConfig.create(
        db=db,
        data={
            "key": fides_key,
            "name": fides_key,
            "connection_type": ConnectionType.saas,
            "access": AccessLevel.write,
            "secrets": fullstory_secrets,
            "saas_config": fullstory_config,
        },
    )
    yield connection_config
    connection_config.delete(db)


@pytest.fixture
def fullstory_dataset_config(
    db: Session,
    fullstory_connection_config: ConnectionConfig,
    fullstory_dataset: Dict[str, Any],
) -> Generator:
    fides_key = fullstory_dataset["fides_key"]
    fullstory_connection_config.name = fides_key
    fullstory_connection_config.key = fides_key
    fullstory_connection_config.save(db=db)
    dataset = DatasetConfig.create(
        db=db,
        data={
            "connection_config_id": fullstory_connection_config.id,
            "fides_key": fides_key,
            "dataset": fullstory_dataset,
        },
    )
    yield dataset
    dataset.delete(db=db)
