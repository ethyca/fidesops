from datetime import datetime, timedelta
from unittest import mock
from unittest.mock import Mock

import pytest
from requests import PreparedRequest, Request
from sqlalchemy.orm import Session

from fidesops.common_exceptions import FidesopsException, OAuth2TokenException
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

    def test_oauth2_authentication_missing_access_token(
        self, oauth2_connection_config, oauth2_configuration
    ):
        # remove the access_token
        oauth2_connection_config.secrets["access_token"] = None

        req: PreparedRequest = Request(method="POST", url="https://localhost").prepare()

        auth_strategy = get_strategy("oauth2", oauth2_configuration)
        with pytest.raises(FidesopsException) as exc:
            auth_strategy.add_authentication(req, oauth2_connection_config)
        assert str(exc.value) == (
            f"OAuth2 access token not found for {oauth2_connection_config.key}, please "
            f"authenticate connection via /api/v1/connection/{oauth2_connection_config.key}/authorize"
        )

    def test_oauth2_authentication_empty_access_token(
        self, oauth2_connection_config, oauth2_configuration
    ):
        # replace the access_token with an empty string
        oauth2_connection_config.secrets["access_token"] = ""

        req: PreparedRequest = Request(method="POST", url="https://localhost").prepare()

        auth_strategy = get_strategy("oauth2", oauth2_configuration)
        with pytest.raises(FidesopsException) as exc:
            auth_strategy.add_authentication(req, oauth2_connection_config)
        assert str(exc.value) == (
            f"OAuth2 access token not found for {oauth2_connection_config.key}, please "
            f"authenticate connection via /api/v1/connection/{oauth2_connection_config.key}/authorize"
        )

    def test_oauth2_authentication_missing_secrets(
        self, oauth2_connection_config, oauth2_configuration
    ):
        # mix of missing and empty secrets
        oauth2_connection_config.secrets["client_id"] = None
        oauth2_connection_config.secrets["client_secret"] = ""

        req: PreparedRequest = Request(method="POST", url="https://localhost").prepare()

        auth_strategy = get_strategy("oauth2", oauth2_configuration)
        with pytest.raises(FidesopsException) as exc:
            auth_strategy.add_authentication(req, oauth2_connection_config)
        assert (
            str(exc.value)
            == f"Missing required secret(s) 'client_id, client_secret' for oauth2_connector"
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

    # no refresh request defined, should still add access token
    def test_oauth2_authentication_no_refresh(
        self, oauth2_connection_config, oauth2_configuration
    ):
        oauth2_configuration["refresh_request"] = None

        # the request we want to authenticate
        req: PreparedRequest = Request(method="POST", url="https://localhost").prepare()

        auth_strategy = get_strategy("oauth2", oauth2_configuration)
        authenticated_request = auth_strategy.add_authentication(
            req, oauth2_connection_config
        )
        assert (
            authenticated_request.headers["Authorization"]
            == f"Bearer {oauth2_connection_config.secrets['access_token']}"
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
        db: Session,
        oauth2_connection_config,
        oauth2_configuration,
    ):
        state = "unique_value"
        mock_uuid.return_value = state
        auth_strategy: OAuth2AuthenticationStrategy = get_strategy(
            "oauth2", oauth2_configuration
        )
        assert (
            auth_strategy.get_authorization_url(db, oauth2_connection_config)
            == "https://localhost/auth/authorize?client_id=client&redirect_uri=https%3A%2F%2Flocalhost%2Fcallback&response_type=code&scope=admin.read+admin.write&state=unique_value"
        )
        mock_create_or_update.assert_called_once_with(
            mock.ANY,
            data={"connection_key": oauth2_connection_config.key, "state": state},
        )

    def test_get_authorization_url_missing_secrets(
        self,
        db: Session,
        oauth2_connection_config,
        oauth2_configuration,
    ):

        # erase some secrets
        oauth2_connection_config.secrets["client_id"] = None
        oauth2_connection_config.secrets["client_secret"] = ""

        auth_strategy: OAuth2AuthenticationStrategy = get_strategy(
            "oauth2", oauth2_configuration
        )
        with pytest.raises(FidesopsException) as exc:
            auth_strategy.get_authorization_url(db, oauth2_connection_config)
        assert (
            str(exc.value)
            == f"Missing required secret(s) 'client_id, client_secret' for oauth2_connector"
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
        db: Session,
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
        auth_strategy.get_access_token(db, "auth_code", oauth2_connection_config)

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

    # make sure we can use the expires_in value in the config if no expires_in is provided
    # in the access token response
    @mock.patch("datetime.datetime")
    @mock.patch("fidesops.models.connectionconfig.ConnectionConfig.update")
    @mock.patch("fidesops.service.connectors.saas_connector.AuthenticatedClient.send")
    def test_get_access_token_no_expires_in(
        self,
        mock_send: Mock,
        mock_connection_config_update: Mock,
        mock_time: Mock,
        db: Session,
        oauth2_connection_config,
        oauth2_configuration,
    ):
        # set a fixed time
        mock_time.utcnow.return_value = datetime(2022, 5, 22)

        # mock the json response from calling the access token request
        mock_send().json.return_value = {
            "access_token": "new_access",
            "refresh_token": "new_refresh",
        }

        oauth2_configuration["expires_in"] = 3600
        auth_strategy: OAuth2AuthenticationStrategy = get_strategy(
            "oauth2", oauth2_configuration
        )
        auth_strategy.get_access_token(db, "auth_code", oauth2_connection_config)

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
                    "expires_at": int(datetime.utcnow().timestamp())
                    + oauth2_configuration["expires_in"],
                }
            },
        )

    def test_get_access_token_missing_secrets(
        self,
        db: Session,
        oauth2_connection_config,
        oauth2_configuration,
    ):
        # erase some secrets
        oauth2_connection_config.secrets["client_id"] = None
        oauth2_connection_config.secrets["client_secret"] = ""

        auth_strategy: OAuth2AuthenticationStrategy = get_strategy(
            "oauth2", oauth2_configuration
        )
        with pytest.raises(FidesopsException) as exc:
            auth_strategy.get_access_token(db, "auth_code", oauth2_connection_config)
        assert (
            str(exc.value)
            == f"Missing required secret(s) 'client_id, client_secret' for oauth2_connector"
        )
