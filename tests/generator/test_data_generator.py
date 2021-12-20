import pytest
import yaml

from fidesops.graph.graph import *


#  -------------------------------------------
#   graph object tests
#  -------------------------------------------
from fidesops.graph.traversal import Traversal
from fidesops.models.datasetconfig import convert_dataset_to_graph
from fidesops.schemas.dataset import FidesopsDataset
from . import sql_data_generator
from ..graph.graph_test_util import generate_graph_resources, field, generate_traversal


f = """dataset:
  - fides_key: db
    name: name
    description: description
    collections:
      - name: user
        fields:
          - name: id
            fidesops_meta:
              primary_key: True
              data_type: integer
              references:
                - dataset: db
                  field: address.user_id
          - name: email
            fidesops_meta:
              identity: email
          - name: name

      - name: address
        fields:
          - name: id
            fidesops_meta:
              primary_key: True
              data_type: integer
          - name: user_id
          - name: street
          - name: city
          - name: state
          - name: zip
"""


def parse_yaml() -> Dataset:
    """Test that 'after' parameters are properly read"""
    d = yaml.safe_load(f)
    dataset = d.get("dataset")[0]
    d: FidesopsDataset = FidesopsDataset.parse_obj(dataset)
    return convert_dataset_to_graph(d, "ignore")


def test_parse():
    print (parse_yaml())
    assert False

def test_generate():
    dataset = parse_yaml()
    traversal = Traversal(DatasetGraph(dataset), {"email": "example@example.com"})
    for k, v in sql_data_generator.generate_data_for_traversal(traversal, 10).items():
        for k2,v2 in v.items():
            print(f"{k}--{k2}=={v2}")

#
#
# def test_extract_seed_nodes() -> None:
#     # TEST INIT:
#     t = generate_graph_resources(3)
#     field(t, ("dr_1", "ds_1", "f1")).references.append(
#         (FieldAddress("dr_2", "ds_2", "f1"), None)
#     )
#     field(t, ("dr_1", "ds_1", "f1")).data_type = "integer"
#     field(t, ("dr_2", "ds_2", "f1")).data_type = "integer"
#     field(t, ("dr_3", "ds_3", "f1")).data_type = "integer"
#     field(t, ("dr_1", "ds_1", "f1")).references.append(
#         (FieldAddress("dr_3", "ds_3", "f1"), None)
#     )
#     field(t, ("dr_1", "ds_1", "f1")).identity = "x"
#     graph: DatasetGraph = DatasetGraph(*t)
#
#     assert set(graph.nodes.keys()) == {
#         CollectionAddress("dr_1", "ds_1"),
#         CollectionAddress("dr_2", "ds_2"),
#         CollectionAddress("dr_3", "ds_3"),
#     }
#
#     assert graph.identity_keys == {FieldAddress("dr_1", "ds_1", "f1"): "x"}
#
#     assert graph.edges == {
#         BidirectionalEdge(
#             FieldAddress("dr_1", "ds_1", "f1"), FieldAddress("dr_2", "ds_2", "f1")
#         ),
#         BidirectionalEdge(
#             FieldAddress("dr_1", "ds_1", "f1"), FieldAddress("dr_3", "ds_3", "f1")
#         ),
#     }
#
#     # extract see nodes
#     traversal = Traversal(graph, {"x": 1})
#
#
#     for k, v in sql_data_generator.generate_data_for_traversal(traversal, 10).items():
#         for k2,v2 in v.items():
#             print(f"{k}--{k2}=={v2}")
#
