from typing import Any, Dict, List, Optional, Set

from fidesops.graph.config import (
    ROOT_COLLECTION_ADDRESS,
    TERMINATOR_ADDRESS,
    CollectionAddress,
    FieldAddress,
)
from fidesops.schemas.base_class import BaseSchema
from fidesops.util.collection_util import Row

GraphRepr = Dict[str, Dict[str, List[str]]]


def format_graph_for_caching(
    env: Dict[CollectionAddress, Any], end_nodes: List[CollectionAddress]
) -> GraphRepr:
    """
    Builds a representation of the current graph (that includes its edges) for caching in Redis.

    Requires the results of traversal.traverse():
        - the modified `env`
        - and the outputted end_nodes, which are nodes without children

    Maps collections to their upstream dependencies and associated edges. The root is stored as having
    no upstream collections and the terminator collection has no incoming edges.

    Example:
    {
       <collection>: {
          <upstream collection>: [edge between upstream and current],
          <another upstream collection>: [edge between another upstream and current]
       },
       <root collection>: {},
       <terminator collection>: {
            <end collection>: [],
            <end collection>: []
       }
    }
    """
    graph_repr: GraphRepr = {
        collection.value: {
            upstream_collection_address.value: [str(edge) for edge in edge_list]
            for upstream_collection_address, edge_list in g_task.incoming_edges_by_collection.items()
        }
        for collection, g_task in env.items()
    }
    graph_repr[ROOT_COLLECTION_ADDRESS.value] = {}
    graph_repr[TERMINATOR_ADDRESS.value] = {
        end_node.value: [] for end_node in end_nodes
    }

    return graph_repr


class GraphDiff(BaseSchema):
    previous_collections: List[str] = []
    current_collections: List[str] = []
    added_collections: List[str] = []
    removed_collections: List[str] = []
    added_edges: List[str] = []
    removed_edges: List[str] = []
    processed_collections: List[str] = []
    remaining_collections: List[str] = []
    added_upstream_edges: List[str] = []


class GraphDiffSummary(BaseSchema):
    prev_collection_count: int = 0
    curr_collection_count: int = 0
    added_collection_count: int = 0
    removed_collection_count: int = 0
    added_edge_count: int = 0
    removed_edge_count: int = 0
    processed_collection_count: int = 0
    remaining_collection_count: int = 0
    added_upstream_edge_count: int = 0


artificial_collections: Set[str] = {
    ROOT_COLLECTION_ADDRESS.value,
    TERMINATOR_ADDRESS.value,
}


def _get_upstream_edges(
    processed_collections: List[str], added_edges: List[str]
) -> List[str]:
    """
    Get new edges that have been added upstream of collections that have
    already been processed on previous runs.

    Currently these edges are not re-run.
    """
    collections_queue = processed_collections.copy()

    added_upstream_edges: List[str] = []
    while collections_queue:
        collection_name = collections_queue.pop()
        for edge in added_edges:
            if f"->{collection_name}" in edge:
                added_upstream_edges.append(edge)
                collections_queue.append(
                    FieldAddress.from_string(edge.split("->")[0])
                    .collection_address()
                    .value
                )

    return added_upstream_edges


def _find_graph_differences(  # pylint: disable=too-many-locals
    previous_graph: Optional[GraphRepr],
    current_graph: GraphRepr,
    previous_results: Dict[str, Optional[List[Row]]],
) -> Optional[GraphDiff]:
    """
    Determine how/if a graph has changed from the previous run when a privacy request is rerun.

    Takes in the previous graph, the current graph, and any collections that already ran the first time (previous_results)
    """
    if not previous_graph:
        return None

    def all_edges(graph: GraphRepr) -> Set[str]:
        edge_list: List[str] = []
        for _, dependent_collections in graph.items():
            for _, edges in dependent_collections.items():
                if edges:
                    edge_list.extend(edges)
        return set(edge_list)

    current_collections: Set[str] = (
        set(list(current_graph.keys())) - artificial_collections
    )
    current_edges: Set[str] = all_edges(current_graph)
    previous_collections: Set[str] = (
        set(list(previous_graph.keys())) - artificial_collections
    )
    previous_edges: Set[str] = all_edges(previous_graph)

    added_collections: List[str] = list(current_collections - previous_collections)
    added_edges: List[str] = list(current_edges - previous_edges)
    removed_collections: List[str] = list(previous_collections - current_collections)
    removed_edges: List[str] = list(previous_edges - current_edges)

    processed_collections = list(previous_results.keys())
    added_upstream_edges: List[str] = _get_upstream_edges(
        processed_collections, added_edges
    )

    upstream_collections: List[str] = []
    for edge in added_upstream_edges:
        upstream_collections.append(
            FieldAddress.from_string(edge.split("->")[0]).collection_address().value
        )

    remaining_collections = list(
        current_collections
        - set(upstream_collections)
        - set(processed_collections)
        - artificial_collections
    )

    return GraphDiff(
        previous_collections=list(sorted(previous_collections)),
        current_collections=list(sorted(current_collections)),
        added_collections=sorted(added_collections),
        removed_collections=sorted(removed_collections),
        added_edges=sorted(added_edges),
        removed_edges=sorted(removed_edges),
        processed_collections=sorted(processed_collections),
        remaining_collections=sorted(remaining_collections),
        added_upstream_edges=sorted(added_upstream_edges),
    )


def find_graph_differences_summary(
    previous_graph: Optional[GraphRepr],
    current_graph: GraphRepr,
    previous_results: Dict[str, Optional[List[Row]]],
) -> Optional[GraphDiffSummary]:
    """
    Summarizes the differences between the current graph and previous graph
    with a series of counts.
    """
    graph_diff: Optional[GraphDiff] = _find_graph_differences(
        previous_graph, current_graph, previous_results
    )

    if not graph_diff:
        return None

    return GraphDiffSummary(
        prev_collection_count=len(graph_diff.previous_collections),
        curr_collection_count=len(graph_diff.current_collections),
        added_collection_count=len(graph_diff.added_collections),
        removed_collection_count=len(graph_diff.removed_collections),
        added_edge_count=len(graph_diff.added_edges),
        removed_edge_count=len(graph_diff.removed_edges),
        processed_collection_count=len(graph_diff.processed_collections),
        remaining_collection_count=len(graph_diff.remaining_collections),
        added_upstream_edge_count=len(graph_diff.added_upstream_edges),
    )
