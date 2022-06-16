import asyncio
from datetime import datetime, timezone
from typing import Any
from unittest import mock
from unittest.mock import Mock

import pytest
from fideslog.sdk.python.event import AnalyticsEvent
from starlette.requests import Request
from starlette.responses import Response

from fidesops.analytics import in_docker_container, running_on_local_host
from fidesops.main import dispatch_log_request
from fidesops.schemas.analytics import Event
from fidesops.util.async_util import wait_for


class CustomTestException(BaseException):
    """Mock Non-HTTP Exception"""
    pass


@mock.patch("fidesops.analytics.send_analytics_event")
@mock.patch("datetime.datetime")
def test_dispatch_log_request_no_exception(
        datetime_mock: Mock,
        send_analytics_request_mock: Mock,
) -> None:
    request = Request(
        scope={
            "type": "http",
            "method": 'GET',
            "path": "/testing",
            "server": {
                "host": "www.testsite.com",
                "port": 3000
            },
            "headers": {}
        },
    )

    datetime_mock.now.return_value = datetime(2022, 5, 22, tzinfo=timezone.utc)

    f = asyncio.Future()
    f.set_result(Response(status_code=200))

    def mock_call_next(request: Request) -> Any:
        return f

    wait_for(dispatch_log_request(request, mock_call_next))
    assert send_analytics_request_mock.assert_called_once_with(
        AnalyticsEvent(
            docker=in_docker_container(),
            event=Event.endpoint_call.value,
            event_created_at=datetime_mock.now.return_value,
            local_host=running_on_local_host(),
            endpoint="GET: http://www.testsite.com/testing",
            status_code=200,
        )
    )


@mock.patch("fidesops.analytics.send_analytics_event")
@mock.patch("datetime.datetime")
def test_dispatch_log_request_http_exception(
        datetime_mock: Mock,
        send_analytics_request_mock: Mock,
) -> None:
    request = Request(
        scope={
            "type": "http",
            "method": 'GET',
            "path": "/testing",
            "server": {
                "host": "www.testsite.com",
                "port": 3000
            },
            "headers": {}
        },
    )

    datetime_mock.now.return_value = datetime(2022, 5, 22, tzinfo=timezone.utc)

    f = asyncio.Future()
    f.set_result(Response(status_code=404))

    def mock_call_next(request: Request) -> Any:
        return f

    wait_for(dispatch_log_request(request, mock_call_next))
    assert send_analytics_request_mock.assert_called_once_with(
        AnalyticsEvent(
            docker=in_docker_container(),
            event=Event.endpoint_call.value,
            event_created_at=datetime_mock.now.return_value,
            local_host=running_on_local_host(),
            endpoint="GET: http://www.testsite.com/testing",
            status_code=404,
        )
    )


@mock.patch("fidesops.analytics.send_analytics_event")
@mock.patch("datetime.datetime")
def test_dispatch_log_request_other_exception(
        datetime_mock: Mock,
        send_analytics_request_mock: Mock,
) -> None:
    request = Request(
        scope={
            "type": "http",
            "method": 'GET',
            "path": "/testing",
            "server": {
                "host": "www.testsite.com",
                "port": 3000
            },
            "headers": {}
        },
    )

    datetime_mock.now.return_value = datetime(2022, 5, 22)

    def mock_call_next(request: Request) -> Any:
        raise CustomTestException(BaseException)

    with pytest.raises(CustomTestException):
        wait_for(dispatch_log_request(request, mock_call_next))
        assert send_analytics_request_mock.assert_called_once_with(
            AnalyticsEvent(
                docker=in_docker_container(),
                event=Event.endpoint_call.value,
                event_created_at=datetime_mock.now.return_value,
                local_host=running_on_local_host(),
                endpoint="GET: http://www.testsite.com/testing",
                status_code=500,
                error="CustomTestException"
            )
        )
