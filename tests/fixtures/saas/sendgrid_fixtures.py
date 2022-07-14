import json
import os
import time
from typing import Any, Dict, Generator

import pydash
import pytest
from sqlalchemy.orm import Session
from starlette.status import HTTP_202_ACCEPTED

from fidesops.core.config import load_toml
from fidesops.db import session
from fidesops.models.connectionconfig import (
    AccessLevel,
    ConnectionConfig,
    ConnectionType,
)
from fidesops.models.datasetconfig import DatasetConfig
from fidesops.schemas.saas.shared_schemas import HTTPMethod, SaaSRequestParams
from fidesops.service.connectors import SaaSConnector
from fidesops.util import cryptographic_util
from tests.fixtures.application_fixtures import load_dataset
from tests.fixtures.saas_example_fixtures import load_config

saas_config = load_toml("saas_config.toml")
SENDGRID_ERASURE_FIRSTNAME = "Erasurefirstname"


@pytest.fixture(scope="session")
def sendgrid_erasure_identity_email():
    return f"{cryptographic_util.generate_secure_random_string(13)}@email.com"


@pytest.fixture(scope="function")
def sendgrid_secrets():
    return {
        "domain": pydash.get(saas_config, "sendgrid.domain")
        or os.environ.get("SENDGRID_DOMAIN"),
        "api_key": pydash.get(saas_config, "sendgrid.api_key")
        or os.environ.get("SENDGRID_API_KEY"),
    }


@pytest.fixture(scope="function")
def sendgrid_identity_email():
    return pydash.get(saas_config, "sendgrid.identity_email") or os.environ.get(
        "SENDGRID_IDENTITY_EMAIL"
    )


@pytest.fixture
def sendgrid_config() -> Dict[str, Any]:
    return load_config("data/saas/config/sendgrid_config.yml")


@pytest.fixture
def sendgrid_dataset() -> Dict[str, Any]:
    return load_dataset("data/saas/dataset/sendgrid_dataset.yml")[0]


@pytest.fixture(scope="function")
def sendgrid_connection_config(
    db: session, sendgrid_config, sendgrid_secrets
) -> Generator:
    fides_key = sendgrid_config["fides_key"]
    connection_config = ConnectionConfig.create(
        db=db,
        data={
            "key": fides_key,
            "name": fides_key,
            "connection_type": ConnectionType.saas,
            "access": AccessLevel.write,
            "secrets": sendgrid_secrets,
            "saas_config": sendgrid_config,
        },
    )
    yield connection_config
    connection_config.delete(db)


@pytest.fixture
def sendgrid_dataset_config(
    db: Session,
    sendgrid_connection_config: ConnectionConfig,
    sendgrid_dataset: Dict[str, Any],
) -> Generator:
    fides_key = sendgrid_dataset["fides_key"]
    sendgrid_connection_config.name = fides_key
    sendgrid_connection_config.key = fides_key
    sendgrid_connection_config.save(db=db)
    dataset = DatasetConfig.create(
        db=db,
        data={
            "connection_config_id": sendgrid_connection_config.id,
            "fides_key": fides_key,
            "dataset": sendgrid_dataset,
        },
    )
    yield dataset
    dataset.delete(db=db)


@pytest.fixture(scope="function")
def sendgrid_erasure_data(
    sendgrid_connection_config, sendgrid_erasure_identity_email, sendgrid_secrets
) -> Generator:
    """
    Creates a dynamic test data record for erasure tests.
    Yields contact ID as this may be useful to have in test scenarios
    """
    connector = SaaSConnector(sendgrid_connection_config)

    # Create contact
    body = {
        "list_ids": ["62d20902-1cdd-42e7-8d5d-0fbb2a8be13e"],
        "contacts": [
            {
                "address_line_1": "address_line_1",
                "address_line_2": "address_line_2",
                "city": "CITY (optional)",
                "country": "country (optional)",
                "email": sendgrid_erasure_identity_email,
                "first_name": SENDGRID_ERASURE_FIRSTNAME,
                "last_name": "Testcontact",
                "postal_code": "postal_code (optional)",
                "state_province_region": "state (optional)",
                "custom_fields": {},
            }
        ],
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {sendgrid_secrets['api_key']}",
    }
    contacts_request: SaaSRequestParams = SaaSRequestParams(
        method=HTTPMethod.PUT,
        path="/v3/marketing/contacts",
        headers=headers,
        body=json.dumps(body),
    )
    contacts_response = connector.create_client().send(contacts_request)
    assert HTTP_202_ACCEPTED == contacts_response.status_code

    # Checks contact is propagated to Sendgrid before calling access / erasure requests
    # this has taken over 25s in testing
    retries = 10
    while (
        contact := _get_contact_if_exists(
            sendgrid_erasure_identity_email, connector, sendgrid_secrets
        )
    ) is None:
        if not retries:
            raise Exception(
                f"Contact with email {sendgrid_erasure_identity_email} could not be added to Sendgrid"
            )
        retries -= 1
        time.sleep(5)

    yield contact



def _get_contact_if_exists(
    sendgrid_erasure_identity_email: str, connector: SaaSConnector, sendgrid_secrets
) -> bool:
    """
    Confirm whether contact exists by calling contact search by email api and comparing resulting firstname str.
    Returns contact ID if it exists, returns None if it does not.
    """

    body = json.dumps({"emails": [sendgrid_erasure_identity_email]})
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {sendgrid_secrets['api_key']}",
    }

    contact_request: SaaSRequestParams = SaaSRequestParams(
        method=HTTPMethod.POST,
        path="/v3/marketing/contacts/search/emails",
        headers=headers,
        body=body,
    )
    contact_response = connector.create_client().send(
        contact_request, ignore_errors=True
    )

    # we expect 404 if contact doesn't exist
    if 404 == contact_response.status_code:
        return None

    return contact_response.json()["result"][sendgrid_erasure_identity_email][
        "contact"
    ]
