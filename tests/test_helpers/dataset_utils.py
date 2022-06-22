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

    # use endpoint order in the SaaS config as the collection order in the dataset
    generated_collections = generate_collections(dataset["fides_key"], response)
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

    merged_dataset = pydash.objects.merge(generated_dataset, {**dataset})

    with open(f"{SAAS_DATASET_DIRECTORY}{file_name}", "w") as dataset_file:
        dataset_file.write(
            re.sub(
                r"(data_categories:)\n\s+- ([^\n]+)",
                r"\1 [\2]",
                yaml.dump(
                    {"dataset": [merged_dataset]},
                    default_flow_style=False,
                    sort_keys=False,
                    indent=2,
                ),
            )
        )


def generate_collections(
    fides_key: str, response: Dict[str, List[Row]]
) -> List[Dict[str, Any]]:
    collections: List[Dict[str, Any]] = []
    for collection_name, rows in response.items():
        if len(rows):
            collection = {
                "name": collection_name.replace(f"{fides_key}:", ""),
                "fields": generate_fields(rows[0]),
            }
            collections.append(collection)
    return collections


def generate_fields(row: Dict[str, Any]) -> List[Dict[str, Dict]]:
    fields = []
    for key, value in row.items():

        field = {"name": key}
        data_type = get_data_type(value)

        # only values of type object or object[] should have sub-fields defined
        # additionally object and object[] cannot have data_categories
        if data_type == "object" or data_type == "object[]":
            field["fidesops_meta"] = {"data_type": get_data_type(value)}
            field["fields"] = generate_fields(value)
        else:
            field["data_categories"] = ["system.operations"]
            field["fidesops_meta"] = {"data_type": get_data_type(value)}

        if field.get("fields") != []:
            fields.append(field)
    return fields


def get_data_type(value) -> Optional[str]:
    data_type = "string"
    if isinstance(value, bool):
        data_type = "boolean"
    elif isinstance(value, int):
        data_type = "integer"
    elif isinstance(value, list):
        if all(isinstance(item, int) for item in value):
            data_type = "integer[]"
        if all(isinstance(item, str) for item in value):
            data_type = "string[]"
        elif all(isinstance(item, dict) for item in value):
            data_type = "object[]"
    elif isinstance(value, dict):
        data_type = "object"
    return data_type
