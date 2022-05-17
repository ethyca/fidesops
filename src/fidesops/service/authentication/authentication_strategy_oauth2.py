from typing import Any, Dict

from requests import PreparedRequest
from fidesops.schemas.saas.strategy_configuration import OAuth2AuthenticationConfiguration, StrategyConfiguration

from fidesops.service.authentication.authentication_strategy import (
    AuthenticationStrategy,
)

class OAuth2AuthenticationStrategy(AuthenticationStrategy):
    """
    Replaces the username and password placeholders with the actual credentials
    and uses them to add a basic authentication header to the incoming request.
    """

    strategy_name = "oauth2"

    def __init__(self, configuration: OAuth2AuthenticationConfiguration):
        self.authorization_request = configuration.authorization_request
        self.token_request = configuration.token_request
        self.refresh_request = configuration.refresh_request

    def add_authentication(
        self, request: PreparedRequest, secrets: Dict[str, Any]
    ) -> PreparedRequest:
        """
        Adds the access_token as a bearer token to the request.
        Refreshes the access_token using the provided refresh token
        if the access_token has expired.
        """
        request.headers["Authorization"] = "Bearer " + secrets["access_token"]
        return request

    @staticmethod
    def configuration_model() -> StrategyConfiguration:
        return OAuth2AuthenticationConfiguration
