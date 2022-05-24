from datetime import datetime, timedelta
from unittest import mock
from unittest.mock import Mock

import pytest
from requests import PreparedRequest, Request

from fidesops.common_exceptions import OAuth2TokenException
from fidesops.service.authentication.authentication_strategy_factory import get_strategy
from fidesops.service.authentication.authentication_strategy_oauth2 import (
    OAuth2AuthenticationStrategy,
)


class TestAddAuthentication:
    # happy path, being able to use the existing access token
    def test_oauth2_authentication(
        self, oauth2_connection_config, oauth2_configuration
    ):

        # set a future expiration date for the access token
        oauth2_connection_config.secrets["expires_at"] = (
            datetime.utcnow() + timedelta(days=1)
        ).timestamp()

        req: PreparedRequest = Request(method="POST", url="https://localhost").prepare()

        auth_strategy = get_strategy("oauth2", oauth2_configuration)
        authenticated_request = auth_strategy.add_authentication(
            req, oauth2_connection_config
        )
        assert (
            authenticated_request.headers["Authorization"]
            == f"Bearer {oauth2_connection_config.secrets['access_token']}"
        )

    # access token expired, call refresh request
    @mock.patch("fidesops.models.connectionconfig.ConnectionConfig.update")
    @mock.patch("fidesops.service.connectors.saas_connector.AuthenticatedClient.send")
    def test_oauth2_authentication_successful_refresh(
        self,
        mock_send: Mock,
        mock_connection_config_update: Mock,
        oauth2_connection_config,
        oauth2_configuration,
    ):
        # mock the json response from calling the token refresh request
        mock_send().json.return_value = {"access_token": "new_access"}

        # expire the access token
        oauth2_connection_config.secrets["expires_at"] = 0

        # the request we want to authenticate
        req: PreparedRequest = Request(method="POST", url="https://localhost").prepare()

        auth_strategy = get_strategy("oauth2", oauth2_configuration)
        authenticated_request = auth_strategy.add_authentication(
            req, oauth2_connection_config
        )
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
        self, mock_send: Mock, oauth2_connection_config, oauth2_configuration
    ):
        # mock the json response from calling the token refresh request
        mock_send().json.return_value = {"error": "invalid_request"}

        # expire the access token
        oauth2_connection_config.secrets["expires_at"] = 0

        # the request we want to authenticate
        req: PreparedRequest = Request(method="POST", url="https://localhost").prepare()

        auth_strategy = get_strategy("oauth2", oauth2_configuration)
        with pytest.raises(OAuth2TokenException) as exc:
            auth_strategy.add_authentication(req, oauth2_connection_config)
        assert (
            str(exc.value)
            == f"Unable to retrieve token for {oauth2_connection_config.key} (invalid_request)."
        )


class TestAuthorizationUrl:
    @mock.patch("fidesops.service.authentication.authentication_strategy_oauth2.uuid4")
    @mock.patch(
        "fidesops.models.authentication_request.AuthenticationRequest.create_or_update"
    )
    def test_get_authorization_url(
        self,
        mock_create_or_update: Mock,
        mock_uuid: Mock,
        oauth2_connection_config,
        oauth2_configuration,
    ):
        state = "unique_value"
        mock_uuid.return_value = state
        auth_strategy: OAuth2AuthenticationStrategy = get_strategy(
            "oauth2", oauth2_configuration
        )
        assert (
            auth_strategy.get_authorization_url(oauth2_connection_config)
            == "https://localhost/auth/authorize?client_id=client&redirect_uri=https%3A%2F%2Flocalhost%2Fcallback&response_type=code&scope=admin.read+admin.write&state=unique_value"
        )
        mock_create_or_update.assert_called_once_with(
            mock.ANY,
            data={"connection_key": oauth2_connection_config.key, "state": state},
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
        oauth2_connection_config,
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
        auth_strategy.get_access_token("auth_code", oauth2_connection_config)

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
