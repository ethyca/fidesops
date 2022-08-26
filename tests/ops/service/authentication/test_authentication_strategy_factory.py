import pytest

from fidesops.ops.common_exceptions import NoSuchStrategyException
from fidesops.ops.service.authentication.authentication_strategy_basic import (
    BasicAuthenticationStrategy,
)
from fidesops.ops.service.authentication.authentication_strategy_bearer import (
    BearerAuthenticationStrategy,
)
from fidesops.ops.service.authentication.authentication_strategy_query_param import (
    QueryParamAuthenticationStrategy,
)
from fidesops.ops.service.strategy_factory import strategy


def test_strategy_basic():
    config = {
        "username": "<username>",
        "password": "<password>",
    }
    basic_strategy = strategy(strategy_name="basic", configuration=config)
    assert isinstance(basic_strategy, BasicAuthenticationStrategy)


def test_strategy_bearer():
    config = {"token": "<api_key>"}
    bearer_strategy = strategy(strategy_name="bearer", configuration=config)
    assert isinstance(bearer_strategy, BearerAuthenticationStrategy)


def test_strategy_query_param():
    config = {"name": "api_key", "value": "<api_key>"}
    query_param_strategy = strategy(strategy_name="query_param", configuration=config)
    assert isinstance(query_param_strategy, QueryParamAuthenticationStrategy)


def test_strategy_invalid_strategy():
    with pytest.raises(NoSuchStrategyException):
        strategy("invalid", {})
