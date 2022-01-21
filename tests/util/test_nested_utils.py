import pytest

from fidesops.common_exceptions import FidesopsException
from fidesops.util.nested_utils import unflatten_dict


def test_unflatten_dict():
    input_data = {"A.B": 1, "A.C": 2, "A.D.E": 3}
    assert unflatten_dict(input_data) == {"A": {"B": 1, "C": 2, "D": {"E": 3}}}

    input_data = {"A": 2, "B": 3, "C": 4}
    assert unflatten_dict(input_data) == input_data

    input_data = {"A.B": 1, "A": 2, "A.C": 3}
    # You don't want to pass in input data like this, you have conflicts here -
    with pytest.raises(FidesopsException):
        unflatten_dict(input_data)
