import json
import os
import time
from typing import Any, Dict, Generator

import pydash
import pytest
import requests
from requests import Response
from sqlalchemy.orm import Session
from starlette.status import HTTP_201_CREATED

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
SALESFORCE_FIRSTNAME = "TestFirstName"


@pytest.fixture(scope="session")
def salesforce_identity_email():
    return f"{cryptographic_util.generate_secure_random_string(13)}@email.com"

@pytest.fixture(scope="session")
def salesforce_account_name():
    return f"{cryptographic_util.generate_secure_random_string(13)} Test Account"


@pytest.fixture(scope="session")
def salesforce_secrets():
    return {
        "domain": pydash.get(saas_config, "salesforce.domain")
        or os.environ.get("SALESFORCE_DOMAIN"),
        "username": pydash.get(saas_config, "salesforce.username")
        or os.environ.get("SALESFORCE_USERNAME"),
        "password": pydash.get(saas_config, "salesforce.password")
        or os.environ.get("SALESFORCE_PASSWORD"),
        "client_id": pydash.get(saas_config, "salesforce.client_id")
        or os.environ.get("SALESFORCE_CLIENT_ID"),
        "client_secret": pydash.get(saas_config, "salesforce.client_secret")
        or os.environ.get("SALESFORCE_CLIENT_SECRET"),
        "access_token": pydash.get(saas_config, "salesforce.access_token")
        or os.environ.get("SALESFORCE_ACCESS_TOKEN")
    }

@pytest.fixture(scope="session")
def salesforce_token(salesforce_secrets) -> str: 
    body = {
        "client_id" : salesforce_secrets["client_id"],
        "client_secret": salesforce_secrets["client_secret"],
        "grant_type" : "password",
        "username" : salesforce_secrets["username"],
        "password" : salesforce_secrets["password"]
    }
    response = requests.post("https://" + salesforce_secrets["domain"] + "/services/oauth2/token", body)
    return response.json()['access_token']



@pytest.fixture
def salesforce_config() -> Dict[str, Any]:
    return load_config("data/saas/config/salesforce_config.yml")


@pytest.fixture
def salesforce_dataset() -> Dict[str, Any]:
    return load_dataset("data/saas/dataset/salesforce_dataset.yml")[0]


@pytest.fixture(scope="function")
def salesforce_connection_config(
    db: session, salesforce_config,salesforce_dataset, salesforce_secrets, salesforce_token
) -> Generator:
    fides_key = salesforce_config["fides_key"]
    salesforce_secrets['access_token'] = salesforce_token
    connection_config = ConnectionConfig.create(
        db=db,
        data={
            "key": fides_key,
            "name": fides_key,
            "connection_type": ConnectionType.saas,
            "access": AccessLevel.write,
            "secrets": salesforce_secrets,
            "saas_config": salesforce_config,
        },
    )
    yield connection_config
    connection_config.delete(db)


@pytest.fixture
def salesforce_dataset_config(
    db: Session,
    salesforce_connection_config: ConnectionConfig,
    salesforce_dataset: Dict[str, Any],
) -> Generator:
    fides_key = salesforce_dataset["fides_key"]
    salesforce_connection_config.name = fides_key
    salesforce_connection_config.key = fides_key
    salesforce_connection_config.save(db=db)
    dataset = DatasetConfig.create(
        db=db,
        data={
            "connection_config_id": salesforce_connection_config.id,
            "fides_key": fides_key,
            "dataset": salesforce_dataset,
        },
    )
    yield dataset
    dataset.delete(db=db)


@pytest.fixture(scope="function")
def salesforce_data(
    salesforce_connection_config, salesforce_identity_email, salesforce_secrets, salesforce_account_name
) -> Generator:
    """
    Creates a dynamic test data record for tests.
    Yields contact ID as this may be useful to have in test scenarios
    """
    connector = SaaSConnector(salesforce_connection_config)

    # Create account
    body = {
        "name": salesforce_account_name
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {salesforce_secrets['access_token']}",
    }
    accounts_request: SaaSRequestParams = SaaSRequestParams(
        method=HTTPMethod.POST,
        path="/services/data/v54.0/sobjects/Account",
        headers=headers,
        body=json.dumps(body),
    )
    accounts_response: Response = connector.create_client().send(accounts_request)
    assert HTTP_201_CREATED == accounts_response.status_code
    account_id = accounts_response.json()['id']
    

    # Create contact
    body = {
        "firstName": "Fidesops",
        "lastName": "Test Contact",
        "email": salesforce_identity_email,
        "AccountId": account_id
    }
    contacts_request: SaaSRequestParams = SaaSRequestParams(
        method=HTTPMethod.POST,
        path="/services/data/v54.0/sobjects/Contact",
        headers=headers,
        body=json.dumps(body),
    )
    contacts_response = connector.create_client().send(contacts_request)
    assert HTTP_201_CREATED == contacts_response.status_code
    contact_id = contacts_response.json()['id']
    yield contact_id
