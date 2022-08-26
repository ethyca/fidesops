import pytest

from fidesops.ops.common_exceptions import NoSuchStrategyException, ValidationError
from fidesops.ops.service.pagination.pagination_strategy_cursor import (
    CursorPaginationStrategy,
)
from fidesops.ops.service.pagination.pagination_strategy_link import (
    LinkPaginationStrategy,
)
from fidesops.ops.service.pagination.pagination_strategy_offset import (
    OffsetPaginationStrategy,
)
from fidesops.ops.service.strategy_factory import strategy


def test_strategy_offset():
    config = {
        "incremental_param": "page",
        "increment_by": 1,
        "limit": 100,
    }
    offset_strategy = strategy(strategy_name="offset", configuration=config)
    assert isinstance(offset_strategy, OffsetPaginationStrategy)


def test_strategy_link():
    config = {"source": "body", "path": "body.next_link"}
    link_strategy = strategy(strategy_name="link", configuration=config)
    assert isinstance(link_strategy, LinkPaginationStrategy)


def test_strategy_cursor():
    config = {"cursor_param": "after", "field": "id"}
    cursor_strategy = strategy(strategy_name="cursor", configuration=config)
    assert isinstance(cursor_strategy, CursorPaginationStrategy)


def test_strategy_invalid_config():
    with pytest.raises(ValidationError):
        strategy(strategy_name="offset", configuration={"invalid": "thing"})


def test_strategy_invalid_strategy():
    with pytest.raises(NoSuchStrategyException):
        strategy("invalid", {})
