from datetime import datetime, timedelta
from unittest import mock
from unittest.mock import Mock

import pytest
from requests import PreparedRequest, Request
from sqlalchemy.orm import Session

from fidesops.common_exceptions import OAuth2TokenException
from fidesops.models.connectionconfig import (
    AccessLevel,
    ConnectionConfig,
    ConnectionType,
)
from fidesops.schemas.saas.strategy_configuration import (
    OAuth2AuthenticationConfiguration,
)
from fidesops.service.authentication.authentication_strategy_factory import get_strategy
from fidesops.service.authentication.authentication_strategy_oauth2 import (
    OAuth2AuthenticationStrategy,
)


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
                    "value": "admin.read admin.write",
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
def connection_config(db: Session, oauth2_configuration) -> ConnectionConfig:
    secrets = {
        "domain": "localhost",
        "client_id": "client",
        "client_secret": "secret",
        "redirect_uri": "https://localhost/callback",
        "access_token": "access",
        "refresh_token": "refresh",
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

    fides_key = saas_config["fides_key"]
    connection_config = ConnectionConfig.create(
        db=db,
        data={
            "key": fides_key,
            "name": fides_key,
            "connection_type": ConnectionType.saas,
            "access": AccessLevel.write,
            "secrets": secrets,
            "saas_config": saas_config,
        },
    )
    yield connection_config
    connection_config.delete(db)


class TestAddAuthentication:
    # happy path, being able to use the existing access token
    def test_oauth2_authentication(self, connection_config, oauth2_configuration):

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

    # access token expired, call refresh request
    @mock.patch("fidesops.models.connectionconfig.ConnectionConfig.update")
    @mock.patch("fidesops.service.connectors.saas_connector.AuthenticatedClient.send")
    def test_oauth2_authentication_successful_refresh(
        self,
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

        # verify correct values for connection_config update
        mock_connection_config_update.assert_called_once_with(
            mock.ANY,
            data={
                "secrets": {
                    "domain": "localhost",
                    "client_id": "client",
                    "client_secret": "secret",
                    "redirect_uri": "https://localhost/callback",
                    "access_token": "new_access",
                    "refresh_token": "refresh",
                    "expires_at": 0,
                }
            },
        )

    # access token expired, unable to refresh
    @mock.patch("fidesops.service.connectors.saas_connector.AuthenticatedClient.send")
    def test_oauth2_authentication_failed_refresh(
        self, mock_send: Mock, connection_config, oauth2_configuration
    ):
        # mock the json response from calling the token refresh request
        mock_send().json.return_value = {"error": "invalid_request"}

        # expire the access token
        connection_config.secrets["expires_at"] = 0

        # the request we want to authenticate
        req: PreparedRequest = Request(method="POST", url="https://localhost").prepare()

        auth_strategy = get_strategy("oauth2", oauth2_configuration)
        with pytest.raises(OAuth2TokenException) as exc:
            auth_strategy.add_authentication(req, connection_config)
        assert (
            str(exc.value)
            == f"Unable to retrieve token for {connection_config.key} (invalid_request)."
        )


class TestAuthorizationUrl:
    @mock.patch("fidesops.service.authentication.authentication_strategy_oauth2.uuid4")
    def test_get_authorization_url(
        self, mock_uuid: Mock, connection_config, oauth2_configuration
    ):
        mock_uuid.return_value = "unique_value"
        auth_strategy: OAuth2AuthenticationStrategy = get_strategy(
            "oauth2", oauth2_configuration
        )
        assert (
            auth_strategy.get_authorization_url(connection_config)
            == "https://localhost/auth/authorize?client_id=client&redirect_uri=https%3A%2F%2Flocalhost%2Fcallback&response_type=code&scope=admin.read+admin.write&state=unique_value"
        )


class TestAccessTokenRequest:
    @mock.patch("datetime.datetime")
    @mock.patch("fidesops.models.connectionconfig.ConnectionConfig.update")
    @mock.patch("fidesops.service.connectors.saas_connector.AuthenticatedClient.send")
    def test_get_access_token(
        self,
        mock_send: Mock,
        mock_connection_config_update: Mock,
        mock_time: Mock,
        connection_config,
        oauth2_configuration,
    ):
        # cast some time magic
        mock_time.utcnow.return_value = datetime(2022, 5, 22)

        # mock the json response from calling the access token request
        expires_in = 7200
        mock_send().json.return_value = {
            "access_token": "new_access",
            "refresh_token": "new_refresh",
            "expires_in": expires_in,
        }

        auth_strategy: OAuth2AuthenticationStrategy = get_strategy(
            "oauth2", oauth2_configuration
        )
        auth_strategy.get_access_token("auth_code", connection_config)

        # verify correct values for connection_config update
        mock_connection_config_update.assert_called_once_with(
            mock.ANY,
            data={
                "secrets": {
                    "domain": "localhost",
                    "client_id": "client",
                    "client_secret": "secret",
                    "redirect_uri": "https://localhost/callback",
                    "access_token": "new_access",
                    "refresh_token": "new_refresh",
                    "code": "auth_code",
                    "expires_at": int(datetime.utcnow().timestamp()) + expires_in,
                }
            },
        )
