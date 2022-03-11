from requests import Response
from fidesops.schemas.saas.shared_schemas import SaaSRequestParams
from fidesops.schemas.saas.strategy_configuration import CursorPaginationConfiguration
from fidesops.service.pagination.pagination_strategy_cursor import (
    CursorPaginationStrategy,
)


def test_cursor():
    config = CursorPaginationConfiguration(cursor_param="after", value_field="next_page")
    request_params: SaaSRequestParams = "GET", "/conversations", {}, None

    paginator = CursorPaginationStrategy(config)
    next_request: SaaSRequestParams = paginator.get_next_request(
        request_params, {}, Response(), {"next_page": 456}
    )
    assert next_request == ("GET", "/conversations", {"after": 456}, None)

def test_missing_cursor():
    config = CursorPaginationConfiguration(cursor_param="after", value_field="next_page")
    request_params: SaaSRequestParams = "GET", "/conversations", {}, None

    paginator = CursorPaginationStrategy(config)
    next_request: SaaSRequestParams = paginator.get_next_request(
        request_params, {}, Response(), {"other_info": "abc"}
    )
    assert next_request is None

def test_cursor_with_no_row():
    config = CursorPaginationConfiguration(cursor_param="after", value_field="next_page")
    request_params: SaaSRequestParams = "GET", "/conversations", {}, None

    paginator = CursorPaginationStrategy(config)
    next_request: SaaSRequestParams = paginator.get_next_request(
        request_params, {}, Response()
    )
    assert next_request is None