from abc import abstractmethod

from requests import PreparedRequest

from fidesops.models.connectionconfig import ConnectionConfig
from fidesops.schemas.saas.strategy_configuration import StrategyConfiguration
from fidesops.service.generic_strategy import GenericStrategy


class AuthenticationStrategy(GenericStrategy):
    """Abstract base class for SaaS authentication strategies"""

    @abstractmethod
    def add_authentication(
        self, request: PreparedRequest, connection_config: ConnectionConfig
    ) -> PreparedRequest:
        """Add authentication to the request"""
