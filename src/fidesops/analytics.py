import logging
from platform import system
from typing import Dict

import versioneer
from fideslog.sdk.python.client import AnalyticsClient
from fideslog.sdk.python.event import AnalyticsEvent
from fideslog.sdk.python.exceptions import AnalyticsError

from fidesops.core.config import config, update_config_file
from fidesops.main import app

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


def generate_and_store_client_id() -> bytes:
    update_obj: Dict[str, Dict] = {}
    client_id = bytes(app.title, "utf-8")  # get fideslog bytestring
    update_obj.update(root_user={"ANALYTICS_ID": client_id})
    update_config_file(update_obj)
    return client_id


analytics_client = AnalyticsClient(
    client_id=config.root_user.ANALYTICS_ID or generate_and_store_client_id(),
    developer_mode=in_developer_mode(),
    extra_data=None,
    os=system(),
    product_name=app.title,
    production_version=get_version(),
)


def send_event(event: AnalyticsEvent) -> None:
    if config.root_user.ANALYTICS_OPT_OUT:
        return
    try:
        analytics_client.send(event)
    except AnalyticsError as err:
        logger.warning(f"Error sending analytics event: {err}")
    else:
        print(f"Analytics event sent: {event.event}")
