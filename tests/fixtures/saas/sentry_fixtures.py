from typing import Any, Dict, Generator

import pytest
from fideslib.db import session
from sqlalchemy.orm import Session

from fidesops.models.connectionconfig import (
    AccessLevel,
    ConnectionConfig,
    ConnectionType,
)
from fidesops.models.datasetconfig import DatasetConfig
from fidesops.util.saas_util import load_config
from tests.fixtures.application_fixtures import load_dataset

from test_helpers.vault_client import get_secrets

secrets = get_secrets("sentry")


@pytest.fixture(scope="session")
def sentry_secrets():
    return {
        "domain": secrets["sentry.domain"],
        "access_token": secrets["access_token"],
        "erasure_access_token": secrets["erasure_access_token"],
        "erasure_identity_email": secrets["erasure_identity_email"],
        "user_id_erasure": secrets["user_id_erasure"],
        "issue_url": secrets["issue_url"],
    }


@pytest.fixture(scope="session")
def sentry_identity_email():
    return secrets["identity_email"]


@pytest.fixture
def sentry_config() -> Dict[str, Any]:
    return load_config("data/saas/config/sentry_config.yml")


@pytest.fixture
def sentry_dataset() -> Dict[str, Any]:
    return load_dataset("data/saas/dataset/sentry_dataset.yml")[0]


@pytest.fixture(scope="function")
def sentry_connection_config(db: session, sentry_config, sentry_secrets) -> Generator:
    fides_key = sentry_config["fides_key"]
    connection_config = ConnectionConfig.create(
        db=db,
        data={
            "key": fides_key,
            "name": fides_key,
            "connection_type": ConnectionType.saas,
            "access": AccessLevel.write,
            "secrets": sentry_secrets,
            "saas_config": sentry_config,
        },
    )
    yield connection_config
    connection_config.delete(db)


@pytest.fixture
def sentry_dataset_config(
    db: Session,
    sentry_connection_config: ConnectionConfig,
    sentry_dataset: Dict[str, Any],
) -> Generator:
    fides_key = sentry_dataset["fides_key"]
    sentry_connection_config.name = fides_key
    sentry_connection_config.key = fides_key
    sentry_connection_config.save(db=db)
    dataset = DatasetConfig.create(
        db=db,
        data={
            "connection_config_id": sentry_connection_config.id,
            "fides_key": fides_key,
            "dataset": sentry_dataset,
        },
    )
    yield dataset
    dataset.delete(db=db)
