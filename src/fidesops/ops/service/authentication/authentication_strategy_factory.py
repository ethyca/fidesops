import logging
from enum import Enum
from typing import Any, Dict, List

from pydantic import ValidationError

from fidesops.ops.common_exceptions import NoSuchStrategyException
from fidesops.ops.common_exceptions import ValidationError as FidesopsValidationError
from fidesops.ops.schemas.saas.strategy_configuration import StrategyConfiguration
from fidesops.ops.service.authentication.authentication_strategy import (
    AuthenticationStrategy,
)
from fidesops.ops.service.authentication.authentication_strategy_basic import (
    BasicAuthenticationStrategy,
)
from fidesops.ops.service.authentication.authentication_strategy_bearer import (
    BearerAuthenticationStrategy,
)
from fidesops.ops.service.authentication.authentication_strategy_oauth2_auth_code import (
    OAuth2AuthCodeAuthenticationStrategy,
)
from fidesops.ops.service.authentication.authentication_strategy_oauth2_client_credentials import (
    OAuth2ClientCredentialsAuthenticationStrategy,
)
from fidesops.ops.service.authentication.authentication_strategy_query_param import (
    QueryParamAuthenticationStrategy,
)

logger = logging.getLogger(__name__)


class SupportedAuthenticationStrategies(Enum):
    """
    The supported strategies for authenticating against SaaS APIs.
    """

    basic = BasicAuthenticationStrategy
    bearer = BearerAuthenticationStrategy
    query_param = QueryParamAuthenticationStrategy
    oauth2_auth_code = OAuth2AuthCodeAuthenticationStrategy
    oauth2_client_credentials = OAuth2ClientCredentialsAuthenticationStrategy

    @classmethod
    def __contains__(cls, item: str) -> bool:
        try:
            cls[item]
        except KeyError:
            return False

        return True


def get_strategy(
    strategy_name: str,
    configuration: Dict[str, Any],
) -> AuthenticationStrategy:
    """
    Returns the strategy given the name and configuration.
    Raises NoSuchStrategyException if the strategy does not exist
    """
    if not SupportedAuthenticationStrategies.__contains__(strategy_name):
        valid_strategies = ", ".join(get_strategy_names())
        raise NoSuchStrategyException(
            f"Strategy '{strategy_name}' does not exist. Valid strategies are [{valid_strategies}]"
        )
    strategy = SupportedAuthenticationStrategies[strategy_name].value
    try:
        strategy_config: StrategyConfiguration = strategy.get_configuration_model()(
            **configuration
        )
        return strategy(configuration=strategy_config)
    except ValidationError as e:
        raise FidesopsValidationError(message=str(e))


def get_strategy_names() -> List[str]:
    """Returns all supported authentication strategies"""
    return [s.name for s in SupportedAuthenticationStrategies]
