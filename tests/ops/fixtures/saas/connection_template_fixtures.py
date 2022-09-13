import pytest

from fidesops.ops.api.v1.scope_registry import SAAS_CONNECTION_INSTANTIATE
from fidesops.ops.api.v1.urn_registry import SAAS_CONNECTOR_FROM_TEMPLATE, V1_URL_PREFIX
from fidesops.ops.models.connectionconfig import ConnectionConfig
from fidesops.ops.models.datasetconfig import DatasetConfig


def base_url() -> str:
    return V1_URL_PREFIX + SAAS_CONNECTOR_FROM_TEMPLATE


@pytest.fixture(scope="function")
def secondary_sendgrid_instance(db, generate_auth_header, api_client):
    """
    Instantiate a `sendgrid` SaaS connector instance
    """
    secrets = {
        "domain": "test_sendgrid_domain",
        "api_key": "test_sendgrid_api_key",
    }
    connection_config, dataset_config = instantiate_connector(
        db,
        generate_auth_header,
        api_client,
        "sendgrid",
        "sendgrid_connection_config_secondary",
        "secondary_sendgrid_instance",
        "Sendgrid ConnectionConfig description",
        secrets,
    )
    yield connection_config, dataset_config
    dataset_config.delete(db)
    connection_config.delete(db)


@pytest.fixture(scope="function")
def secondary_mailchimp_instance(db, generate_auth_header, api_client):
    """
    Instantiate a `mailchimp` SaaS connector instance
    """
    connection_config, dataset_config = instantiate_mailchimp(
        db,
        generate_auth_header,
        api_client,
        "mailchimp_connection_config_secondary",
        "secondary_mailchimp_instance",
    )
    yield connection_config, dataset_config
    dataset_config.delete(db)
    connection_config.delete(db)


@pytest.fixture(scope="function")
def tertiary_mailchimp_instance(db, generate_auth_header, api_client):
    """
    Instantiate a `mailchimp` SaaS connector instance
    "Tertiary" is to distinguish this instance from the
    instance created by the `secondary_mailchimp_instance` fixture
    """
    connection_config, dataset_config = instantiate_mailchimp(
        db,
        generate_auth_header,
        api_client,
        "mailchimp_connection_config_tertiary",
        "tertiary_mailchimp_instance",
    )
    yield connection_config, dataset_config
    dataset_config.delete(db)
    connection_config.delete(db)


def instantiate_mailchimp(db, generate_auth_header, api_client, key, fides_key):
    secrets = {
        "domain": "test_mailchimp_domain",
        "username": "test_mailchimp_username",
        "api_key": "test_mailchimp_api_key",
    }
    return instantiate_connector(
        db,
        generate_auth_header,
        api_client,
        "mailchimp",
        key,
        fides_key,
        "Mailchimp ConnectionConfig description",
        secrets,
    )


def instantiate_connector(
    db,
    generate_auth_header,
    api_client,
    connector_type,
    key,
    fides_key,
    description,
    secrets,
):
    """
    Helper to genericize instantiation of a SaaS connector
    """
    connection_config = ConnectionConfig.filter(
        db=db, conditions=(ConnectionConfig.key == key)
    ).first()
    assert connection_config is None

    dataset_config = DatasetConfig.filter(
        db=db,
        conditions=(DatasetConfig.fides_key == fides_key),
    ).first()
    assert dataset_config is None

    auth_header = generate_auth_header(scopes=[SAAS_CONNECTION_INSTANTIATE])
    request_body = {
        "instance_key": fides_key,
        "secrets": secrets,
        "name": key,
        "description": description,
        "key": key,
    }
    resp = api_client.post(
        base_url().format(saas_connector_type=connector_type),
        headers=auth_header,
        json=request_body,
    )

    assert resp.status_code == 200
    assert set(resp.json().keys()) == {"connection", "dataset"}
    connection_data = resp.json()["connection"]
    assert connection_data["key"] == key
    assert connection_data["name"] == key
    assert "secrets" not in connection_data

    dataset_data = resp.json()["dataset"]
    assert dataset_data["fides_key"] == fides_key

    connection_config = ConnectionConfig.filter(
        db=db, conditions=(ConnectionConfig.key == key)
    ).first()
    dataset_config = DatasetConfig.filter(
        db=db,
        conditions=(DatasetConfig.fides_key == fides_key),
    ).first()
    return connection_config, dataset_config
