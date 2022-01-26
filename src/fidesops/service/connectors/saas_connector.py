import logging
from typing import Optional

from fidesops.service.connectors.base_connector import BaseConnector
from fidesops.models.connectionconfig import ConnectionTestStatus

logger = logging.getLogger(__name__)


class SaaSConnector(BaseConnector[None]):
    def test_connection(self) -> Optional[ConnectionTestStatus]:
        """
        Override to skip connection test
        """
        return ConnectionTestStatus.skipped
