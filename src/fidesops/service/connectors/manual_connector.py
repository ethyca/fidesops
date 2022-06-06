import logging
from typing import Any, Dict, List, Optional

from sqlalchemy.sql.elements import TextClause

from fidesops.common_exceptions import PrivacyRequestPaused
from fidesops.graph.traversal import TraversalNode
from fidesops.models.policy import PausedStep, Policy
from fidesops.models.privacy_request import ManualAction, PrivacyRequest
from fidesops.service.connectors.base_connector import BaseConnector
from fidesops.service.connectors.query_config import ManualQueryConfig
from fidesops.util.collection_util import Row

logger = logging.getLogger(__name__)


class ManualConnector(BaseConnector[None]):
    def query_config(self, node: TraversalNode) -> ManualQueryConfig:
        """
        The ManualQueryConfig generates instructions for the user to retrieve and mask
        data manually.
        """
        return ManualQueryConfig(node)

    def create_client(self) -> None:
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
        Returns manually added data for the given collection if it exists, otherwise pauses the Privacy Request.

        On the event that we pause, caches the stopped step, stopped collection, and details needed to manually resume
        the privacy request.
        """
        cached_results: Optional[List[Row]] = privacy_request.get_manual_input(
            node.address
        )

        if cached_results is not None:  # None comparison intentional
            privacy_request.cache_paused_collection_details()  # Resets paused details to None
            return cached_results

        query_config = self.query_config(node)
        action_needed: Optional[ManualAction] = query_config.generate_query(
            input_data, policy
        )
        privacy_request.cache_paused_collection_details(
            step=PausedStep.access,
            collection=node.address,
            action_needed=[action_needed] if action_needed else None,
        )

        raise PrivacyRequestPaused(
            f"Collection '{node.address.value}' waiting on manual data for privacy request '{privacy_request.id}'"
        )

    def mask_data(
        self,
        node: TraversalNode,
        policy: Policy,
        privacy_request: PrivacyRequest,
        rows: List[Row],
    ) -> Optional[int]:
        """If erasure confirmation has been added to the manual cache, continue, otherwise,
        pause and wait for manual input.

        On the event that we pause, caches the stopped step, stopped collection, and details needed to manually resume
        the privacy request.
        """
        manual_cached_count: Optional[int] = privacy_request.get_manual_erasure_count(
            node.address
        )

        if manual_cached_count is not None:  # None comparison intentional
            privacy_request.cache_paused_collection_details()  # Resets paused details to None
            return manual_cached_count

        query_config: ManualQueryConfig = self.query_config(node)
        action_needed: List[ManualAction] = []
        for row in rows:
            action: Optional[ManualAction] = query_config.generate_update_stmt(
                row, policy, privacy_request
            )
            if action:
                action_needed.append(action)

        privacy_request.cache_paused_collection_details(
            step=PausedStep.erasure,
            collection=node.address,
            action_needed=action_needed if action_needed else None,
        )

        raise PrivacyRequestPaused(
            f"Collection '{node.address.value}' waiting on manual erasure confirmation for privacy request '{privacy_request.id}'"
        )


def format_cached_query(stmt: Optional[TextClause]) -> Optional[Dict[str, Any]]:
    """
    Format the SQLAlchemy TextClause for caching in Redis, for describing to the user the manual actions required on their
    part. Store the query and the parameters separately.

    For example:
    {
        'query': 'UPDATE filing_cabinet SET authorized_user = :authorized_user WHERE id = :id',
        'parameters': {
            'authorized_user': None,
            'id': 121
        }
    }
    """
    if stmt is None:
        return None

    query_elems: Dict[str, Any] = {"query": str(stmt), "parameters": {}}
    for (
        param_name,
        bind_parameters,
    ) in stmt._bindparams.items():  # pylint: disable=W0212
        query_elems["parameters"][param_name] = bind_parameters.value
    return query_elems
