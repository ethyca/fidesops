import re
from typing import Any, Dict, List, Optional

import pydash
import yaml

from fidesops.models.connectionconfig import ConnectionConfig
from fidesops.models.datasetconfig import DatasetConfig
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

    dataset = dataset_config.dataset

    # create field map from dataset to look up existing fields
    # as we're generating the new dataset
    field_map = {}
    for collection in dataset["collections"]:
        field_map[collection["name"]] = get_field_attributes(collection["fields"])

    # use endpoint order in the SaaS config as the collection order in the dataset
    generated_collections = generate_collections(
        dataset["fides_key"], response, field_map
    )
    collection_order = [
        endpoint["name"] for endpoint in connection_config.saas_config["endpoints"]
    ]
    generated_collections.sort(
        key=lambda collection: collection_order.index(collection["name"])
    )

    generated_dataset = {
        "fides_key": dataset["fides_key"],
        "name": dataset["name"],
        "description": dataset["description"],
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


def get_field_attributes(fields: Dict[str, Any]) -> Dict[str, Any]:
    data_categories = {}
    for field in fields:
        if field.get("fields"):
            data_categories[field["name"]] = get_field_attributes(field["fields"])
        else:
            data_categories[field["name"]] = field
    return data_categories


def generate_collections(
    fides_key: str, response: Dict[str, List[Row]], data_category_map: Dict[str, Any]
) -> List[Dict[str, Any]]:
    collections: List[Dict[str, Any]] = []
    for key, rows in response.items():
        collection_name = key.replace(f"{fides_key}:", "")
        if len(rows):
            collection = {
                "name": collection_name,
                "fields": generate_fields(rows[0], collection_name, data_category_map),
            }
            collections.append(collection)
    return collections


def generate_fields(
    row: Dict[str, Any], parent_path: str, data_category_map: Dict[str, Any]
) -> List[Dict[str, Dict]]:
    fields = []
    for key, value in row.items():
        current_path = f"{parent_path}.{key}"
        field = {"name": key}
        data_type = get_data_type(value)

        # only values of type object or object[] should have sub-fields defined
        # additionally object and object[] cannot have data_categories
        if data_type == "object":
            field["fidesops_meta"] = {"data_type": data_type}
            field["fields"] = generate_fields(value, current_path, data_category_map)
        elif data_type == "object[]":
            field["fidesops_meta"] = {"data_type": data_type}
            field["fields"] = generate_fields(value[0], current_path, data_category_map)
        else:
            existing_fields = pydash.get(data_category_map, current_path)
            if existing_fields:
                if existing_fields.get("data_categories"):
                    # field exists, copy existing data categories
                    field["data_categories"] = existing_fields["data_categories"]
                    field["fidesops_meta"] = {"data_type": data_type}
                else:
                    # the existing field is more defined than what we could derive from the API response
                    # we need to copy the fields instead of just the data_categories
                    field["fidesops_meta"] = {
                        "data_type": "object[]" if isinstance(value, list) else "object"
                    }
                    # mapping field properties manually to preserve order
                    field["fields"] = [
                        {
                            "name": existing_field.get("name"),
                            "data_categories": existing_field.get("data_categories"),
                            "fidesops_meta": existing_field.get("fidesops_meta"),
                        }
                        for existing_field in existing_fields.values()
                    ]
            else:
                # we don't have this field in our dataset, use the derived data_type and default category
                field["data_categories"] = ["system.operations"]
                field["fidesops_meta"] = {"data_type": data_type}

        if field.get("fields") != []:
            fields.append(field)
    return fields


def get_data_type(value) -> Optional[str]:
    data_type = None
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
