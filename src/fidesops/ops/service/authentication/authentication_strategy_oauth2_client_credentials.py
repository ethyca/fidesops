import logging
from typing import List

from requests import PreparedRequest

from fidesops.ops.models.connectionconfig import ConnectionConfig
from fidesops.ops.schemas.saas.strategy_configuration import (
    OAuth2ClientCredentialsConfiguration,
    StrategyConfiguration,
)
from fidesops.ops.service.authentication.authentication_strategy_oauth2_base import (
    OAuth2AuthenticationStrategyBase,
)

logger = logging.getLogger(__name__)


class OAuth2ClientCredentialsAuthenticationStrategy(OAuth2AuthenticationStrategyBase):
    """
    Checks the expiration date on the stored access token and refreshes
    it if needed using the configured token refresh request.
    """

    strategy_name = "oauth2_client_credentials"

    def __init__(self, configuration: OAuth2ClientCredentialsConfiguration):
        self.expires_in = configuration.expires_in
        self.token_request = configuration.token_request
        self.refresh_request = configuration.refresh_request

    def add_authentication(
        self, request: PreparedRequest, connection_config: ConnectionConfig
    ) -> PreparedRequest:
        """
        Checks the expiration date on the existing access token and refreshes if necessary.
        The existing/updated access token is then added to the request as a bearer token.
        """

        access_token = connection_config.secrets.get("access_token")  # type: ignore
        if not access_token:
            access_token = self.get_access_token(connection_config, None)
        elif self.refresh_request:
            access_token = self._refresh_token(connection_config)

        # add access_token to request
        request.headers["Authorization"] = "Bearer " + access_token
        return request

    @staticmethod
    def _required_secrets() -> List[str]:
        return ["client_id", "client_secret"]

    @staticmethod
    def get_configuration_model() -> StrategyConfiguration:
        return OAuth2ClientCredentialsConfiguration  # type: ignore
