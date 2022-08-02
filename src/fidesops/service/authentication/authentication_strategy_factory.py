import logging

from fidesops.service.authentication.authentication_strategy import (
    AuthenticationStrategy,
)
from fidesops.service.generic_strategy_factory import GenericStrategyFactory

logger = logging.getLogger(__name__)


class AuthenticationStrategyFactory(GenericStrategyFactory[AuthenticationStrategy]):
    pass


authentication_strategy_factory = AuthenticationStrategyFactory()
register = authentication_strategy_factory.register
get_strategy = authentication_strategy_factory.get_strategy
