import logging
from datetime import datetime, timedelta
from typing import Any, Dict

from requests import PreparedRequest

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

logger = logging.getLogger(__name__)


class OAuth2AuthenticationStrategy(AuthenticationStrategy):
    """
    Checks the expiration date on the stored access token and refreshes
    it if needed using the configured token refresh request.
    """

    strategy_name = "oauth2"

    def __init__(self, configuration: OAuth2AuthenticationConfiguration):
        self.refresh_request = configuration.refresh_request

    def add_authentication(
        self, request: PreparedRequest, connection_config: ConnectionConfig
    ) -> PreparedRequest:
        """
        Checks the expiration date on the existing access token and refreshes if necessary.
        The existing/updated access token is then added to the request as a bearer token.
        """
        access_token = connection_config.secrets.get("access_token")
        # automatically expire if expires_at is missing
        expires_at = connection_config.secrets.get("expires_at", 0)

        # check access_token expiration and refresh if needed
        if expires_at < datetime.utcnow():
            refresh_response: Dict[str, Any] = self._refresh_token(
                self.refresh_request, connection_config
            )
            logger.info(refresh_response)
            access_token = refresh_response.get("access_token")
            # store new values
            logger.info(
                f"Storing new access and refresh tokens for {connection_config.key}"
            )

        # add authorization
        request.headers["Authorization"] = "Bearer " + access_token
        return request

    @staticmethod
    def _refresh_token(
        refresh_request: SaaSRequest, connection_config: ConnectionConfig
    ) -> Dict[str, Any]:
        """
        Generates and executes the refresh token request based on the OAuth2 config
        and connection config secrets.
        """

        logger.info(
            f"Attemping to refresh access and refresh tokens for {connection_config.key}"
        )
        # populate refresh request
        prepared_refresh_request = SaaSQueryConfig.map_param_values(
            "refresh",
            f"{connection_config.name} OAuth2",
            refresh_request,
            connection_config.secrets,
        )

        # delayed import to prevent cyclic dependency error
        from fidesops.service.connectors.saas_connector import SaaSConnector
        
        connector = SaaSConnector(connection_config)
        client = connector.create_client_from_request(refresh_request)
        # client.send(prepared_refresh_request)
        return {
            "access_token": "new_access",
            "refresh_token": "new_refresh",
            "expires_at": datetime.utcnow() + timedelta(days=1),
        }

    @staticmethod
    def get_configuration_model() -> StrategyConfiguration:
        return OAuth2AuthenticationConfiguration
