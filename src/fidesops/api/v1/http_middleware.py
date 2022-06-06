from datetime import datetime, timezone

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
        is_from_front_end = bool(request.headers.get("request_source") in ['admin-ui', 'privacy-center'])  # fixme: add to front end

        # process the request and get the response
        try:
            response = await call_next(request)
            status_code = response.status_code
        except Exception as e:
            error_class = e.__class__.__name__
            status_code = e.args[0]

        # log response code and/or err type
        analytics_event = AnalyticsEvent(
            docker=in_docker_container(),
            event=EVENT.server_start.value,
            event_created_at=datetime.now(tz=timezone.utc),
            local_host=running_on_local_host(),
            endpoint=request.url.path,
            status_code=status_code,
            extra_data={
                "is_from_front_end": is_from_front_end
            }
        )
        if error_class:
            analytics_event.error = error_class
        send_analytics_event(analytics_event)

        return response