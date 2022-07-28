from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from fideslog.sdk.python.event import AnalyticsEvent

from fidesops.analytics import in_docker_container
from fidesops.graph.config import CollectionAddress
from fidesops.graph.graph_differences import (
    GraphDiffSummary,
    GraphRepr,
    find_graph_differences_summary,
    format_graph_for_caching,
)
from fidesops.models.privacy_request import PrivacyRequest
from fidesops.task.task_resources import TaskResources
from fidesops.util.collection_util import Row


def prepare_rerun_access_graph_analytics_event(
    privacy_request: PrivacyRequest,
    env: Dict[CollectionAddress, Any],
    end_nodes: List[CollectionAddress],
    resources: TaskResources,
) -> Optional[AnalyticsEvent]:
    """Prepares an AnalyticsEvent to send to Fideslog with stats on how an access graph
    has changed from the previous run if applicable
    """
    previous_graph: Optional[GraphRepr] = privacy_request.get_cached_access_graph()
    current_graph: GraphRepr = format_graph_for_caching(env, end_nodes)

    previous_results: Dict[
        str, Optional[List[Row]]
    ] = resources.get_all_cached_objects()

    graph_diff_summary: Optional[GraphDiffSummary] = find_graph_differences_summary(
        previous_graph, current_graph, previous_results
    )

    if not graph_diff_summary:
        return None

    data = graph_diff_summary.dict()
    data["privacy_request"] = privacy_request.id

    return AnalyticsEvent(
        docker=in_docker_container(),
        event="rerun_access_graph",
        event_created_at=datetime.now(tz=timezone.utc),
        local_host=None,
        endpoint=None,
        status_code=None,
        error=None,
        extra_data=data,
    )
