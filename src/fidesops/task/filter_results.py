import logging
from typing import List, Dict, Any, Union

from fidesops.graph.config import FieldPath

logger = logging.getLogger(__name__)


def select_and_save_field(saved: Any, row: Any, target_path: FieldPath) -> Dict:
    """Extract the data located along the given `target_path` from the row and save in the "base" dictionary.

    Entire rows are returned from your collections; this function will incrementally just pull the PII from the rows,
    by retrieving data along target_paths to relevant data categories.

    To use, you might start with a base that is an empty dict, and loop through a list of FieldPaths you want,
    continuing to pass in the ever-growing new "saved" collection that was returned from the previous iteration.

    :param saved: Call with an empty dict to start, it will recursively update as data along the target_path is added to it.
    :param row: Call with retrieved row to start, it will recursively be called with a variety of object types until we
    reach the most deeply nested value.
    :param target_path: FieldPath to the data we want to retrieve

    :return: modified saved dictionary with given field path if found
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

    :param row: Pass in retrieved row, and it will recursively go through objects and arrays and filter out empty objects.
    :return: Updated row with empty objects removed
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
