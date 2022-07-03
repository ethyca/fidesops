import re
from typing import Any, Dict, Iterable, List, Optional

import yaml

from fidesops.graph.config import Collection, Field, FieldPath, ObjectField, ScalarField
from fidesops.models.connectionconfig import ConnectionConfig
from fidesops.models.datasetconfig import DatasetConfig, convert_dataset_to_graph
from fidesops.schemas.dataset import FidesopsDataset
from fidesops.util.collection_util import Row

SAAS_DATASET_DIRECTORY = "data/saas/dataset/"


def update_dataset(
    connection_config: ConnectionConfig,
    dataset_config: DatasetConfig,
    api_data: Dict[str, List[Row]],
    file_name: str,
):
    """
    Helper function to update the dataset in the given dataset_config
    with api_data and write the formatted result to the specified file.
    """

    generated_dataset = generate_dataset(
        dict(**dataset_config.dataset),
        api_data,
        [endpoint["name"] for endpoint in connection_config.saas_config["endpoints"]],
    )

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


def generate_dataset(
    existing_dataset: Dict[str, Any],
    api_data: Dict[str, List[Row]],
    collection_order: List[str],
):
    """
    Generates a dataset which is an aggregate of the existing dataset and
    any new fields generated from the API data. Orders the collections
    based on the order of collection_order.
    """

    fides_key = existing_dataset["fides_key"]

    # convert FidesopsDataset to Dataset to be able to use the Collection helpers
    existing_graph = convert_dataset_to_graph(
        FidesopsDataset(**existing_dataset), fides_key
    )
    collection_map = {
        collection.name: collection for collection in existing_graph.collections
    }
    generated_collections = generate_collections(fides_key, api_data, collection_map)

    return {
        "fides_key": existing_dataset["fides_key"],
        "name": existing_dataset["name"],
        "description": existing_dataset["description"],
        "collections": [
            {
                "name": collection["name"],
                "fields": collection["fields"],
            }
            for collection in sorted(
                generated_collections,
                key=lambda collection: collection_order.index(collection["name"]),
            )
        ],
    }


def generate_collections(
    fides_key: str,
    api_data: Dict[str, List[Row]],
    collection_map: Dict[str, Collection],
) -> List[Dict[str, Any]]:
    """
    Generates a list of collections based on the response data or returns
    the existing collections if no API data is available.
    """

    collections = []
    for key, rows in api_data.items():

        collection_name = key.replace(f"{fides_key}:", "")
        fields = None

        if len(rows):
            fields = generate_fields(rows[0], collection_name, collection_map)
        elif collection_map.get(collection_name):
            fields = collection_map[collection_name]

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
    exists in the existing dataset. If it does, some existing attributes
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
            if existing_field := get_existing_field(field_map, current_path):
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
                    # from the API response, we need to copy the fields too instead of just
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


def get_existing_field(field_map: Dict[str, Collection], path: str) -> Optional[Field]:
    """
    Lookup existing field by collection name and field path.
    """
    collection_name, field_path = path.split(".", 1)
    if collection := field_map.get(collection_name):
        return collection.field_dict.get(FieldPath.parse((field_path)))
    return None


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


def get_data_type(value) -> Optional[str]:
    """
    Returns the simple or array type of the given value.
    """

    data_type = None

    # cannot assume data type for missing or empty values
    if value in (None, "", [], {}):
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
