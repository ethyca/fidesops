import logging
from datetime import datetime, timedelta
from typing import Any, Dict, Optional
from urllib.parse import urlencode

from requests import PreparedRequest

from fidesops.common_exceptions import FidesopsException, SaaSTokenRefreshException
from fidesops.db.session import get_db_session
from fidesops.models.connectionconfig import ConnectionConfig
from fidesops.schemas.saas.saas_config import SaaSRequest
from fidesops.schemas.saas.strategy_configuration import (
    OAuth2AuthenticationConfiguration,
    StrategyConfiguration,
)
from fidesops.service.authentication.authentication_strategy import (
    AuthenticationStrategy,
)
from fidesops.service.connectors.saas_query_config import SaaSQueryConfig
from fidesops.util.logger import NotPii
from fidesops.util.saas_util import assign_placeholders, map_param_values

logger = logging.getLogger(__name__)


class OAuth2AuthenticationStrategy(AuthenticationStrategy):
    """
    Checks the expiration date on the stored access token and refreshes
    it if needed using the configured token refresh request.
    """

    strategy_name = "oauth2"

    def __init__(self, configuration: OAuth2AuthenticationConfiguration):
        self.authorization_request = configuration.authorization_request
        self.refresh_request = configuration.refresh_request

    def add_authentication(
        self, request: PreparedRequest, connection_config: ConnectionConfig
    ) -> PreparedRequest:
        """
        Checks the expiration date on the existing access token and refreshes if necessary.
        The existing/updated access token is then added to the request as a bearer token.
        """

        access_token = connection_config.secrets.get("access_token")
        if access_token is None:
            raise FidesopsException(
                f"OAuth2 access token not found for {connection_config.key}, please "
                f"authenticate connection via /api/v1/connection/{connection_config.key}/authorize"
            )

        # automatically expire if expires_at is missing
        expires_at = connection_config.secrets.get("expires_at") or 0

        if self._close_to_expiration(expires_at):
            refresh_response = self._refresh_token(
                self.refresh_request, connection_config
            )
            access_token = self._update_tokens(refresh_response, connection_config)

        # add access_token to request
        request.headers["Authorization"] = "Bearer " + access_token
        return request

    @staticmethod
    def _close_to_expiration(expires_at: int) -> bool:
        """Check if the access_token will expire in the next 10 minutes"""
        return int(expires_at) < (datetime.utcnow() + timedelta(minutes=10)).timestamp()

    @staticmethod
    def _refresh_token(
        refresh_request: SaaSRequest, connection_config: ConnectionConfig
    ) -> Dict[str, Any]:
        """
        Generates and executes the refresh token request based on the OAuth2 config
        and connection config secrets.
        """

        # delayed import to prevent cyclic dependency
        from fidesops.service.connectors.saas_connector import SaaSConnector

        logger.info(
            f"Attempting to refresh access and refresh tokens for {connection_config.key}"
        )

        connector = SaaSConnector(connection_config)
        client = connector.create_client_from_request(refresh_request)

        try:
            # map param values to placeholders in refresh request
            prepared_refresh_request = map_param_values(
                "refresh",
                f"{connection_config.name} OAuth2",
                refresh_request,
                connection_config.secrets,
            )
            response = client.send(prepared_refresh_request)
            refresh_response = response.json()
        except Exception as exc:
            logger.error(
                "Error occurred refreshing the OAuth2 access token for %s: %s",
                NotPii(connection_config.key),
                str(exc),
            )
            raise SaaSTokenRefreshException(
                f"Error occurred refreshing the OAuth2 access token for {connection_config.key}"
            )

        return refresh_response

    @staticmethod
    def _update_tokens(
        refresh_response: Dict[str, Any], connection_config: ConnectionConfig
    ) -> str:
        """
        Persists and returns the new access token.
        Also updates the refresh token if one is provided.
        """

        access_token = refresh_response.get("access_token")

        if access_token is None:
            raise SaaSTokenRefreshException(
                f"The token refresh response for {connection_config.key} is missing an access_token"
            )

        data = {"access_token": access_token}

        # The authorization server MAY issue a new refresh token, in which case
        # the client MUST discard the old refresh token and replace it with the
        # new refresh token.
        #
        # https://datatracker.ietf.org/doc/html/rfc6749#section-6

        refresh_token = refresh_response.get("refresh_token")
        if refresh_token is not None:
            data["refresh_token"] = refresh_token

        # persist new tokens to the database
        SessionLocal = get_db_session()
        db = SessionLocal()
        updated_connection_config = ConnectionConfig.get_by(
            db, field="key", value=connection_config.key
        )
        updated_connection_config.update(db, data=data)

        logger.info(
            f"Successfully updated the OAuth2 token(s) for {connection_config.key}"
        )

        return access_token

    def get_authorization_url(
        self, connection_config: ConnectionConfig
    ) -> Optional[str]:
        """Returns the authorization URL to initiate the OAuth2 workflow"""

        # assign placeholders in the authorization request config
        prepared_authorization_request = map_param_values(
            "authorize",
            f"{connection_config.name} OAuth2",
            self.authorization_request,
            connection_config.secrets,
        )

        # get the client config from the authorization request or default
        # to the base client config if one isn't provided
        client_config = (
            self.authorization_request.client_config
            if self.authorization_request.client_config
            else connection_config.get_saas_config().client_config
        )

        # build the complete URL with query params
        return (
            f"{client_config.protocol}://{assign_placeholders(client_config.host, connection_config.secrets)}"
            f"{prepared_authorization_request.path}"
            f"?{urlencode(prepared_authorization_request.query_params)}"
        )

    @staticmethod
    def get_configuration_model() -> StrategyConfiguration:
        return OAuth2AuthenticationConfiguration
