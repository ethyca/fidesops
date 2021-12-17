import pytest
from fidesops.graph.graph import *


#  -------------------------------------------
#   graph object tests
#  -------------------------------------------
from fidesops.graph.traversal import Traversal
from . import sql_data_generator
from ..graph.graph_test_util import generate_graph_resources, field, generate_traversal


def test_extract_seed_nodes() -> None:
    # TEST INIT:
    t = generate_graph_resources(3)
    field(t, ("dr_1", "ds_1", "f1")).references.append(
        (FieldAddress("dr_2", "ds_2", "f1"), None)
    )
    field(t, ("dr_1", "ds_1", "f1")).data_type = "integer"
    field(t, ("dr_2", "ds_2", "f1")).data_type = "integer"
    field(t, ("dr_3", "ds_3", "f1")).data_type = "integer"
    field(t, ("dr_1", "ds_1", "f1")).references.append(
        (FieldAddress("dr_3", "ds_3", "f1"), None)
    )
    field(t, ("dr_1", "ds_1", "f1")).identity = "x"
    graph: DatasetGraph = DatasetGraph(*t)

    assert set(graph.nodes.keys()) == {
        CollectionAddress("dr_1", "ds_1"),
        CollectionAddress("dr_2", "ds_2"),
        CollectionAddress("dr_3", "ds_3"),
    }

    assert graph.identity_keys == {FieldAddress("dr_1", "ds_1", "f1"): "x"}

    assert graph.edges == {
        BidirectionalEdge(
            FieldAddress("dr_1", "ds_1", "f1"), FieldAddress("dr_2", "ds_2", "f1")
        ),
        BidirectionalEdge(
            FieldAddress("dr_1", "ds_1", "f1"), FieldAddress("dr_3", "ds_3", "f1")
        ),
    }

    # extract see nodes
    traversal = Traversal(graph, {"x": 1})


    for k, v in sql_data_generator.generate_data_for_traversal(traversal, 10).items():
        for k2,v2 in v.items():
            print(f"{k}--{k2}=={v2}")

