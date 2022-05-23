from abc import abstractmethod

from typing import Any, Dict, List, Optional

from fidesops.common_exceptions import PrivacyRequestPaused
from fidesops.graph.traversal import TraversalNode
from fidesops.models.policy import Policy, ActionType
from fidesops.models.privacy_request import PrivacyRequest
from fidesops.service.connectors.base_connector import BaseConnector, DB_CONNECTOR_TYPE
from fidesops.service.connectors.query_config import QueryConfig
from fidesops.util.cache import FidesopsRedis, get_cache
from fidesops.util.collection_util import Row


class ManualConnector(BaseConnector[None]):
    def query_config(self, node: TraversalNode) -> QueryConfig[Any]:
        return None

    def create_client(self) -> DB_CONNECTOR_TYPE:
        return None

    def close(self) -> None:
        return None

    def test_connection(self) -> None:
        return None

    def retrieve_data(
        self,
        node: TraversalNode,
        policy: Policy,
        privacy_request: PrivacyRequest,
        input_data: Dict[str, List[Any]],
    ) -> List[Row]:
        """
        Returns manual data cached for the given privacy request on the given node
        if it exists, otherwise, pauses the privacy request.
        """
        results = privacy_request.get_manual_input(node.address)
        if results:
            # We just care that results were added - it is okay if they are an empty list.
            privacy_request.cache_paused_location()
            return list(results.values())[0]
        else:
            # Save the node and the request type that we're paused on
            privacy_request.cache_paused_location(ActionType.access, node.address)
            raise PrivacyRequestPaused(
                f"Node {node.address.value} waiting on manual data for privacy request {privacy_request.id}"
            )

    def mask_data(
        self,
        node: TraversalNode,
        policy: Policy,
        privacy_request: PrivacyRequest,
        rows: List[Row],
    ) -> int:
        """Execute a masking request. Return the number of rows that have been updated"""
