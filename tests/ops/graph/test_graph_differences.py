from typing import Any, Dict

import pytest

from fidesops.graph.config import (
    ROOT_COLLECTION_ADDRESS,
    CollectionAddress,
    FieldAddress,
)
from fidesops.graph.graph import Edge
from fidesops.graph.graph_differences import (
    GraphDiff,
    GraphDiffSummary,
    _find_graph_differences,
    find_graph_differences_summary,
    format_graph_for_caching,
)
from fidesops.graph.traversal import TraversalNode, artificial_traversal_node
from fidesops.models.connectionconfig import ConnectionConfig, ConnectionType
from fidesops.models.policy import Policy
from fidesops.task.graph_task import EMPTY_REQUEST, GraphTask
from fidesops.task.task_resources import TaskResources

from ..graph.graph_test_util import generate_node


def build_test_traversal_env(*traversal_nodes, resources):
    """For testing purposes, mock building an env which is modified in place
    as part of calling traversal.traverse

    We can build a graph from the "env" variable.
    """

    env: Dict[CollectionAddress, Any] = {}

    for tn in traversal_nodes:
        env[tn.address] = GraphTask(traversal_node=tn, resources=resources)
    return env


def a_traversal_node():
    return TraversalNode(
        generate_node("test_db", "a_collection", "id", "A_info", "email")
    )


def b_traversal_node():
    return TraversalNode(
        generate_node("test_db", "b_collection", "id", "B_info", "upstream_id")
    )


def c_traversal_node():
    return TraversalNode(
        generate_node("test_db", "c_collection", "upstream_id", "C_info")
    )


@pytest.fixture(scope="module")
def resources():
    return TaskResources(
        EMPTY_REQUEST,
        Policy(),
        [
            ConnectionConfig(
                key="mock_connection_config_key_test_db",
                connection_type=ConnectionType.postgres,
            )
        ],
    )


@pytest.fixture(scope="module")
def env_a_b(resources):
    """Mocks env result that is mutated as of traversal.traverse()
    This mimics a simple graph where ROOT->A->B->TERMINATOR
    """
    a_tn = a_traversal_node()
    b_tn = b_traversal_node()

    root_node = artificial_traversal_node(ROOT_COLLECTION_ADDRESS)
    root_node.add_child(
        a_tn,
        Edge(
            FieldAddress(
                ROOT_COLLECTION_ADDRESS.dataset,
                ROOT_COLLECTION_ADDRESS.collection,
                "email",
            ),
            FieldAddress("test_db", "a_collection", "email"),
        ),
    )
    a_tn.add_child(
        b_tn,
        Edge(
            FieldAddress("test_db", "a_collection", "id"),
            FieldAddress("test_db", "b_collection", "upstream_id"),
        ),
    )
    b_tn.is_terminal_node = True

    return build_test_traversal_env(a_tn, b_tn, resources=resources)


@pytest.fixture(scope="module")
def env_c_a_b(resources):
    """Mocks env result that is mutated as of traversal.traverse()
    This mimics a simple graph where ROOT->C->A->B->TERMINATOR
    """
    c_tn = c_traversal_node()
    a_tn = a_traversal_node()
    b_tn = b_traversal_node()

    root_node = artificial_traversal_node(ROOT_COLLECTION_ADDRESS)
    root_node.add_child(
        c_tn,
        Edge(
            FieldAddress(
                ROOT_COLLECTION_ADDRESS.dataset,
                ROOT_COLLECTION_ADDRESS.collection,
                "email",
            ),
            FieldAddress("test_db", "c_collection", "email"),
        ),
    )
    c_tn.add_child(
        a_tn,
        Edge(
            FieldAddress("test_db", "c_collection", "id"),
            FieldAddress("test_db", "a_collection", "upstream_id"),
        ),
    )
    a_tn.add_child(
        b_tn,
        Edge(
            FieldAddress("test_db", "a_collection", "id"),
            FieldAddress("test_db", "b_collection", "upstream_id"),
        ),
    )

    return build_test_traversal_env(c_tn, a_tn, b_tn, resources=resources)


