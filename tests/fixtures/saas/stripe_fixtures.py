import json
import os
from multidimensional_urlencode import urlencode
from typing import Any, Dict, Generator
from fidesops.core.config import load_toml
from fidesops.db import session
from fidesops.models.connectionconfig import (
    AccessLevel,
    ConnectionConfig,
    ConnectionType,
)
from fidesops.models.datasetconfig import DatasetConfig
import pytest
import pydash
import requests
from tests.fixtures.application_fixtures import load_dataset
from tests.fixtures.saas_example_fixtures import load_config
from sqlalchemy.orm import Session

saas_config = load_toml("saas_config.toml")


@pytest.fixture(scope="function")
def stripe_secrets():
    return {
        "host": pydash.get(saas_config, "stripe.host") or os.environ.get("STRIPE_HOST"),
        "api_key": pydash.get(saas_config, "stripe.api_key")
        or os.environ.get("STRIPE_API_KEY"),
        "payment_types": pydash.get(saas_config, "stripe.payment_types")
        or os.environ.get("STRIPE_PAYMENT_TYPES"),
        "items_per_page": pydash.get(saas_config, "stripe.items_per_page")
        or os.environ.get("STRIPE_ITEMS_PER_PAGE"),
    }


@pytest.fixture(scope="function")
def stripe_identity_email():
    return pydash.get(saas_config, "stripe.identity_email") or os.environ.get(
        "STRIPE_IDENTITY_EMAIL"
    )


@pytest.fixture(scope="function")
def stripe_erasure_identity_email():
    return "ethyca+stripe+rtf@example.com"


@pytest.fixture
def stripe_config() -> Dict[str, Any]:
    return load_config("data/saas/config/stripe_config.yml")


@pytest.fixture
def stripe_dataset() -> Dict[str, Any]:
    return load_dataset("data/saas/dataset/stripe_dataset.yml")[0]


@pytest.fixture(scope="function")
def stripe_connection_config(
    db: Session, stripe_config: Dict[str, Dict], stripe_secrets: Dict[str, Any]
) -> Generator:
    fides_key = stripe_config["fides_key"]
    connection_config = ConnectionConfig.create(
        db=db,
        data={
            "key": fides_key,
            "name": fides_key,
            "connection_type": ConnectionType.saas,
            "access": AccessLevel.write,
            "secrets": stripe_secrets,
            "saas_config": stripe_config,
        },
    )
    yield connection_config
    connection_config.delete(db)


@pytest.fixture
def stripe_dataset_config(
    db: session,
    stripe_connection_config: ConnectionConfig,
    stripe_dataset: Dict[str, Dict],
) -> Generator:
    fides_key = stripe_dataset["fides_key"]
    stripe_connection_config.name = fides_key
    stripe_connection_config.key = fides_key
    stripe_connection_config.save(db=db)
    dataset = DatasetConfig.create(
        db=db,
        data={
            "connection_config_id": stripe_connection_config.id,
            "fides_key": fides_key,
            "dataset": stripe_dataset,
        },
    )
    yield dataset
    dataset.delete(db=db)


@pytest.fixture(scope="function")
def stripe_create_erasure_data(stripe_secrets) -> Generator:

    base_url = f"https://{stripe_secrets['host']}"

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": f"Bearer {stripe_secrets['api_key']}",
    }

    # customer

    customer_data = {
        "address": {
            "city": "Anaheim",
            "country": "US",
            "line1": "123 Fake St",
            "line2": "Apt 1",
            "postal_code": "92882",
            "state": "CA",
        },
        "balance": 0,
        "description": "RTF Test Customer",
        "email": "ethyca+stripe+rtf@example.com",
        "name": "Ethyca RTF",
        "phone": "+19515551234",
        "preferred_locales": ["en-US"],
        "shipping": {
            "address": {
                "city": "Anaheim",
                "country": "US",
                "line1": "123 Fake St",
                "line2": "Apt 1",
                "postal_code": "92882",
                "state": "CA",
            },
            "name": "Ethyca RTF",
            "phone": "+19515551234",
        },
    }

    response = requests.post(
        url=f"{base_url}/v1/customers",
        headers=headers,
        data=urlencode(customer_data),
    )

    customer = response.json()

    # create other stuff

    yield customer

    requests.delete(
        url=f"{base_url}/v1/customers/{customer['id']}",
        headers=headers
    )

    
