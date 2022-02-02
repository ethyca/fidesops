from typing import List, Dict, Any


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
        and not type(element) in [list, dict]
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