@pytest.fixture(scope="module")
def env_a_b_c(resources):
    """Mocks env result that is mutated as of traversal.traverse()
    This mimics a simple graph where ROOT->A->B->C->TERMINATOR
    """
    c_tn = c_traversal_node()
    a_tn = a_traversal_node()
    b_tn = b_traversal_node()

    root_node = artificial_traversal_node(ROOT_COLLECTION_ADDRESS)
    root_node.add_child(
        a_tn,
        Edge(
            FieldAddress(
                ROOT_COLLECTION_ADDRESS.dataset,
                ROOT_COLLECTION_ADDRESS.collection,
                "email",
            ),
            FieldAddress("test_db", "a_collection", "email"),
        ),
    )
    a_tn.add_child(
        b_tn,
        Edge(
            FieldAddress("test_db", "a_collection", "id"),
            FieldAddress("test_db", "b_collection", "upstream_id"),
        ),
    )
    b_tn.add_child(
        c_tn,
        Edge(
            FieldAddress("test_db", "b_collection", "id"),
            FieldAddress("test_db", "c_collection", "upstream_id"),
        ),
    )
    c_tn.is_terminal_node = True

    return build_test_traversal_env(a_tn, b_tn, c_tn, resources=resources)


@pytest.fixture(scope="function")
def env_a_c_b(resources):
    """Mocks env result that is mutated as of traversal.traverse()
    This mimics a simple graph where ROOT->A->C->B->TERMINATOR
    """
    c_tn = c_traversal_node()
    a_tn = a_traversal_node()
    b_tn = b_traversal_node()

    root_node = artificial_traversal_node(ROOT_COLLECTION_ADDRESS)
    root_node.add_child(
        a_tn,
        Edge(
            FieldAddress(
                ROOT_COLLECTION_ADDRESS.dataset,
                ROOT_COLLECTION_ADDRESS.collection,
                "email",
            ),
            FieldAddress("test_db", "a_collection", "email"),
        ),
    )
    a_tn.add_child(
        c_tn,
        Edge(
            FieldAddress("test_db", "a_collection", "id"),
            FieldAddress("test_db", "c_collection", "upstream_id"),
        ),
    )
    c_tn.add_child(
        b_tn,
        Edge(
            FieldAddress("test_db", "c_collection", "id"),
            FieldAddress("test_db", "b_collection", "upstream_id"),
        ),
    )
    b_tn.is_terminal_node = True

    return build_test_traversal_env(a_tn, c_tn, b_tn, resources=resources)


class TestFormatGraphForCaching:
    def test_format_graph_for_caching(self, env_a_b_c, env_a_c_b):
        """Test two graphs:

        Root -> Graph A -> B -> C -> Terminator

        Root -> Graph A -> C -> B -> Terminator

        """

        end_nodes = [c_traversal_node().address]

        assert format_graph_for_caching(env_a_b_c, end_nodes) == {
            "test_db:a_collection": {
                "__ROOT__:__ROOT__": [
                    "__ROOT__:__ROOT__:email->test_db:a_collection:email"
                ]
            },
            "test_db:b_collection": {
                "test_db:a_collection": [
                    "test_db:a_collection:id->test_db:b_collection:upstream_id"
                ]
            },
            "test_db:c_collection": {
                "test_db:b_collection": [
                    "test_db:b_collection:id->test_db:c_collection:upstream_id"
                ]
            },
            "__ROOT__:__ROOT__": {},
            "__TERMINATE__:__TERMINATE__": {"test_db:c_collection": []},
        }

        # Now swap positions of b and c collection
        end_nodes = [b_traversal_node().address]
        assert format_graph_for_caching(env_a_c_b, end_nodes) == {
            "test_db:a_collection": {
                "__ROOT__:__ROOT__": [
                    "__ROOT__:__ROOT__:email->test_db:a_collection:email"
                ]
            },
            "test_db:c_collection": {
                "test_db:a_collection": [
                    "test_db:a_collection:id->test_db:c_collection:upstream_id"
                ]
            },
            "test_db:b_collection": {
                "test_db:c_collection": [
                    "test_db:c_collection:id->test_db:b_collection:upstream_id"
                ]
            },
            "__ROOT__:__ROOT__": {},
            "__TERMINATE__:__TERMINATE__": {"test_db:b_collection": []},
        }


