from datetime import datetime, timedelta
from unittest import mock
from unittest.mock import Mock

import pytest
from requests import PreparedRequest, Request

from fidesops.common_exceptions import SaaSTokenRefreshException
from fidesops.models.connectionconfig import ConnectionConfig
from fidesops.schemas.saas.strategy_configuration import (
    OAuth2AuthenticationConfiguration,
)
from fidesops.service.authentication.authentication_strategy_factory import get_strategy


@pytest.fixture(scope="session")
def oauth2_configuration() -> OAuth2AuthenticationConfiguration:
    return {
        "authorization_request": {
            "method": "GET",
            "path": "/auth/authorize",
            "query_params": [
                {"name": "client_id", "value": "<client_id>"},
                {"name": "redirect_uri", "value": "<redirect_uri>"},
                {"name": "response_type", "value": "code"},
                {
                    "name": "scope",
                    "value": "full_access",
                },
            ],
        },
        "token_request": {
            "method": "POST",
            "path": "/oauth/token",
            "headers": [
                {
                    "name": "Content-Type",
                    "value": "application/x-www-form-urlencoded",
                }
            ],
            "query_params": [
                {"name": "client_id", "value": "<client_id>"},
                {"name": "client_secret", "value": "<client_secret>"},
                {"name": "grant_type", "value": "authorization_code"},
                {"name": "code", "value": "<code>"},
                {"name": "redirect_uri", "value": "<redirect_uri>"},
            ],
        },
        "refresh_request": {
            "method": "POST",
            "path": "/oauth/token",
            "headers": [
                {
                    "name": "Content-Type",
                    "value": "application/x-www-form-urlencoded",
                }
            ],
            "query_params": [
                {"name": "client_id", "value": "<client_id>"},
                {"name": "client_secret", "value": "<client_secret>"},
                {"name": "redirect_uri", "value": "<redirect_uri>"},
                {"name": "grant_type", "value": "refresh_token"},
                {"name": "refresh_token", "value": "<refresh_token>"},
            ],
        },
    }


@pytest.fixture(scope="function")
def connection_config(oauth2_configuration) -> ConnectionConfig:
    secrets = {
        "domain": "localhost",
        "client_id": "client",
        "client_secret": "secret",
        "redirect_uri": "https://localhost/callback",
        "access_token": "access",
        "refersh_token": "refresh",
    }
    saas_config = {
        "fides_key": "oauth2_connector",
        "name": "OAuth2 Connector",
        "description": "Generic OAuth2 connector for testing",
        "version": "0.0.1",
        "connector_params": [{"name": item} for item in secrets.values()],
        "client_config": {
            "protocol": "https",
            "host": secrets["domain"],
            "authentication": {
                "strategy": "oauth2",
                "configuration": oauth2_configuration,
            },
        },
        "endpoints": [],
        "test_request": {"method": "GET", "path": "/test"},
    }

    return ConnectionConfig(
        key="oauth2_connector_example", secrets=secrets, saas_config=saas_config
    )


# happy path, being able to use the existing access token
def test_oauth2_authentication(connection_config, oauth2_configuration):

    # set a future expiration date for the access token
    connection_config.secrets["expires_at"] = (
        datetime.utcnow() + timedelta(days=1)
    ).timestamp()

    req: PreparedRequest = Request(method="POST", url="https://localhost").prepare()

    auth_strategy = get_strategy("oauth2", oauth2_configuration)
    authenticated_request = auth_strategy.add_authentication(req, connection_config)
    assert (
        authenticated_request.headers["Authorization"]
        == f"Bearer {connection_config.secrets['access_token']}"
    )


# access token expired call refresh request
@mock.patch("fidesops.models.connectionconfig.ConnectionConfig.update")
@mock.patch("fidesops.service.connectors.saas_connector.AuthenticatedClient.send")
def test_oauth2_authentication_successful_refresh(
    mock_send: Mock,
    mock_connection_config_update: Mock,
    connection_config,
    oauth2_configuration,
):
    # mock the json response from calling the token refresh request
    mock_send().json.return_value = {"access_token": "new_access"}

    # expire the access token
    connection_config.secrets["expires_at"] = 0

    # the request we want to authenticate
    req: PreparedRequest = Request(method="POST", url="https://localhost").prepare()

    auth_strategy = get_strategy("oauth2", oauth2_configuration)
    authenticated_request = auth_strategy.add_authentication(req, connection_config)
    assert authenticated_request.headers["Authorization"] == "Bearer new_access"

    # verify correct values from connection_config update
    mock_connection_config_update.assert_called_with(
        mock.ANY, data={"access_token": "new_access"}
    )


# access token expired, unable to refresh
@mock.patch("fidesops.service.connectors.saas_connector.AuthenticatedClient.send")
def test_oauth2_authentication_failed_refresh(
    mock_send: Mock, connection_config, oauth2_configuration
):
    # mock the json response from calling the token refresh request
    mock_send().json.return_value = {"error": "invalid_request"}

    # expire the access token
    connection_config.secrets["expires_at"] = 0

    # the request we want to authenticate
    req: PreparedRequest = Request(method="POST", url="https://localhost").prepare()

    auth_strategy = get_strategy("oauth2", oauth2_configuration)
    with pytest.raises(SaaSTokenRefreshException) as exc:
        auth_strategy.add_authentication(req, connection_config)
    assert (
        str(exc.value)
        == f"The token refresh response for {connection_config.key} is missing an access_token"
    )
