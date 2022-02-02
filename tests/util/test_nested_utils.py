from fidesops.graph.config import FieldPath
from fidesops.util.nested_utils import select_field_from_input_data


def test_select_field():
    final_results = {}
    flat = {
        "A": "a",
        "B": "b",
        "C": ["d", "e", "f"],
        "D": ["g", "h", "i", "j"],
        "E": {
            "F": "g",
            "H": "i",
            "J": {"K": {"L": {"M": ["m", "n", "o"], "P": "p"}}, "N": {"O": "o"}},
        },
        "F": [{"G": "g", "H": "h"}, {"G": "h", "H": "i"}, {"G": "i", "H": "j"}],
        "H": [
            [
                {"M": [1, 2, 3], "N": "n"},
                {"M": [3, 2, 1], "N": "o"},
                {"M": [1, 1, 1], "N": "p"},
            ],
            [
                {"M": [4, 5, 6], "N": "q"},
                {"M": [2, 2, 2], "N": "s"},
                {"M": [], "N": "u"},
            ],
            [
                {"M": [7, 8, 9], "N": "w"},
                {"M": [6, 6, 6], "N": "y"},
                {"M": [2], "N": "z"},
            ],
        ],
        "I": {
            "X": [
                {"J": "j", "K": ["k"]},
                {"J": "m", "K": ["customer@example.com", "customer-1@example.com"]},
            ],
            "Y": [{"J": "l", "K": ["n"]}, {"J": "m", "K": ["customer@example.com"]}],
            "Z": [{"J": "m", "K": ["n"]}],
        },
        "J": {
            "K": {
                "L": {
                    "M": {
                        "N": {
                            "O": ["customer@example.com", "customer@gmail.com"],
                            "P": ["customer@yahoo.com", "customer@customer.com"],
                        }
                    }
                }
            }
        },
    }

    # Test simple scalar field selected
    assert select_field_from_input_data(final_results, flat, FieldPath("A")) == {
        "A": "a"
    }
    # Test array field selected, and added to final results
    assert select_field_from_input_data(final_results, flat, FieldPath("C")) == {
        "A": "a",
        "C": ["d", "e", "f"],
    }
    # Test only certain scalar fields selected and added to final results
    assert select_field_from_input_data(
        final_results, flat, FieldPath("D"), only=["h", "j"]
    ) == {
        "A": "a",
        "C": ["d", "e", "f"],
        "D": ["h", "j"],
    }
    # Test nested field selected and added to final results
    assert select_field_from_input_data(final_results, flat, FieldPath("E", "F")) == {
        "A": "a",
        "C": ["d", "e", "f"],
        "D": ["h", "j"],
        "E": {"F": "g"},
    }
    # Test select field not in results
    assert select_field_from_input_data(
        final_results, flat, FieldPath("E", "F", "Z", "X")
    ) == {
        "A": "a",
        "C": ["d", "e", "f"],
        "D": ["h", "j"],
        "E": {"F": "g"},
    }

    # Test more deeply nested scalar from previous dict
    assert select_field_from_input_data(
        final_results, flat, FieldPath("E", "J", "K", "L", "M"), only=["n"]
    ) == {
        "A": "a",
        "C": ["d", "e", "f"],
        "D": ["h", "j"],
        "E": {"F": "g", "J": {"K": {"L": {"M": ["n"]}}}},
    }

    # Test get matching dict key for each element in array
    assert select_field_from_input_data(final_results, flat, FieldPath("F", "G")) == {
        "A": "a",
        "C": ["d", "e", "f"],
        "D": ["h", "j"],
        "E": {"F": "g", "J": {"K": {"L": {"M": ["n"]}}}},
        "F": [{"G": "g"}, {"G": "h"}, {"G": "i"}],
    }

    # Test get nested fields inside nested arrays
    assert select_field_from_input_data(final_results, flat, FieldPath("H", "N")) == {
        "A": "a",
        "C": ["d", "e", "f"],
        "D": ["h", "j"],
        "E": {"F": "g", "J": {"K": {"L": {"M": ["n"]}}}},
        "F": [{"G": "g"}, {"G": "h"}, {"G": "i"}],
        "H": [
            [{"N": "n"}, {"N": "o"}, {"N": "p"}],
            [{"N": "q"}, {"N": "s"}, {"N": "u"}],
            [{"N": "w"}, {"N": "y"}, {"N": "z"}],
        ],
    }

    # Test get nested fields inside nested arrays
    assert select_field_from_input_data(
        final_results, flat, FieldPath("H", "M"), only=[2]
    ) == {
        "A": "a",
        "C": ["d", "e", "f"],
        "D": ["h", "j"],
        "E": {"F": "g", "J": {"K": {"L": {"M": ["n"]}}}},
        "F": [{"G": "g"}, {"G": "h"}, {"G": "i"}],
        "H": [
            [{"M": [2], "N": "n"}, {"M": [2], "N": "o"}, {"M": [], "N": "p"}],
            [{"M": [], "N": "q"}, {"M": [2], "N": "s"}, {"M": [], "N": "u"}],
            [{"M": [], "N": "w"}, {"M": [], "N": "y"}, {"M": [2], "N": "z"}],
        ],
    }

    # Test get dict of array of dict fields
    assert select_field_from_input_data(
        final_results, flat, FieldPath("I", "X", "J")
    ) == {
        "A": "a",
        "C": ["d", "e", "f"],
        "D": ["h", "j"],
        "E": {"F": "g", "J": {"K": {"L": {"M": ["n"]}}}},
        "F": [{"G": "g"}, {"G": "h"}, {"G": "i"}],
        "H": [
            [{"M": [2], "N": "n"}, {"M": [2], "N": "o"}, {"M": [], "N": "p"}],
            [{"M": [], "N": "q"}, {"M": [2], "N": "s"}, {"M": [], "N": "u"}],
            [{"M": [], "N": "w"}, {"M": [], "N": "y"}, {"M": [2], "N": "z"}],
        ],
        "I": {"X": [{"J": "j"}, {"J": "m"}]},
    }

    # Test get deeply nested array field with only matching data, array in arrays
    assert select_field_from_input_data(
        final_results, flat, FieldPath("I", "X", "K"), only=["customer-1@example.com"]
    ) == {
        "A": "a",
        "C": ["d", "e", "f"],
        "D": ["h", "j"],
        "E": {"F": "g", "J": {"K": {"L": {"M": ["n"]}}}},
        "F": [{"G": "g"}, {"G": "h"}, {"G": "i"}],
        "H": [
            [{"M": [2], "N": "n"}, {"M": [2], "N": "o"}, {"M": [], "N": "p"}],
            [{"M": [], "N": "q"}, {"M": [2], "N": "s"}, {"M": [], "N": "u"}],
            [{"M": [], "N": "w"}, {"M": [], "N": "y"}, {"M": [2], "N": "z"}],
        ],
        "I": {"X": [{"J": "j", "K": []}, {"J": "m", "K": ["customer-1@example.com"]}]},
    }

    # Get deeply nested array inside of dicts, with only matching data
    assert select_field_from_input_data(
        final_results, flat, FieldPath("I", "Y", "K"), only=["n"]
    ) == {
        "A": "a",
        "C": ["d", "e", "f"],
        "D": ["h", "j"],
        "E": {"F": "g", "J": {"K": {"L": {"M": ["n"]}}}},
        "F": [{"G": "g"}, {"G": "h"}, {"G": "i"}],
        "H": [
            [{"M": [2], "N": "n"}, {"M": [2], "N": "o"}, {"M": [], "N": "p"}],
            [{"M": [], "N": "q"}, {"M": [2], "N": "s"}, {"M": [], "N": "u"}],
            [{"M": [], "N": "w"}, {"M": [], "N": "y"}, {"M": [2], "N": "z"}],
        ],
        "I": {
            "X": [{"J": "j", "K": []}, {"J": "m", "K": ["customer-1@example.com"]}],
            "Y": [{"K": ["n"]}, {"K": []}],
        },
    }

    assert select_field_from_input_data(
        final_results,
        flat,
        FieldPath("J", "K", "L", "M", "N", "O"),
        only=["customer@gmail.com"],
    ) == {
        "A": "a",
        "C": ["d", "e", "f"],
        "D": ["h", "j"],
        "E": {"F": "g", "J": {"K": {"L": {"M": ["n"]}}}},
        "F": [{"G": "g"}, {"G": "h"}, {"G": "i"}],
        "H": [
            [{"M": [2], "N": "n"}, {"M": [2], "N": "o"}, {"M": [], "N": "p"}],
            [{"M": [], "N": "q"}, {"M": [2], "N": "s"}, {"M": [], "N": "u"}],
            [{"M": [], "N": "w"}, {"M": [], "N": "y"}, {"M": [2], "N": "z"}],
        ],
        "I": {
            "X": [{"J": "j", "K": []}, {"J": "m", "K": ["customer-1@example.com"]}],
            "Y": [{"K": ["n"]}, {"K": []}],
        },
        "J": {"K": {"L": {"M": {"N": {"O": ["customer@gmail.com"]}}}}},
    }
