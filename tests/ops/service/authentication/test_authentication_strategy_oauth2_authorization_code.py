from datetime import datetime, timedelta
from typing import Generator
from unittest import mock
from unittest.mock import Mock

import pytest
from requests import PreparedRequest, Request
from sqlalchemy.orm import Session

from fidesops.ops.common_exceptions import FidesopsException, OAuth2TokenException
from fidesops.ops.models.connectionconfig import (
    AccessLevel,
    ConnectionConfig,
    ConnectionType,
)
from fidesops.ops.schemas.saas.strategy_configuration import (
    OAuth2AuthCodeAuthenticationConfiguration,
)
from fidesops.ops.service.authentication.authentication_strategy_factory import (
    get_strategy,
)
from fidesops.ops.service.authentication.authentication_strategy_oauth2_authorization_code import (
    OAuth2AuthorizationCodeAuthenticationStrategy,
)


@pytest.fixture(scope="function")
def oauth2_authorization_code_configuration() -> OAuth2AuthCodeAuthenticationConfiguration:
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
                {"name": "state", "value": "<state>"},
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
def oauth2_authorization_code_connection_config(
    db: Session, oauth2_authorization_code_configuration
) -> Generator:
    secrets = {
        "domain": "localhost",
        "client_id": "client",
        "client_secret": "secret",
        "redirect_uri": "https://localhost/callback",
        "access_token": "access",
        "refresh_token": "refresh",
    }
    saas_config = {
        "fides_key": "oauth2_authorization_code_connector",
        "name": "OAuth2 Auth Code Connector",
        "type": "custom",
        "description": "Generic OAuth2 connector for testing",
        "version": "0.0.1",
        "connector_params": [{"name": item} for item in secrets.keys()],
        "client_config": {
            "protocol": "https",
            "host": secrets["domain"],
            "authentication": {
                "strategy": "oauth2_authorization_code",
                "configuration": oauth2_authorization_code_configuration,
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
    def test_oauth2_authentication(
        self,
        oauth2_authorization_code_connection_config,
        oauth2_authorization_code_configuration,
    ):
        # set a future expiration date for the access token
        oauth2_authorization_code_connection_config.secrets["expires_at"] = (
            datetime.utcnow() + timedelta(days=1)
        ).timestamp()

        req: PreparedRequest = Request(method="POST", url="https://localhost").prepare()

        auth_strategy: OAuth2AuthorizationCodeAuthenticationStrategy = get_strategy(
            "oauth2_authorization_code", oauth2_authorization_code_configuration
        )
        authenticated_request = auth_strategy.add_authentication(
            req, oauth2_authorization_code_connection_config
        )
        assert (
            authenticated_request.headers["Authorization"]
            == f"Bearer {oauth2_authorization_code_connection_config.secrets['access_token']}"
        )

    def test_oauth2_authentication_missing_access_token(
        self,
        oauth2_authorization_code_connection_config,
        oauth2_authorization_code_configuration,
    ):
        # remove the access_token
        oauth2_authorization_code_connection_config.secrets["access_token"] = None

        req: PreparedRequest = Request(method="POST", url="https://localhost").prepare()

        auth_strategy = get_strategy(
            "oauth2_authorization_code", oauth2_authorization_code_configuration
        )
        with pytest.raises(FidesopsException) as exc:
            auth_strategy.add_authentication(
                req, oauth2_authorization_code_connection_config
            )
        assert str(exc.value) == (
            f"OAuth2 access token not found for {oauth2_authorization_code_connection_config.key}, please "
            f"authenticate connection via /api/v1/connection/{oauth2_authorization_code_connection_config.key}/authorize"
        )

    def test_oauth2_authentication_empty_access_token(
        self,
        oauth2_authorization_code_connection_config,
        oauth2_authorization_code_configuration,
    ):
        # replace the access_token with an empty string
        oauth2_authorization_code_connection_config.secrets["access_token"] = ""

        req: PreparedRequest = Request(method="POST", url="https://localhost").prepare()

        auth_strategy = get_strategy(
            "oauth2_authorization_code", oauth2_authorization_code_configuration
        )
        with pytest.raises(FidesopsException) as exc:
            auth_strategy.add_authentication(
                req, oauth2_authorization_code_connection_config
            )
        assert str(exc.value) == (
            f"OAuth2 access token not found for {oauth2_authorization_code_connection_config.key}, please "
            f"authenticate connection via /api/v1/connection/{oauth2_authorization_code_connection_config.key}/authorize"
        )

    def test_oauth2_authentication_missing_secrets(
        self,
        oauth2_authorization_code_connection_config,
        oauth2_authorization_code_configuration,
    ):
        # mix of missing and empty secrets
        oauth2_authorization_code_connection_config.secrets["client_id"] = None
        oauth2_authorization_code_connection_config.secrets["client_secret"] = ""

        req: PreparedRequest = Request(method="POST", url="https://localhost").prepare()

        auth_strategy = get_strategy(
            "oauth2_authorization_code", oauth2_authorization_code_configuration
        )
        with pytest.raises(FidesopsException) as exc:
            auth_strategy.add_authentication(
                req, oauth2_authorization_code_connection_config
            )
        assert (
            str(exc.value)
            == f"Missing required secret(s) 'client_id, client_secret' for oauth2_authorization_code_connector"
        )

    # access token expired, call refresh request
    @mock.patch("fidesops.ops.models.connectionconfig.ConnectionConfig.update")
    @mock.patch(
        "fidesops.ops.service.connectors.saas_connector.AuthenticatedClient.send"
    )
    def test_oauth2_authentication_successful_refresh(
        self,
        mock_send: Mock,
        mock_connection_config_update: Mock,
        oauth2_authorization_code_connection_config,
        oauth2_authorization_code_configuration,
    ):
        # mock the json response from calling the token refresh request
        mock_send().json.return_value = {"access_token": "new_access"}

        # expire the access token
        oauth2_authorization_code_connection_config.secrets["expires_at"] = 0

        # the request we want to authenticate
        req: PreparedRequest = Request(method="POST", url="https://localhost").prepare()

        auth_strategy = get_strategy(
            "oauth2_authorization_code", oauth2_authorization_code_configuration
        )
        authenticated_request = auth_strategy.add_authentication(
            req, oauth2_authorization_code_connection_config
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
        self,
        oauth2_authorization_code_connection_config,
        oauth2_authorization_code_configuration,
    ):
        oauth2_authorization_code_configuration["refresh_request"] = None

        # the request we want to authenticate
        req: PreparedRequest = Request(method="POST", url="https://localhost").prepare()

        auth_strategy = get_strategy(
            "oauth2_authorization_code", oauth2_authorization_code_configuration
        )
        authenticated_request = auth_strategy.add_authentication(
            req, oauth2_authorization_code_connection_config
        )
        assert (
            authenticated_request.headers["Authorization"]
            == f"Bearer {oauth2_authorization_code_connection_config.secrets['access_token']}"
        )

    # access token expired, unable to refresh
    @mock.patch(
        "fidesops.ops.service.connectors.saas_connector.AuthenticatedClient.send"
    )
    def test_oauth2_authentication_failed_refresh(
        self,
        mock_send: Mock,
        oauth2_authorization_code_connection_config,
        oauth2_authorization_code_configuration,
    ):
        # mock the json response from calling the token refresh request
        mock_send().json.return_value = {"error": "invalid_request"}

        # expire the access token
        oauth2_authorization_code_connection_config.secrets["expires_at"] = 0

        # the request we want to authenticate
        req: PreparedRequest = Request(method="POST", url="https://localhost").prepare()

        auth_strategy = get_strategy(
            "oauth2_authorization_code", oauth2_authorization_code_configuration
        )
        with pytest.raises(OAuth2TokenException) as exc:
            auth_strategy.add_authentication(
                req, oauth2_authorization_code_connection_config
            )
        assert (
            str(exc.value)
            == f"Unable to retrieve token for {oauth2_authorization_code_connection_config.key} (invalid_request)."
        )


class TestAuthorizationUrl:
    @mock.patch(
        "fidesops.ops.service.authentication.authentication_strategy_oauth2_authorization_code.OAuth2AuthCodeAuthenticationStrategy._generate_state"
    )
    @mock.patch(
        "fidesops.ops.models.authentication_request.AuthenticationRequest.create_or_update"
    )
    def test_get_authorization_url(
        self,
        mock_create_or_update: Mock,
        mock_state: Mock,
        db: Session,
        oauth2_authorization_code_connection_config,
        oauth2_authorization_code_configuration,
    ):
        state = "unique_value"
        mock_state.return_value = state
        auth_strategy: OAuth2AuthorizationCodeAuthenticationStrategy = get_strategy(
            "oauth2_authorization_code", oauth2_authorization_code_configuration
        )
        assert (
            auth_strategy.get_authorization_url(
                db, oauth2_authorization_code_connection_config
            )
            == "https://localhost/auth/authorize?client_id=client&redirect_uri=https%3A%2F%2Flocalhost%2Fcallback&response_type=code&scope=admin.read+admin.write&state=unique_value"
        )
        mock_create_or_update.assert_called_once_with(
            mock.ANY,
            data={
                "connection_key": oauth2_authorization_code_connection_config.key,
                "state": state,
            },
        )

    def test_get_authorization_url_missing_secrets(
        self,
        db: Session,
        oauth2_authorization_code_connection_config,
        oauth2_authorization_code_configuration,
    ):

        # erase some secrets
        oauth2_authorization_code_connection_config.secrets["client_id"] = None
        oauth2_authorization_code_connection_config.secrets["client_secret"] = ""

        auth_strategy: OAuth2AuthorizationCodeAuthenticationStrategy = get_strategy(
            "oauth2_authorization_code", oauth2_authorization_code_configuration
        )
        with pytest.raises(FidesopsException) as exc:
            auth_strategy.get_authorization_url(
                db, oauth2_authorization_code_connection_config
            )
        assert (
            str(exc.value)
            == f"Missing required secret(s) 'client_id, client_secret' for oauth2_authorization_code_connector"
        )


class TestAccessTokenRequest:
    @mock.patch("datetime.datetime")
    @mock.patch("fidesops.ops.models.connectionconfig.ConnectionConfig.update")
    @mock.patch(
        "fidesops.ops.service.connectors.saas_connector.AuthenticatedClient.send"
    )
    def test_get_access_token(
        self,
        mock_send: Mock,
        mock_connection_config_update: Mock,
        mock_time: Mock,
        db: Session,
        oauth2_authorization_code_connection_config,
        oauth2_authorization_code_configuration,
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

        auth_strategy: OAuth2AuthorizationCodeAuthenticationStrategy = get_strategy(
            "oauth2_authorization_code", oauth2_authorization_code_configuration
        )
        oauth2_authorization_code_connection_config.secrets = {
            **oauth2_authorization_code_connection_config.secrets,
            "code": "auth_code",
        }
        auth_strategy.get_access_token(oauth2_authorization_code_connection_config, db)

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
    @mock.patch("fidesops.ops.models.connectionconfig.ConnectionConfig.update")
    @mock.patch(
        "fidesops.ops.service.connectors.saas_connector.AuthenticatedClient.send"
    )
    def test_get_access_token_no_expires_in(
        self,
        mock_send: Mock,
        mock_connection_config_update: Mock,
        mock_time: Mock,
        db: Session,
        oauth2_authorization_code_connection_config,
        oauth2_authorization_code_configuration,
    ):
        # set a fixed time
        mock_time.utcnow.return_value = datetime(2022, 5, 22)

        # mock the json response from calling the access token request
        mock_send().json.return_value = {
            "access_token": "new_access",
            "refresh_token": "new_refresh",
        }

        oauth2_authorization_code_configuration["expires_in"] = 3600
        auth_strategy: OAuth2AuthorizationCodeAuthenticationStrategy = get_strategy(
            "oauth2_authorization_code", oauth2_authorization_code_configuration
        )
        oauth2_authorization_code_connection_config.secrets = {
            **oauth2_authorization_code_connection_config.secrets,
            "code": "auth_code",
        }
        auth_strategy.get_access_token(oauth2_authorization_code_connection_config, db)

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
                    + oauth2_authorization_code_configuration["expires_in"],
                }
            },
        )

    def test_get_access_token_missing_secrets(
        self,
        db: Session,
        oauth2_authorization_code_connection_config,
        oauth2_authorization_code_configuration,
    ):
        # erase some secrets
        oauth2_authorization_code_connection_config.secrets["client_id"] = None
        oauth2_authorization_code_connection_config.secrets["client_secret"] = ""

        auth_strategy: OAuth2AuthorizationCodeAuthenticationStrategy = get_strategy(
            "oauth2_authorization_code", oauth2_authorization_code_configuration
        )
        with pytest.raises(FidesopsException) as exc:
            oauth2_authorization_code_connection_config.secrets = {
                **oauth2_authorization_code_connection_config.secrets,
                "code": "auth_code",
            }
            auth_strategy.get_access_token(
                oauth2_authorization_code_connection_config, db
            )
        assert (
            str(exc.value)
            == f"Missing required secret(s) 'client_id, client_secret' for oauth2_authorization_code_connector"
        )
