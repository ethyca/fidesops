from fidesops.graph.config import FieldPath
from fidesops.task.refine_target_path import refine_target_path, build_incoming_refined_target_paths


def test_refine_target_path(sample_data):
    result = refine_target_path(
        sample_data, ["months", "march", "crops"], ["swiss chard"]
    )
    assert result == [
        ["months", "march", 0, "crops", 0],
        ["months", "march", 0, "crops", 1],
    ]

    result = refine_target_path(sample_data, ["_id"], [12345])
    assert result == ["_id"]

    result = refine_target_path(sample_data, ["snacks"], ["pizza"])
    assert result == ["snacks", 0]

    result = refine_target_path(sample_data, ["thread", "comment"], ["com_0002"])
    assert result == [["thread", 1, "comment"], ["thread", 2, "comment"]]

    result = refine_target_path(sample_data, ["seats", "first_choice"], ["A2"])
    assert result == ["seats", "first_choice"]

    result = refine_target_path(sample_data, ["upgrades", "books"], ["SICP"])
    assert result == ["upgrades", "books", 1]

    result = refine_target_path(sample_data, ["other_flights", "CHO"], ["1 PM"])
    assert result == [["other_flights", 0, "CHO", 1], ["other_flights", 1, "CHO", 1]]

    result = refine_target_path(sample_data, ["bad_path"], ["bad match"])
    assert result == []

    result = refine_target_path(sample_data, ["hello"], only=[2])
    assert result == [["hello", 1], ["hello", 4]]

    result = refine_target_path(
        sample_data, ["months", "july", "crops"], ["watermelon", "grapes"]
    )
    assert result == [
        ["months", "july", 0, "crops", 0],
        ["months", "july", 0, "crops", 2],
    ]

    result = refine_target_path(sample_data, ["weights"], [4])
    assert result == ["weights", 1, 1]

    result = refine_target_path(sample_data, ["toppings"], ["cheese"])
    assert result == [["toppings", 0, 1, 1], ["toppings", 0, 1, 2]]

    result = refine_target_path(sample_data, ["A", "C", "M"], ["n"])
    assert result == [["A", "C", 0, "M", 1], ["A", "C", 0, "M", 2]]

    result = refine_target_path(sample_data, [], ["pizza"])
    assert result == []

    result = refine_target_path(sample_data, ["C"], ["B"])
    assert result == [["C", 0, 1], ["C", 0, 3], ["C", 1, 2], ["C", 1, 3]]

    result = refine_target_path(sample_data, ["D"], ["B"])
    assert result == [
        ["D", 0, 0, 1],
        ["D", 0, 0, 3],
        ["D", 0, 1, 2],
        ["D", 0, 1, 3],
        ["D", 1, 0, 1],
        ["D", 1, 0, 3],
        ["D", 1, 1, 2],
        ["D", 1, 1, 3],
    ]

    result = refine_target_path(sample_data, ["E"], ["B"])
    assert result == [
        ["E", 0, 0, 0],
        ["E", 0, 1, 0, 1],
        ["E", 0, 1, 0, 3],
        ["E", 0, 1, 1, 2],
        ["E", 0, 1, 1, 3],
    ]

    result = refine_target_path(sample_data, ["F"], ["a"])
    assert result == [["F", 0], ["F", 1, 1], ["F", 1, 2, 0, 1], ["F", 1, 2, 0, 2]]


def test_build_incoming_refined_target_paths(sample_data):
    incoming_paths = {
        FieldPath(
            "F",
        ): ["a"],
        FieldPath("snacks"): ["pizza"],
        FieldPath("thread", "comment"): ["com_0002"],
    }
    result = build_incoming_refined_target_paths(sample_data, incoming_paths)
    assert result == [
        ["F", 0],
        ["snacks", 0],
        ["F", 1, 1],
        ["thread", 1, "comment"],
        ["thread", 2, "comment"],
        ["F", 1, 2, 0, 1],
        ["F", 1, 2, 0, 2],
    ]

