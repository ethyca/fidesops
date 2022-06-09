from datetime import datetime, timezone
from typing import Optional

from fastapi import Request
from fideslog.sdk.python.event import AnalyticsEvent
from starlette.middleware.base import BaseHTTPMiddleware

from fidesops.analytics import (
    in_docker_container,
    running_on_local_host,
    send_analytics_event,
)
from fidesops.schemas.analytics import Event, ExtraData


class HttpMiddleware(BaseHTTPMiddleware):
    """
    Middleware for every endpoint
    Currently only used for logging analytics events
    """

    def __init__(
        self,
        app,
    ):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        fides_source: Optional[str] = request.headers.get("X-Fides-Source")

        try:
            response = await call_next(request)
            HttpMiddleware.prepare_and_send_analytics_event(
                request.url.path, response.status_code, fides_source, None
            )
            return response
        except Exception as e:
            HttpMiddleware.prepare_and_send_analytics_event(
                request.url.path, e.args[0], fides_source, e.__class__.__name__
            )
            raise

    @staticmethod
    def prepare_and_send_analytics_event(
        endpoint: str,
        status_code: int,
        fides_source: Optional[str],
        error_class: Optional[str],
    ):
        analytics_event = AnalyticsEvent(
            docker=in_docker_container(),
            event=Event.endpoint_call.value,
            event_created_at=datetime.now(tz=timezone.utc),
            local_host=running_on_local_host(),
            endpoint=endpoint,
            status_code=status_code,
        )
        if error_class:
            analytics_event.error = error_class
        if fides_source:
            analytics_event.extra_data = {ExtraData.fides_source.value: fides_source}
        send_analytics_event(analytics_event)
