import pytest

from fidesops.common_exceptions import NoSuchStrategyException, ValidationError
from fidesops.service.processors.post_processor_strategy.post_processor_strategy_filter import (
    FilterPostProcessorStrategy,
)
from fidesops.service.processors.post_processor_strategy.post_processor_strategy_unwrap import (
    UnwrapPostProcessorStrategy,
)
from fidesops.service.strategy_factory import strategy


def test_get_strategy_filter():
    config = {"field": "email_contact", "value": "somebody@email.com"}
    filter_strategy = strategy(strategy_name="filter", configuration=config)
    assert isinstance(filter_strategy, FilterPostProcessorStrategy)


def test_get_strategy_unwrap():
    config = {"data_path": "exact_matches.members"}
    unwrap_strategy = strategy(strategy_name="unwrap", configuration=config)
    assert isinstance(unwrap_strategy, UnwrapPostProcessorStrategy)


def test_get_strategy_invalid_config():
    with pytest.raises(ValidationError):
        strategy(strategy_name="unwrap", configuration={"invalid": "thing"})


def test_get_strategy_invalid_strategy():
    with pytest.raises(NoSuchStrategyException):
        strategy("invalid", {})
