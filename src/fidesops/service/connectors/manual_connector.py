from typing import Any, Dict, List, Optional

from fidesops.common_exceptions import PrivacyRequestPaused
from fidesops.graph.traversal import TraversalNode
from fidesops.models.policy import ActionType, Policy
from fidesops.models.privacy_request import PrivacyRequest
from fidesops.service.connectors.base_connector import DB_CONNECTOR_TYPE, BaseConnector
from fidesops.service.connectors.query_config import QueryConfig
from fidesops.util.collection_util import Row


class ManualConnector(BaseConnector[None]):
    def query_config(self, node: TraversalNode) -> QueryConfig[Any]:
        """No query_config for the Manual Connector"""
        return None

    def create_client(self) -> DB_CONNECTOR_TYPE:
        """Not needed because this connector involves a human performing some lookup step"""
        return None

    def close(self) -> None:
        """No session to close for the Manual Connector"""
        return None

    def test_connection(self) -> None:
        """No automated test_connection available for the Manual Connector"""
        return None

    def retrieve_data(
        self,
        node: TraversalNode,
        policy: Policy,
        privacy_request: PrivacyRequest,
        input_data: Dict[str, List[Any]],
    ) -> Optional[List[Row]]:
        """
        Returns manual data cached for the given privacy request on the given node
        if it exists, otherwise, pauses the privacy request.
        """
        results: Dict[
            Optional[str], Optional[List[Row]]
        ] = privacy_request.get_manual_input(node.address)
        if results:
            privacy_request.cache_paused_location()  # Caches paused location as None
            return list(results.values())[0]
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
        """Pause to have the user manually perform an erasure of data at the given node."""
        # TODO implement in follow-up ticket