class TestGraphDiff:
    def test_find_graph_differences_no_previous(self, env_a_b_c):
        """Test no previous graph to compare"""
        previous_graph = {}
        formatted_current_graph = format_graph_for_caching(
            env_a_b_c, [c_traversal_node().address]
        )
        assert not _find_graph_differences(
            previous_graph=previous_graph,
            current_graph=formatted_current_graph,
            previous_results={},
        )

    def test_find_graph_differences_no_change(self, env_a_b_c):
        formatted_graph = format_graph_for_caching(
            env_a_b_c, [c_traversal_node().address]
        )
        graph_diff = _find_graph_differences(
            previous_graph=formatted_graph,
            current_graph=formatted_graph,
            previous_results={},
        )
        assert graph_diff == GraphDiff(
            previous_collections=[
                "test_db:a_collection",
                "test_db:b_collection",
                "test_db:c_collection",
            ],
            current_collections=[
                "test_db:a_collection",
                "test_db:b_collection",
                "test_db:c_collection",
            ],
            added_collections=[],
            removed_collections=[],
            added_edges=[],
            removed_edges=[],
            processed_collections=[],
            remaining_collections=[
                "test_db:a_collection",
                "test_db:b_collection",
                "test_db:c_collection",
            ],
            added_upstream_edges=[],
        )
        assert find_graph_differences_summary(
            formatted_graph, formatted_graph, {}
        ) == GraphDiffSummary(
            prev_collection_count=3,
            curr_collection_count=3,
            added_collection_count=0,
            removed_collection_count=0,
            added_edge_count=0,
            removed_edge_count=0,
            processed_collection_count=0,
            remaining_collection_count=3,
            added_upstream_edge_count=0,
        )

    def test_find_graph_differences_collection_added(self, env_a_b, env_a_b_c):
        previous_graph = format_graph_for_caching(
            env_a_b, end_nodes=[b_traversal_node().address]
        )
        current_graph = format_graph_for_caching(
            env_a_b_c, end_nodes=[c_traversal_node().address]
        )
        graph_diff = _find_graph_differences(previous_graph, current_graph, {})
        assert graph_diff == GraphDiff(
            previous_collections=["test_db:a_collection", "test_db:b_collection"],
            current_collections=[
                "test_db:a_collection",
                "test_db:b_collection",
                "test_db:c_collection",
            ],
            added_collections=["test_db:c_collection"],
            removed_collections=[],
            added_edges=["test_db:b_collection:id->test_db:c_collection:upstream_id"],
            removed_edges=[],
            processed_collections=[],
            remaining_collections=[
                "test_db:a_collection",
                "test_db:b_collection",
                "test_db:c_collection",
            ],
            added_upstream_edges=[],
        )
        assert find_graph_differences_summary(
            previous_graph, current_graph, {}
        ) == GraphDiffSummary(
            prev_collection_count=2,
            curr_collection_count=3,
            added_collection_count=1,
            removed_collection_count=0,
            added_edge_count=1,
            removed_edge_count=0,
            processed_collection_count=0,
            remaining_collection_count=3,
            added_upstream_edge_count=0,
        )

    def test_find_graph_differences_collection_removed(self, env_a_b_c, env_a_b):
        previous_graph = format_graph_for_caching(
            env_a_b_c, end_nodes=[c_traversal_node().address]
        )
        current_graph = format_graph_for_caching(
            env_a_b, end_nodes=[b_traversal_node().address]
        )
        graph_diff = _find_graph_differences(previous_graph, current_graph, {})
        assert graph_diff == GraphDiff(
            previous_collections=[
                "test_db:a_collection",
                "test_db:b_collection",
                "test_db:c_collection",
            ],
            current_collections=["test_db:a_collection", "test_db:b_collection"],
            added_collections=[],
            removed_collections=["test_db:c_collection"],
            added_edges=[],
            removed_edges=["test_db:b_collection:id->test_db:c_collection:upstream_id"],
            processed_collections=[],
            remaining_collections=["test_db:a_collection", "test_db:b_collection"],
            added_upstream_edges=[],
        )
        assert find_graph_differences_summary(
            previous_graph, current_graph, {}
        ) == GraphDiffSummary(
            prev_collection_count=3,
            curr_collection_count=2,
            added_collection_count=0,
            removed_collection_count=1,
            added_edge_count=0,
            removed_edge_count=1,
            processed_collection_count=0,
            remaining_collection_count=2,
            added_upstream_edge_count=0,
        )

    def test_find_graph_differences_collection_order_changed(
        self, env_a_b_c, env_a_c_b
    ):
        previous_graph = format_graph_for_caching(
            env_a_b_c, end_nodes=[c_traversal_node().address]
        )
        current_graph = format_graph_for_caching(
            env_a_c_b, end_nodes=[b_traversal_node().address]
        )
        previous_results = {"test_db:a_collection": []}
        graph_diff = _find_graph_differences(
            previous_graph, current_graph, previous_results
        )

        assert graph_diff == GraphDiff(
            previous_collections=[
                "test_db:a_collection",
                "test_db:b_collection",
                "test_db:c_collection",
            ],
            current_collections=[
                "test_db:a_collection",
                "test_db:b_collection",
                "test_db:c_collection",
            ],
            added_collections=[],
            removed_collections=[],
            added_edges=[
                "test_db:a_collection:id->test_db:c_collection:upstream_id",
                "test_db:c_collection:id->test_db:b_collection:upstream_id",
            ],
            removed_edges=[
                "test_db:a_collection:id->test_db:b_collection:upstream_id",
                "test_db:b_collection:id->test_db:c_collection:upstream_id",
            ],
            processed_collections=["test_db:a_collection"],
            remaining_collections=["test_db:b_collection", "test_db:c_collection"],
            added_upstream_edges=[],
        )
        assert find_graph_differences_summary(
            previous_graph, current_graph, previous_results
        ) == GraphDiffSummary(
            prev_collection_count=3,
            curr_collection_count=3,
            added_collection_count=0,
            removed_collection_count=0,
            added_edge_count=2,
            removed_edge_count=2,
            processed_collection_count=1,
            remaining_collection_count=2,
            added_upstream_edge_count=0,
        )

    def test_find_graph_differences_collection_added_upstream(self, env_a_b, env_c_a_b):
        previous_graph = format_graph_for_caching(
            env_a_b, end_nodes=[b_traversal_node().address]
        )
        current_graph = format_graph_for_caching(
            env_c_a_b, end_nodes=[b_traversal_node().address]
        )

        previous_results = {"test_db:a_collection": []}

        graph_diff = _find_graph_differences(
            previous_graph, current_graph, previous_results
        )

        assert graph_diff == GraphDiff(
            previous_collections=["test_db:a_collection", "test_db:b_collection"],
            current_collections=[
                "test_db:a_collection",
                "test_db:b_collection",
                "test_db:c_collection",
            ],
            added_collections=["test_db:c_collection"],
            removed_collections=[],
            added_edges=[
                "__ROOT__:__ROOT__:email->test_db:c_collection:email",
                "test_db:c_collection:id->test_db:a_collection:upstream_id",
            ],
            removed_edges=["__ROOT__:__ROOT__:email->test_db:a_collection:email"],
            processed_collections=["test_db:a_collection"],
            remaining_collections=["test_db:b_collection"],
            added_upstream_edges=[
                "__ROOT__:__ROOT__:email->test_db:c_collection:email",
                "test_db:c_collection:id->test_db:a_collection:upstream_id",
            ],
        )
        assert find_graph_differences_summary(
            previous_graph, current_graph, previous_results
        ) == GraphDiffSummary(
            prev_collection_count=2,
            curr_collection_count=3,
            added_collection_count=1,
            removed_collection_count=0,
            added_edge_count=2,
            removed_edge_count=1,
            processed_collection_count=1,
            remaining_collection_count=1,
            added_upstream_edge_count=2,
        )
