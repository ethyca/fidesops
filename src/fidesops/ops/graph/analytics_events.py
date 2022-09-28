from typing import TYPE_CHECKING, Dict, List, Optional

from fideslog.sdk.python.event import AnalyticsEvent

from fidesops.ops.analytics_event_factory import rerun_graph_analytics_event
from fidesops.ops.graph.config import CollectionAddress
from fidesops.ops.graph.graph_differences import (
    GraphDiffSummary,
    GraphRepr,
    find_graph_differences_summary,
    format_graph_for_caching,
)
from fidesops.ops.models.policy import ActionType
from fidesops.ops.models.privacy_request import PrivacyRequest
from fidesops.ops.task.task_resources import TaskResources
from fidesops.ops.util.collection_util import Row

if TYPE_CHECKING:
    from fidesops.ops.task.graph_task import GraphTask


def prepare_rerun_graph_analytics_event(
    privacy_request: PrivacyRequest,
    env: Dict[CollectionAddress, "GraphTask"],
    end_nodes: List[CollectionAddress],
    resources: TaskResources,
    step: ActionType,
) -> Optional[AnalyticsEvent]:
    """Prepares an AnalyticsEvent to send to Fideslog with stats on how an access graph
    has changed from the previous run if applicable.

    Even for erasure requests, we still compare the "access graphs", because that reflects
    what data has changed and the relationships between them.
    The erasure graph is really just a list that runs each node with data from the access graphs.
    """
    previous_graph: Optional[GraphRepr] = privacy_request.get_cached_access_graph()
    current_graph: GraphRepr = format_graph_for_caching(env, end_nodes)

    previous_access_results: Dict[
        str, Optional[List[Row]]
    ] = resources.get_all_cached_objects()

    previous_erasure_results: Dict[str, int] = {}
    if step == ActionType.erasure:
        # Don't bother looking this up if we are running this just for the access portion
        previous_erasure_results = resources.get_all_cached_erasures()

    graph_diff_summary: Optional[GraphDiffSummary] = find_graph_differences_summary(
        previous_graph, current_graph, previous_access_results, previous_erasure_results
    )

    if not graph_diff_summary:
        return None

    data = graph_diff_summary.dict()
    data["privacy_request"] = privacy_request.id

    return rerun_graph_analytics_event(data=data, step=step)
