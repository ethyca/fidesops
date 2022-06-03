import logging
import os
from platform import system

from fideslog.sdk.python.client import AnalyticsClient
from fideslog.sdk.python.event import AnalyticsEvent
from fideslog.sdk.python.exceptions import AnalyticsError

from fidesops.core.config import config
from fidesops import __version__ as fidesops_version

logger = logging.getLogger(__name__)


def in_docker_container() -> bool:
    """`True` if the command was submitted within a Docker container. Default: `False`."""
    return bool(os.getenv("RUNNING_IN_DOCKER") == "true")


def running_on_local_host() -> bool:
    """For events submitted as a result of making API server requests, `True` if the API server is running on the user's local host. Default: `False`."""
    return False


analytics_client = AnalyticsClient(
    client_id=config.root_user.ANALYTICS_ID,
    developer_mode=config.dev_mode,
    extra_data=None,
    os=system(),
    product_name="fidesops",
    production_version=fidesops_version,
)


def send_analytics_event(event: AnalyticsEvent) -> None:
    if config.root_user.ANALYTICS_OPT_OUT:
        return
    try:
        analytics_client.send(event)
    except AnalyticsError as err:
        logger.warning(f"Error sending analytics event: {err}")
    else:
        logger.info(
            f"Analytics event sent: {event.event} with client id: {analytics_client.client_id}"
        )
