import random
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


@pytest.fixture(scope="function")
def rollbar_create_erasure_data(
    rollbar_connection_config: ConnectionConfig, rollbar_erasure_identity_email: str
) -> Generator:
    """
    Creates a dynamic test data record for erasure tests.
    """
    rollbar_secrets = rollbar_connection_config.secrets
    """
        there are 3 steps to create data for erasure api
        1) create a new project
        2) get access token with scope post_server_item from project details
        3) create item inside above created project
        """

    # 1) create a new project
    random_num = random.randint(0, 99)
    base_url = f"https://{rollbar_secrets['domain']}"
    body = {"name": f"ethyca_test_project_{random_num}"}
    headers = {
        "Content-Type": "application/json",
        "X-Rollbar-Access-Token": rollbar_secrets["write_access_token"],
        # Use an Account Access Token with 'write' scope
    }

    project_response = requests.post(
        url=f"{base_url}/api/1/projects", json=body, headers=headers
    )
    project = project_response.json()
    assert project_response.ok
    project_id = project["result"]["id"]

    # 2) get access token with scope post_server_item, read from project details
    headers = {
        "Content-Type": "application/json",
        "X-Rollbar-Access-Token": rollbar_secrets["read_access_token"],
        #     Use an Account Access Token with 'read' scope
    }
    url = f"{base_url}/api/1/project/{project_id}/access_tokens"
    access_token_response = requests.get(url=url, headers=headers)
    assert access_token_response.ok
    access_tokens = access_token_response.json()
    access_tokens_result = access_tokens["result"]
    import pdb

    pdb.set_trace()
    # fetch only specific tokens from token list
    project_tokens = {"read": "", "post_server_item": ""}
    for token in access_tokens_result:
        if token["name"] == "read":
            project_tokens["read"] = token["access_token"]
        if token["name"] == "post_server_item":
            project_tokens["post_server_item"] = token["access_token"]

    # 3) create item inside above created project
    # Use an access token with scope post_server_item
    headers = {
        "Content-Type": "application/json",
        "X-Rollbar-Access-Token": project_tokens["post_server_item"],
    }
    body = {
        "data": {
            "environment": "production",
            "body": {
                "message": {
                    "body": "Request over threshold of 10 seconds",
                    "route": "home#index",
                    "time_elapsed": 15.23,
                },
                "level": "error",
            },
            "person": {
                "id": "1",
                "username": "ethyca",
                "email": rollbar_erasure_identity_email,
            },
        }
    }
    item_response = requests.post(
        url=f"{base_url}/api/1/item/", json=body, headers=headers
    )

    assert item_response.ok
    item = item_response.json()["result"]
    yield item
