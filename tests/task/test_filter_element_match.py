from fidesops.graph.config import FieldPath
from fidesops.task.filter_element_match import (
    _expand_array_paths_to_preserve,
    filter_element_match,
)


def test_build_array_path_preservation():
    expanded_field_paths = [
        ["F", 0],
        ["snacks", 0],
        ["F", 1, 1],
        ["thread", 1, "comment"],
        ["thread", 2, "comment"],
        ["F", 1, 2, 0, 1],
        ["F", 1, 2, 0, 2],
        ["Non", "integer"],
    ]

    assert _expand_array_paths_to_preserve(expanded_field_paths) == {
        "F": [0, 1],
        "snacks": [0],
        "F.1": [1, 2],
        "thread": [1, 2],
        "F.1.2": [0],
        "F.1.2.0": [1, 2],
    }


def test_filter_element_match(sample_data):
    incoming_paths = {
        FieldPath(
            "F",
        ): ["a"],
        FieldPath("snacks"): ["pizza"],
        FieldPath("thread", "comment"): ["com_0002"],
    }

    filtered_record = filter_element_match(sample_data, incoming_paths)
    assert filtered_record == {
        "_id": 12345,
        "thread": [
            {
                "comment": "com_0002",
                "message": "yep, got your message, looks like it works",
                "chat_name": "Jane",
            },
            {"comment": "com_0002", "message": "hello!", "chat_name": "Jeanne"},
        ],
        "snacks": ["pizza"],
        "seats": {"first_choice": "A2", "second_choice": "B3"},
        "upgrades": {
            "magazines": ["Time", "People"],
            "books": ["Once upon a Time", "SICP"],
            "earplugs": True,
        },
        "other_flights": [
            {"DFW": ["11 AM", "12 PM"], "CHO": ["12 PM", "1 PM"]},
            {"DFW": ["2 AM", "12 PM"], "CHO": ["2 PM", "1 PM"]},
            {"DFW": ["3 AM", "2 AM"], "CHO": ["2 PM", "1:30 PM"]},
        ],
        "months": {
            "july": [
                {
                    "activities": ["swimming", "hiking"],
                    "crops": ["watermelon", "cheese", "grapes"],
                },
                {"activities": ["tubing"], "crops": ["corn"]},
            ],
            "march": [
                {
                    "activities": ["skiing", "bobsledding"],
                    "crops": ["swiss chard", "swiss chard"],
                },
                {"activities": ["hiking"], "crops": ["spinach"]},
            ],
        },
        "hello": [1, 2, 3, 4, 2],
        "weights": [[1, 2], [3, 4]],
        "toppings": [[["pepperoni", "salami"], ["pepperoni", "cheese", "cheese"]]],
        "A": {"C": [{"M": ["p", "n", "n"]}]},
        "C": [["A", "B", "C", "B"], ["G", "H", "B", "B"]],
        "D": [
            [["A", "B", "C", "B"], ["G", "H", "B", "B"]],
            [["A", "B", "C", "B"], ["G", "H", "B", "B"]],
        ],
        "E": [[["B"], [["A", "B", "C", "B"], ["G", "H", "B", "B"]]]],
        "F": ["a", ["a", [["a", "a"]]]],
    }
