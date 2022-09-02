from typing import Any, Dict, Generator

import pydash
import pytest
import requests
from fideslib.cryptography import cryptographic_util
from fideslib.db import session
from sqlalchemy.orm import Session
from starlette.status import HTTP_404_NOT_FOUND

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
from tests.ops.fixtures.application_fixtures import load_dataset
from tests.ops.test_helpers.saas_test_utils import poll_for_existence
from tests.ops.test_helpers.vault_client import get_secrets

secrets = get_secrets("rollbar")


@pytest.fixture(scope="session")
def rollbar_secrets(saas_config):
    return {
        "domain": pydash.get(saas_config, "rollbar.domain") or secrets["domain"],
        "read_access_token": pydash.get(saas_config, "rollbar.read_access_token")
        or secrets["read_access_token"],
        "write_access_token": pydash.get(saas_config, "rollbar.write_access_token")
        or secrets["write_access_token"],
    }


@pytest.fixture(scope="session")
def rollbar_identity_email(saas_config):
    return (
        pydash.get(saas_config, "rollbar.identity_email") or secrets["identity_email"]
    )


@pytest.fixture(scope="function")
def rollbar_erasure_identity_email() -> str:
    return f"{cryptographic_util.generate_secure_random_string(13)}@email.com"


@pytest.fixture
def rollbar_config() -> Dict[str, Any]:
    return load_config_with_replacement(
        "data/saas/config/rollbar_config.yml",
        "<instance_fides_key>",
        "rollbar_instance",
    )


@pytest.fixture
def rollbar_dataset() -> Dict[str, Any]:
    return load_dataset_with_replacement(
        "data/saas/dataset/rollbar_dataset.yml",
        "<instance_fides_key>",
        "rollbar_instance",
    )[0]


@pytest.fixture(scope="function")
def rollbar_connection_config(
    db: session, rollbar_config, rollbar_secrets
) -> Generator:
    fides_key = rollbar_config["fides_key"]
    connection_config = ConnectionConfig.create(
        db=db,
        data={
            "key": fides_key,
            "name": fides_key,
            "connection_type": ConnectionType.saas,
            "access": AccessLevel.write,
            "secrets": rollbar_secrets,
            "saas_config": rollbar_config,
        },
    )
    yield connection_config
    connection_config.delete(db)


@pytest.fixture
def rollbar_dataset_config(
    db: Session,
    rollbar_connection_config: ConnectionConfig,
    rollbar_dataset,
    rollbar_config,
) -> Generator:
    fides_key = rollbar_config["fides_key"]
    rollbar_connection_config.name = fides_key
    rollbar_connection_config.key = fides_key
    rollbar_connection_config.save(db=db)
    dataset = DatasetConfig.create(
        db=db,
        data={
            "connection_config_id": rollbar_connection_config.id,
            "fides_key": fides_key,
            "dataset": rollbar_dataset,
        },
    )
    yield dataset
    dataset.delete(db=db)


@pytest.fixture(scope="session")
def rollbar_erasure_identity_email():
    return f"{cryptographic_util.generate_secure_random_string(13)}@email.com"


def rollbar_erasure_data(
    rollbar_connection_config: ConnectionConfig, rollbar_erasure_identity_email: str
) -> Generator:
    """
    Creates a dynamic test data record for erasure tests.
    Yields User ID as this may be useful to have in test scenarios
    """
    rollbar_secrets = rollbar_connection_config.secrets
    base_url = f"https://{rollbar_secrets['domain']}"
    body = {
        "email": rollbar_erasure_identity_email,
        "password": "k1UhfAg8hBu",
        "email_verified": True,
        "name": "Test",
        "given_name": "First Name",
        "family_name": "Last Name",
    }
    users_response = requests.post(
        url=f"{base_url}/websso/signup?response_type=code&redirect_uri={base_url}/version",
        json=body,
    )
    user = users_response.json()
    assert users_response.ok
    yield user
