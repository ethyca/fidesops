import logging
import itertools
from collections import defaultdict
from typing import List, Dict, Any, Optional, Union, Set

from fidesops.graph.config import FieldPath, CollectionAddress
from fidesops.schemas.shared_schemas import FidesOpsKey
from fidesops.task.filter_element_match import filter_element_match
from fidesops.util.cache import get_cache

logger = logging.getLogger(__name__)


def filter_data_categories(
    access_request_results: Dict[str, Optional[Any]],
    target_categories: Set[str],
    data_category_fields: Dict[CollectionAddress, Dict[FidesOpsKey, List[FieldPath]]],
    privacy_request_id: str,
) -> Dict[str, List[Dict[str, Optional[Any]]]]:
    """Filter access request results to only return fields associated with the target data categories
    and subcategories

    If data category "user.provided.identifiable.contact" is specified on one of the rule targets,
    all fields on subcategories also apply, so ["user.provided.identifiable.contact.city",
    "user.provided.identifiable.contact.street", ...], etc.
    """
    logger.info(
        "Filtering Access Request results to return fields associated with data categories"
    )
    filtered_access_results: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    collection_inputs = get_collection_inputs_from_cache(privacy_request_id)
    for node_address, results in access_request_results.items():
        if not results:
            continue

        # Gets all FieldPaths on this traversal_node associated with the requested data
        # categories and sub data categories
        target_field_paths: Set[FieldPath] = set(
            itertools.chain(
                *[
                    field_paths
                    for cat, field_paths in data_category_fields[
                        CollectionAddress.from_string(node_address)
                    ].items()
                    if any([cat.startswith(tar) for tar in target_categories])
                ]
            )
        )

        if not target_field_paths:
            continue

        for row in results:
            row = filter_element_match(
                row,
                collection_inputs.get(CollectionAddress.from_string(node_address), {}),
            )
            filtered_results: Dict[str, Any] = {}
            for field_path in target_field_paths:
                select_and_save_field(filtered_results, row, field_path)
            remove_empty_objects(filtered_results)
            filtered_access_results[node_address].append(filtered_results)

    return filtered_access_results


def get_collection_inputs_from_cache(
    privacy_request_id: str,
) -> Dict[CollectionAddress, Dict[FieldPath, List]]:
    """
    Retrieve the inputs to each collection from the cache that was used to build queries for the given privacy request.

    In the example return below, we can see that customer_id 1 was used to find records in the mongo_test orders
    collection, and the nested_resource.email values "customer-1@example.com" and "customer@example.com" were used to
    locate records on the mongo_test customer collection.
    {
        CollectionAddress("mongo_test", "orders"): {FieldPath("customer_id"): ["1"]},
        CollectionAddress("mongo_test", "customer"): {
            FieldPath("nested_resource.email"): ["customer-1@example.com", "customer@example.com"]
        }
    }

    """
    cache = get_cache()
    value_dict = cache.get_encoded_objects_by_prefix(f"INPUT__{privacy_request_id}")
    return {
        CollectionAddress.from_string(collection_name.split("__")[-1]): {
            FieldPath.parse(field): inputs
            for field, inputs in collection_inputs.items()
        }
        for collection_name, collection_inputs in value_dict.items()
    }


def select_and_save_field(saved: Any, row: Any, target_path: FieldPath) -> Dict:
    """Extract the data located along the given `target_path` from the row and save in the "base" dictionary.

    Entire rows are returned from your collections; this function will incrementally just pull the PII from the rows,
    by retrieving data along target_paths to relevant data categories.

    To use, you might start with a base that is an empty dict, and loop through a list of FieldPaths you want,
    continuing to pass in the ever-growing new "saved" collection that was returned from the previous iteration.
    """

    def _defaultdict_or_array(resource: Any) -> Any:
        """Helper for building new nested resource - can return an empty dict, empty array or resource itself"""
        return type(resource)() if isinstance(resource, (list, dict)) else resource

    if isinstance(row, list):
        for i, elem in enumerate(row):
            try:
                saved[i] = select_and_save_field(saved[i], elem, target_path)
            except IndexError:
                saved.append(
                    select_and_save_field(
                        _defaultdict_or_array(elem), elem, target_path
                    )
                )

    elif isinstance(row, dict):
        for key in row:
            if key == target_path.levels[0]:
                if key not in saved:
                    saved[key] = _defaultdict_or_array(row[key])
                saved[key] = select_and_save_field(
                    saved[key], row[key], FieldPath(*target_path.levels[1:])
                )
    return saved


RecursiveRow = Union[Dict[Any, Any], List[Any]]


def remove_empty_objects(row: RecursiveRow) -> RecursiveRow:
    """
    Recursively updates row in place to remove empty dictionaries at any level in collection or
    from embedded collections in arrays.

    `select_and_save_field` recursively builds a nested structure based on desired field paths.
    If no input data was found along a deeply nested field path, we may have empty dicts to clean up
    before supplying response to user.
    """
    if isinstance(row, dict):
        for key, value in row.copy().items():
            if isinstance(value, (dict, list)):
                value = remove_empty_objects(value)

            if value == {}:
                del row[key]

    elif isinstance(row, list):
        for elem in row:
            remove_empty_objects(elem)

    return row
