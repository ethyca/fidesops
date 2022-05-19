import logging
from datetime import datetime, timezone
from platform import system

import versioneer
from fideslog.sdk.python.client import AnalyticsClient
from fideslog.sdk.python.event import AnalyticsEvent
from fideslog.sdk.python.exceptions import AnalyticsError
from fideslog.sdk.python.utils import generate_client_id

from fidesops.core.config import config
from fidesops.main import app
from fidesops.schemas.analytics import FideslogAnalyticsEvent

logger = logging.getLogger(__name__)


def get_version() -> str:
    """Version of Fidesops"""
    return versioneer.get_version()


def in_developer_mode() -> bool:
    """True if runnning in dev mode"""
    return config.dev_mode


def in_docker_container() -> bool:
    """`True` if the command was submitted within a Docker container. Default: `False`."""
    return True


def running_on_local_host() -> bool:
    """For events submitted as a result of making API server requests, `True` if the API server is running on the user's local host. Default: `False`."""
    return False


class Analytics:
    def __init__(self):
        if not config.user.ANALYTICS_OPT_OUT:
            client_id: str = generate_client_id(bytes(app.title, "utf-8"))
            self.client = AnalyticsClient(
                client_id=client_id,
                developer_mode=in_developer_mode(),
                extra_data={
                    "this data": "will be included with every event sent by this client",
                    "include": "any context that every event requires",
                    "never include": "identifying information of any kind",
                },
                os=system(),
                product_name=app.title,
                production_version=get_version(),
            )

    def send_event(self, event_data: FideslogAnalyticsEvent):
        if not config.user.ANALYTICS_OPT_OUT:
            try:
                cli_command_event = AnalyticsEvent(
                    command=event_data.command,
                    docker=in_docker_container(),
                    event=event_data.event,
                    error=event_data.error,
                    event_created_at=datetime.now(tz=timezone.utc),
                    extra_data=event_data.extra_data,
                    flags=event_data.flags,
                    local_host=running_on_local_host(),
                    resource_counts=event_data.resource_counts,
                    status_code=event_data.status_code,
                )
                self.client.send(cli_command_event)
            except AnalyticsError as err:
                logger.warning(f"Error sending analytics event: {err}")
            else:
                print(f"Analytics event sent: {event_data.event}")
