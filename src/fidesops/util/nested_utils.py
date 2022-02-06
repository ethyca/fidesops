from typing import List, Dict, Any, Optional, Union, Sequence


from fidesops.graph.config import FieldPath


def _get_starter(obj: Any) -> Any:
    """
    Used in recursive 'select_field_from_input_data' as we're adding fields that match
    desired data categories to the filtered results we'll return to the user.
    """
    if isinstance(obj, list):
        return []
    if isinstance(obj, dict):
        return {}
    return obj


def _skip_unmatched_scalar(element: Any, only: List, base: List) -> bool:
    """
    Data in one collection can be used to lookup data inside arrays inside another collection.  For some identities
    or referenced fields contained in arrays, the user may only want to return the "matched" result.

    If the given element is a scalar value *within an array*, and is in the "only" list and hasn't already been
    added to the "base" list, we want to add it.

    For example, we might *only* want to retrieve the identity data ["customer-1@example.com"] from an array.
    If this element is "customer-1@example.com" and is contained in an array, and we haven't already saved this off,
    we'll add it to our staged array.
    """
    return bool(
        only
        and not isinstance(element, (dict, list))
        and (element not in only or element in base)
    )


def select_field_from_input_data(
    base: Any, input_data: Any, target_path: FieldPath, only: List = []
) -> Dict:
    """Extract input_data along the target_path and add to "base"

    Used to incrementally filter a record retrieved from a collection to only contain the target field paths with the
    relevant data categories.  To use, you might start with a base that is an empty dict, and loop through a list of
    FieldPaths you want, continuing to pass in the ever-growing new base that was returned from the previous iteration.
    """

    if isinstance(input_data, list):
        for i, elem in enumerate(input_data):
            if _skip_unmatched_scalar(elem, only, base):
                continue
            try:
                base[i] = select_field_from_input_data(base[i], elem, target_path, only)
            except IndexError:
                base.append(
                    select_field_from_input_data(
                        _get_starter(elem), elem, target_path, only
                    )
                )

    elif isinstance(input_data, dict):
        for key in input_data:
            if key == target_path.levels[0]:
                if key not in base:
                    base[key] = _get_starter(input_data[key])
                base[key] = select_field_from_input_data(
                    base[key], input_data[key], FieldPath(*target_path.levels[1:]), only
                )
    return base


def flatten_and_merge_matches(
    input_data: Dict[str, Any],
    target_path: FieldPath,
    flattened_matches: Optional[List] = None,
) -> List[Any]:
    """
    Uses target_path from the previous collection to locate specific value(s) in input_data, and returns matches
    as a flattened array. These values are used to locate records in a subsequent collection.

    Multiple values are possible when a target_path corresponds to multiple sub-fields, for example,
    in an array of objects.

    """
    if flattened_matches is None:
        flattened_matches = []

    if isinstance(input_data, list):
        for elem in input_data:
            flatten_and_merge_matches(elem, target_path, flattened_matches)

    elif isinstance(input_data, dict):
        for key, value in input_data.items():
            if target_path.levels and key == target_path.levels[0]:
                flatten_and_merge_matches(
                    value, FieldPath(*target_path.levels[1:]), flattened_matches
                )

    else:
        flattened_matches.append(input_data)

    return flattened_matches


def strip_empty_dicts(data: Any) -> Dict:
    """
    Recursively updates data in place to remove empty dictionaries at any level in a nested
    dictionary or within an array.

    `select_field_from_input_data` recursively builds a nested structure based on desired field paths.
    If no input data was found along a deeply nested field path, we may have empty dicts to clean up
    before supplying response to user.
    """
    if isinstance(data, dict):
        for k, v in data.copy().items():
            if isinstance(v, (dict, list)):
                v = strip_empty_dicts(v)

            if v == {}:
                del data[k]

    elif isinstance(data, list):
        for elem in data:
            strip_empty_dicts(elem)

    return data


def build_incoming_refined_target_paths(
    row: Dict[str, Any], incoming_paths: Dict[FieldPath, List]
) -> List[List]:
    """
    Expand incoming field paths to be more detailed field paths with
    """
    found_paths = []
    for target_path, only in incoming_paths.items():
        path = refine_target_path(row, list(target_path.levels), only)
        if path:
            if isinstance(path[0], list):
                found_paths.extend(path)
            else:
                found_paths.append(path)
    found_paths.sort(key=len)
    return found_paths


def refine_target_path(
    record: Dict[str, Any], field_path: List[str], only=Sequence[Any]
) -> List:
    """
    Expand target path to be more accurately target data within arrays by inserting indices
    into path where applicable.  If one match, returns a list, otherwise returns a list of lists

    For example:
    refine_target_path({"A": {"B": [{"C": "D"}, {"C": "F"}, {"C": "G"}]}}, ["A", "B", "C"], only=["F", "G"])

    -> [['A', 'B', 1, 'C'], ['A', 'B', 2, 'C']]
    """
    try:
        current_level = field_path[0]
        current_elem = record[current_level]
    except (IndexError, KeyError):  # No field path or field path not found in record
        return []

    if isinstance(current_elem, dict):
        next_levels = refine_target_path(current_elem, field_path[1:], only)
        return _update_path(current_level, next_levels)

    if isinstance(current_elem, list):
        next_levels = _enter_array(current_elem, field_path[1:], only)
        return _update_path(current_level, next_levels)

    # Simple case - value is a scalar
    return [current_level] if _match_found(current_elem, only) else []


def _enter_array(array: List[Any], field_path: List[str], only=Sequence[Any]) -> List:
    """
    Used by recursive "refine_target_path" whenever arrays are encountered in the record.
    """
    results = []
    for index, elem in enumerate(array):
        current_result = []

        if field_path:
            next_result = refine_target_path(elem, field_path, only)
            current_result = _update_path(index, next_result)
        else:
            if isinstance(elem, list):
                next_result = _enter_array(
                    elem, field_path, only
                )  # Nested enter_array calls needed for lists in lists
                current_result = _update_path(index, next_result)
            else:
                if _match_found(elem, only):
                    current_result = [index]

        if current_result:  # Match found at lower level
            if isinstance(current_result[0], list):
                # Keeps nested lists at most list of lists
                results.extend(current_result)
            else:
                results.append(current_result)

    return results[0] if len(results) == 1 else results


def _match_found(elem: Any, only: Sequence[Any]) -> bool:
    """The given scalar element matches one of the input values"""
    return elem in only


def _update_path(
    current_level: Union[str, int], deeper_levels: List[Union[str, int]]
) -> List[Union[str, int]]:
    """
    Used by "refine_target_path" and "_enter_array" to recursively build a
    more refined target path to the desired data.
    """
    if not deeper_levels:
        # Element did not contain a match
        return []

    if isinstance(deeper_levels[0], list):
        result = []
        for item in deeper_levels:
            # Builds multiple possible paths
            result.append(_update_path(current_level, item))
        return result

    # Consolidates current level with deeper levels
    result = [current_level]
    result.extend(deeper_levels)
    return result
