from abc import abstractmethod

from typing import Any, Dict, List, Optional

from fidesops.common_exceptions import PrivacyRequestPaused
from fidesops.graph.traversal import TraversalNode
from fidesops.models.policy import Policy
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

    def manual_access_results(
        self, privacy_request: PrivacyRequest, node: TraversalNode
    ) -> Optional[List[Row]]:
        """Retrieves any identity data pertaining to this request from the cache"""
        # See if manual key added to cache for node
        prefix = (
            f"MANUAL_INPUT__{privacy_request.id}__access_request__{node.address.value}"
        )
        cache: FidesopsRedis = get_cache()
        value_dict = cache.get_encoded_objects_by_prefix(prefix)
        return value_dict

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
        results = self.manual_access_results(privacy_request, node)
        cache: FidesopsRedis = get_cache()
        prefix = f"PAUSED_LOCATION__{privacy_request.id}__access_request"
        if not results:
            # Save the node that we're paused on
            cache.set_encoded_object(
                prefix,
                node.address.value,
            )
            raise PrivacyRequestPaused(
                f"Node {node.address.value} waiting on manual data for privacy request {privacy_request.id}"
            )
        else:
            cache.set_encoded_object(prefix, None)
            return list(results.values())[0]

    def mask_data(
        self,
        node: TraversalNode,
        policy: Policy,
        privacy_request: PrivacyRequest,
        rows: List[Row],
    ) -> int:
        """Execute a masking request. Return the number of rows that have been updated"""
