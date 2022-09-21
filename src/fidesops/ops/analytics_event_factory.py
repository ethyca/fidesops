from datetime import datetime, timezone
from typing import Any, Dict, Optional

from fideslog.sdk.python.event import AnalyticsEvent

from fidesops.ops.analytics import accessed_through_local_host, in_docker_container
from fidesops.ops.models.policy import ActionType
from fidesops.ops.models.privacy_request import PrivacyRequest
from fidesops.ops.schemas.analytics import Event, ExtraData


def rerun_graph_analytics_event(
    data: Dict[str, Any],
    step: ActionType,
) -> Optional[AnalyticsEvent]:
    """Sends an AnalyticsEvent to send to Fideslog with stats on how an access graph
    has changed from the previous run if applicable"""

    return AnalyticsEvent(
        docker=in_docker_container(),
        event="rerun_access_graph"
        if step == ActionType.access
        else "rerun_erasure_graph",
        event_created_at=datetime.now(tz=timezone.utc),
        local_host=None,
        endpoint=None,
        status_code=None,
        error=None,
        extra_data=data,
    )


def failed_graph_analytics_event(
    privacy_request: PrivacyRequest, exc: Optional[BaseException]
) -> Optional[AnalyticsEvent]:
    """Sends an AnalyticsEvent to send to Fideslog if privacy request execution has failed."""

    data = {"privacy_request": privacy_request.id}

    return AnalyticsEvent(
        docker=in_docker_container(),
        event="privacy_request_execution_failure",
        event_created_at=datetime.now(tz=timezone.utc),
        local_host=None,
        endpoint=None,
        status_code=500,
        error=exc.__class__.__name__ if exc else None,
        extra_data=data,
    )


def server_start_analytics_event() -> Optional[AnalyticsEvent]:
    """Sends an AnalyticsEvent to send to Fideslog upon server start"""

    return AnalyticsEvent(
        docker=in_docker_container(),
        event=Event.server_start.value,
        event_created_at=datetime.now(tz=timezone.utc),
    )


def endpoint_call_analytics_event(
    endpoint: str,
    hostname: Optional[str],
    status_code: int,
    event_created_at: datetime,
    fides_source: Optional[str],
    error_class: Optional[str],
) -> Optional[AnalyticsEvent]:
    """Sends an AnalyticsEvent to send to Fideslog upon endpoint calls"""

    return AnalyticsEvent(
        docker=in_docker_container(),
        event=Event.endpoint_call.value,
        event_created_at=event_created_at,
        local_host=accessed_through_local_host(hostname),
        endpoint=endpoint,
        status_code=status_code,
        error=error_class or None,
        extra_data={ExtraData.fides_source.value: fides_source}
        if fides_source
        else None,
    )
