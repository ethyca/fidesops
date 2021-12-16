from bson import ObjectId

from fidesops.graph.data_type import (
    SimpleDataType,
    NoOpTypeConverter,
    get_data_type_converter,
    StringTypeConverter,
)


def test_int_convert():
    converter = SimpleDataType.integer.value
    assert converter.to_value("1") == 1
    assert converter.to_value(1.0) == 1
    assert converter.to_value(1) == 1
    assert converter.to_value("A") is None


def test_string_convert():
    converter = SimpleDataType.string.value
    assert converter.to_value(1.0) == "1.0"
    assert converter.to_value(1) == "1"
    assert (
        converter.to_value(ObjectId("abc123abc123abc123abc123"))
        == "abc123abc123abc123abc123"
    )


def test_float_convert():
    converter = SimpleDataType.float.value
    assert converter.to_value(1) == 1.0
    assert converter.to_value("1.0") == 1.0


def test_bool_convert():
    converter = SimpleDataType.boolean.value
    assert converter.to_value(1) == True
    assert converter.to_value(0) == False
    assert converter.to_value("True") == True
    assert converter.to_value("False") == False
    assert converter.to_value("NOT A BOOLEAN ") is None


def test_object_id_convert():
    converter = SimpleDataType.object_id.value
    assert converter.to_value("abc123abc123abc123abc123") == ObjectId(
        "abc123abc123abc123abc123"
    )
    assert converter.to_value("abc123abc1") is None


def test_safe_none_conversion():
    """Ensure that None is safely handled in any type."""
    for data_type in SimpleDataType:
        converter = data_type.value
        assert converter.to_value(None) is None


def test_get_data_type_converter():
    v = get_data_type_converter(None)
    v2 = get_data_type_converter("")
    v3 = get_data_type_converter("string")
    assert isinstance(get_data_type_converter(None), NoOpTypeConverter)
    assert isinstance(get_data_type_converter(""), NoOpTypeConverter)
    assert isinstance(get_data_type_converter("string"), StringTypeConverter)
