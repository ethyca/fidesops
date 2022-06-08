from datetime import datetime, timezone
from typing import Optional

from fastapi import Request
from fideslog.sdk.python.event import AnalyticsEvent
from starlette.middleware.base import BaseHTTPMiddleware


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

        # process the request and get the response
        try:
            response = await call_next(request)
            HttpMiddleware.prepare_and_send_analytics_event(response.status_code, fides_source, None)
            return response
        except Exception as e:
            HttpMiddleware.prepare_and_send_analytics_event(e.args[0], fides_source, e.__class__.__name__)
            raise

    @staticmethod
    def prepare_and_send_analytics_event(status_code: int, fides_source: Optional[str], error_class: Optional[str]):
        # log response code and/or err type
        analytics_event = AnalyticsEvent(
            docker=in_docker_container(),
            event=EVENT.server_start.value,  # fixme: add to enum EVENT.endpoint_call or something
            event_created_at=datetime.now(tz=timezone.utc),
            local_host=running_on_local_host(),
            endpoint=request.url.path,
            status_code=status_code,
        )
        if error_class:
            analytics_event.error = error_class
        if fides_source:
            analytics_event.extra_data = {
                "fides_source": fides_source  # fixme: add to enums
            }
        send_analytics_event(analytics_event)
