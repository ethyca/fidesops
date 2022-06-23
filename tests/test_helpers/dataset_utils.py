import re
from typing import Any, Dict, Iterable, List, Optional

import yaml

from fidesops.graph.config import (
    Collection,
    Dataset,
    Field,
    FieldPath,
    ObjectField,
    ScalarField,
)
from fidesops.models.connectionconfig import ConnectionConfig
from fidesops.models.datasetconfig import DatasetConfig, convert_dataset_to_graph
from fidesops.schemas.dataset import FidesopsDataset
from fidesops.util.collection_util import Row

SAAS_DATASET_DIRECTORY = "data/saas/dataset/"


def populate_dataset(
    connection_config: ConnectionConfig,
    dataset_config: DatasetConfig,
    response: Dict[str, List[Row]],
    file_name: str,
):
    """
    Populates the given dataset with missing collections and
    fields from the map of API responses. Preserves any
    existing/user-overwritten data categories.
    """

    # convert to Dataset to be able to use the Collection helpers
    dataset = FidesopsDataset(**dataset_config.dataset)
    graph = convert_dataset_to_graph(dataset, dataset.fides_key)
    field_map = {collection.name: collection for collection in graph.collections}

    # use endpoint order in the SaaS config as the collection order in the dataset
    generated_collections = generate_collections(dataset.fides_key, response, field_map)
    collection_order = [
        endpoint["name"] for endpoint in connection_config.saas_config["endpoints"]
    ]
    generated_collections.sort(
        key=lambda collection: collection_order.index(collection["name"])
    )

    generated_dataset = {
        "fides_key": dataset.fides_key,
        "name": dataset.name,
        "description": dataset.description,
        "collections": generated_collections,
    }

    # the yaml library doesn't allow us to just reformat
    # the data_categories field so we fix it with a regex
    #
    # data_categories:
    #   - system.operations
    #
    # data_categories: [system.operations]
    #
    with open(f"{SAAS_DATASET_DIRECTORY}{file_name}", "w") as dataset_file:
        dataset_file.write(
            re.sub(
                r"(data_categories:)\n\s+- ([^\n]+)",
                r"\1 [\2]",
                yaml.dump(
                    {"dataset": [generated_dataset]},
                    default_flow_style=False,
                    sort_keys=False,
                    indent=2,
                ),
            )
        )


def generate_collections(
    fides_key: str, response: Dict[str, List[Row]], field_map: Dict[str, Collection]
) -> List[Dict[str, Any]]:
    """
    Generates a list of collections based on the response data or returns
    the existing collections if no row data is available.
    """

    collections = []
    for key, rows in response.items():
        collection_name = key.replace(f"{fides_key}:", "")
        fields = None
        if len(rows):
            fields = generate_fields(rows[0], collection_name, field_map)
        elif field_map.get(collection_name):
            fields = field_map[collection_name]

        if fields:
            collection = {"name": collection_name, "fields": fields}
            collections.append(collection)
    return collections


def generate_fields(
    row: Dict[str, Any], parent_path: str, field_map: Dict[str, Collection]
) -> List[Dict[str, Dict]]:
    """
    Generates a simplified version of dataset fields based on the row data.
    Maintains the current path of the traversal to determine if the field
    exists in the existing dataset. If it does, the existing attributes
    are preserved instead of generating them from the row data.
    """

    fields = []
    for key, value in row.items():
        # increment path
        current_path = f"{parent_path}.{key}"
        # initialize field
        field = {"name": key}
        # derive data_type based on row data
        data_type = get_data_type(value)

        # only values of type object or object[] should have sub-fields defined
        # additionally object and object[] cannot have data_categories
        if data_type == "object":
            field["fidesops_meta"] = {"data_type": data_type}
            field["fields"] = generate_fields(value, current_path, field_map)
        elif data_type == "object[]":
            field["fidesops_meta"] = {"data_type": data_type}
            field["fields"] = generate_fields(value[0], current_path, field_map)
        else:
            existing_field = get_existing_field(field_map, current_path)
            if existing_field:
                if isinstance(existing_field, ScalarField):
                    # field exists, copy existing data categories and data_type (if available)
                    field["data_categories"] = existing_field.data_categories or [
                        "system.operations"
                    ]
                    data_type = (
                        existing_field.data_type()
                        if existing_field.data_type() != "None"
                        else data_type
                    )
                    if data_type:
                        field["fidesops_meta"] = {"data_type": data_type}
                elif isinstance(existing_field, ObjectField):
                    # the existing field has a more complex type than what we could derive
                    # from the API response, we need to copy the fields instead of just
                    # the data_categories and data_type
                    field["fidesops_meta"] = {
                        "data_type": "object[]" if isinstance(value, list) else "object"
                    }
                    field["fields"] = get_simple_fields(existing_field.fields.values())
            else:
                # we don't have this field in our dataset, use the default category
                # and the derived data_type
                field["data_categories"] = ["system.operations"]
                # we don't assume the data_type for empty strings, empty lists,
                # empty dicts, or nulls
                if data_type:
                    field["fidesops_meta"] = {"data_type": data_type}
        fields.append(field)
    return fields


def get_simple_fields(fields: Iterable[Field]) -> List[Dict[str, Any]]:
    """
    Converts dataset fields into simple dictionaries with only
    name, data_category, and data_type.
    """

    object_list = []
    for field in fields:
        object = {"name": field.name}
        if field.data_categories:
            object["data_categories"] = field.data_categories
        if field.data_type() != "None":
            object["fidesops_meta"] = {"data_type": field.data_type()}
        if isinstance(field, ObjectField) and field.fields:
            object["fields"] = get_simple_fields(field.fields.values())
        object_list.append(object)
    return object_list


def get_existing_field(field_map: Dict[str, Collection], path: str) -> Optional[Field]:
    """
    Lookup existing field by collection name and field path.
    """
    collection_name, field_path = path.split(".", 1)
    collection = field_map.get(collection_name)
    if collection:
        return collection.field_dict.get(FieldPath.parse((field_path)))
    return None


def get_data_type(value) -> Optional[str]:
    """
    Returns the simple or array type of the given value.
    """

    data_type = None

    # cannot assume data type for falsy values
    if not value:
        return data_type

    if isinstance(value, bool):
        data_type = "boolean"
    elif isinstance(value, int):
        data_type = "integer"
    elif isinstance(value, float):
        data_type = "float"
    elif isinstance(value, str):
        data_type = "string"
    elif isinstance(value, dict):
        data_type = "object"
    elif isinstance(value, list):
        if all(isinstance(item, int) for item in value):
            data_type = "integer[]"
        elif all(isinstance(item, float) for item in value):
            data_type = "float[]"
        elif all(isinstance(item, str) for item in value):
            data_type = "string[]"
        elif all(isinstance(item, dict) for item in value):
            data_type = "object[]"

    return data_type
