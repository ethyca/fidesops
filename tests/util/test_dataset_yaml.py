import pytest
import yaml

from fidesops.graph.config import CollectionAddress
from fidesops.models.datasetconfig import convert_dataset_to_graph
from fidesops.schemas.dataset import FidesopsDataset

f = """dataset:
  - fides_key: xyz
    fidesops_meta:
        after: [db1, db2, db3]        
    name: xyz
    description: x
    collections:
      - name: address
        fidesops_meta:
            after: [a.b, c.d, e.f]
        fields:
          - name: city
            data_categories: [user.provided.identifiable.contact.city] 
          - name: id
            data_categories: [system.operations]
            fidesops_meta:
              primary_key: True  
"""


f2 = """dataset:
  - fides_key: mongo_nested_test
    name: Mongo Example Nested Test Dataset
    description: Example of a Mongo dataset that contains nested data
    collections:
      - name: photos
        data_type: json   # nested types
        fields:
          - name: _id
            data_type: object_id
            data_categories: [system.operations]
            fidesops_meta:
              primary_key: True
          - name: photo_id
            data_type: integer
            data_categories: [user.derived.identifiable.unique_id]
            fidesops_meta:
              references:
                - dataset: postgres_example_test_dataset
                  field: customer.id
                  direction: from
          - name: name
            data_categories: [user.provided.identifiable]
            data_type: string
          - name: submitter
            data_type: string
            data_categories: [user.provided.identifiable]
          - name: thumbnail
            fields:
              - name: photo_id
                data_type: integer
              - name: name
                data_categories: [user.provided.identifiable]
                data_type: string
              - name: submitter
                data_type: string
                data_categories: [user.provided.identifiable]
          - name: tags
            data_type: string[]
            data_categories: [user.provided]
          - name: comments
            data_type: json[] # array type
            fields:
              - name: comment_id
              - name: text
              - name: submitter
              ""
"""


def test_dataset_yaml_format():
    """Test that 'after' parameters are properly read"""
    d = yaml.safe_load(f)
    dataset = d.get("dataset")[0]
    d: FidesopsDataset = FidesopsDataset.parse_obj(dataset)
    config = convert_dataset_to_graph(d, "ignore")
    assert config.after == {"db1", "db2", "db3"}
    assert config.collections[0].after == {
        CollectionAddress("a", "b"),
        CollectionAddress("c", "d"),
        CollectionAddress("e", "f"),
    }


def test_dataset_yaml_format_invalid_format():
    """Test that 'after' parameters are properly read"""
    d = yaml.safe_load(f)
    dataset = d.get("dataset")[0]
    dataset.get("collections")[0].get("fidesops_meta").get("after")[0] = "invalid"
    with pytest.raises(ValueError) as exc:
        d: FidesopsDataset = FidesopsDataset.parse_obj(dataset)
        convert_dataset_to_graph(d, "ignore")
    assert "FidesCollection must be specified in the form 'FidesKey.FidesKey'" in str(
        exc.value
    )


def test_dataset_yaml_format_invalid_fides_keys():
    """Test that 'after' parameters are properly read"""
    d = yaml.safe_load(f)
    dataset = d.get("dataset")[0]
    dataset.get("collections")[0].get("fidesops_meta").get("after")[
        0
    ] = "invalid-dataset-name.invalid-collection-name"
    with pytest.raises(ValueError) as exc:
        d: FidesopsDataset = FidesopsDataset.parse_obj(dataset)
        convert_dataset_to_graph(d, "ignore")
    assert "FidesKey must only contain alphanumeric characters, '.' or '_'." in str(
        exc.value
    )


def test_nested_dataset_format():
    d = yaml.safe_load(f2)
    dataset = d.get("dataset")[0]
    print(dataset)
    d2 = FidesopsDataset.parse_obj(dataset)
    print(d2)
