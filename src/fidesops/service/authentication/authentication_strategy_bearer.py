from typing import Any, Dict

from requests import PreparedRequest

from fidesops.schemas.saas.strategy_configuration import (
    BearerAuthenticationConfiguration,
    StrategyConfiguration,
)
from fidesops.service.authentication.authentication_strategy import (
    AuthenticationStrategy,
)
from fidesops.util.saas_util import assign_placeholders

STRATEGY_NAME = "bearer"


class BearerAuthenticationStrategy(AuthenticationStrategy):
    def __init__(self, configuration: BearerAuthenticationConfiguration):
        self.token = configuration.token

    def get_strategy_name(self) -> str:
        return STRATEGY_NAME

    def add_authentication(
        self, request: PreparedRequest, secrets: Dict[str, Any]
    ) -> PreparedRequest:
        """Add bearer authentication to the request"""
        request.headers["Authorization"] = "Bearer " + assign_placeholders(
            self.token, secrets
        )
        return request

    @staticmethod
    def get_configuration_model() -> StrategyConfiguration:
        return BearerAuthenticationConfiguration
