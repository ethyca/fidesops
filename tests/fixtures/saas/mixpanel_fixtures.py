import os
import time
from typing import Any, Dict, Generator

import pydash
import pytest
import requests
from faker import Faker
from requests.auth import _basic_auth_str
from sqlalchemy.orm import Session
from fidesops.core.config import load_toml
from fidesops.db import session
from fidesops.models.connectionconfig import (
    AccessLevel,
    ConnectionConfig,
    ConnectionType,
)
from fidesops.models.datasetconfig import DatasetConfig
from tests.fixtures.application_fixtures import load_dataset
from tests.fixtures.saas_example_fixtures import load_config

saas_config = load_toml("saas_config.toml")


@pytest.fixture(scope="function")
def mixpanel_secrets():
    return {
        "domain": pydash.get(saas_config, "mixpanel.domain")
        or os.environ.get("MIXPANEL_DOMAIN"),
        "api_domain": pydash.get(saas_config, "mixpanel.api_domain")
        or os.environ.get("MIXPANEL_API_DOMAIN"),
        "project_token": pydash.get(saas_config, "mixpanel.project_token")
        or os.environ.get("MIXPANEL_PROJECT_TOKEN"),
        "gdpr_oauth_token": pydash.get(saas_config, "mixpanel.gdpr_oauth_token")
        or os.environ.get("MIXPANEL_GDPR_OAUTH_TOKEN"),
        "username": pydash.get(saas_config, "mixpanel.username")
        or os.environ.get("MIXPANEL_USERNAME"),
        "password": pydash.get(saas_config, "mixpanel.password")
        or os.environ.get("MIXPANEL_PASSWORD"),
        "project_id": pydash.get(saas_config, "mixpanel.project_id")
        or os.environ.get("MIXPANEL_PROJECT_ID"),
    }


@pytest.fixture(scope="function")
def mixpanel_identity_email():
    return pydash.get(saas_config, "mixpanel.identity_email") or os.environ.get(
        "MIXPANEL_IDENTITY_EMAIL"
    )


@pytest.fixture
def mixpanel_config() -> Dict[str, Any]:
    return load_config("data/saas/config/mixpanel_config.yml")


@pytest.fixture
def mixpanel_dataset() -> Dict[str, Any]:
    return load_dataset("data/saas/dataset/mixpanel_dataset.yml")[0]


@pytest.fixture(scope="function")
def mixpanel_connection_config(
    db: session, mixpanel_config, mixpanel_secrets
) -> Generator:
    fides_key = mixpanel_config["fides_key"]
    connection_config = ConnectionConfig.create(
        db=db,
        data={
            "key": fides_key,
            "name": fides_key,
            "connection_type": ConnectionType.saas,
            "access": AccessLevel.write,
            "secrets": mixpanel_secrets,
            "saas_config": mixpanel_config,
        },
    )
    yield connection_config
    connection_config.delete(db)


@pytest.fixture
def mixpanel_dataset_config(
    db: Session,
    mixpanel_connection_config: ConnectionConfig,
    mixpanel_dataset: Dict[str, Any],
) -> Generator:
    fides_key = mixpanel_dataset["fides_key"]
    mixpanel_connection_config.name = fides_key
    mixpanel_connection_config.key = fides_key
    mixpanel_connection_config.save(db=db)
    dataset = DatasetConfig.create(
        db=db,
        data={
            "connection_config_id": mixpanel_connection_config.id,
            "fides_key": fides_key,
            "dataset": mixpanel_dataset,
        },
    )
    yield dataset
    dataset.delete(db=db)


@pytest.fixture(scope="function")
def mixpanel_create_test_data(mixpanel_identity_email, mixpanel_connection_config):
    mixpanel_secrets = mixpanel_connection_config.secrets
    faker = Faker()
    ts = int(time.time())
    at_index: int = mixpanel_identity_email.find("@")
    email = (
        f"{mixpanel_identity_email[0:at_index]}{ts}{mixpanel_identity_email[at_index:]}"
    )
    distinct_id = str(ts)

    first_name = faker.first_name()
    last_name = faker.last_name()

    # Create user
    headers = {
        "Accept": "text/plain",
        "Content-Type": "application/json",
    }

    body = [
        {
            "$token": mixpanel_secrets["project_token"],
            "$distinct_id": distinct_id,
            "$set": {
                "$email": email,
                "$first_name": first_name,
                "$last_name": last_name,
            },
        }
    ]

    resp = requests.post(
        "https://api.mixpanel.com/engage#profile-set", headers=headers, json=body
    )

    assert resp.json() == 1

    # Create event
    body = [
        {
            "event": "Signed up",
            "properties": {
                "time": ts,
                "distinct_id": distinct_id,
                "$insert_id": "29fc2962-6d9c-455d-95ad-95b84f09b9e4",
                "ip": "136.24.0.114",
                "Referred by": "Friend",
                "URL": "mixpanel.com/signup",
            },
        }
    ]

    resp = requests.post(
        f"https://api.mixpanel.com/import?strict=1&project_id={mixpanel_secrets['project_id']}",
        headers={
            **headers,
            "Authorization": _basic_auth_str(
                mixpanel_secrets["username"], mixpanel_secrets["password"]
            ),
        },
        json=body,
    )

    assert resp.json()["num_records_imported"] == 1

    yield email

    # Delete test data
    body = {
        "distinct_ids": [distinct_id],
    }

    resp = requests.post(
        f"https://mixpanel.com/api/app/data-deletions/v3.0/?token={mixpanel_secrets['project_token']}",
        headers={
            **headers,
            "Authorization": f"Bearer {mixpanel_secrets['gdpr_oauth_token']}",
        },
        json=body,
    )

    assert resp.json()["status"] == "ok"
