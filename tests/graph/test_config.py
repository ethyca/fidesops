import pytest

from fidesops.graph.config import *


def test_collection_address_compare() -> None:
    assert CollectionAddress("A", "B") == CollectionAddress("A", "B")
    assert not CollectionAddress("A", "B") == 1
    assert CollectionAddress("A", "B") < CollectionAddress("C", "D")


def test_field_address_compare() -> None:
    assert FieldAddress("A", "B", "C") == FieldAddress("A", "B", "C")
    assert FieldAddress("A", "B", "C") < FieldAddress("C", "D", "E")
    assert FieldAddress("A", "B", "C", "D") < FieldAddress("C", "D", "D", "E")


def test_field_address_member_odf() -> None:
    f = FieldAddress("A", "B", "C")
    assert f.is_member_of(CollectionAddress("A", "B"))
    assert not f.is_member_of(CollectionAddress("B", "A"))
    f.is_member_of(CollectionAddress("X", "Y"))


def test_collection_address_to_string():
    address = CollectionAddress("A", "B")
    assert CollectionAddress.from_string(str(address)) == address
    assert CollectionAddress.from_string(
        "postgres_example:customer"
    ) == CollectionAddress("postgres_example", "customer")
    with pytest.raises(FidesopsException):
        CollectionAddress.from_string("A")
    with pytest.raises(FidesopsException):
        CollectionAddress.from_string("A:B:C")


def test_collection_field_map():
    c = Collection(
        name="t3",
        fields=[ScalarField(name="f1")],
    )
    assert c.field(FieldPath("f1")).name == "f1"
    assert c.field(FieldPath("not found")) is None


def test_collection_identities() -> None:
    ds = Collection(
        name="t3",
        fields=[
            ScalarField(name="f1", identity="email"),
            ScalarField(name="f2", identity="id"),
            ScalarField(name="f3"),
        ],
    )
    assert ds.identities() == {FieldPath("f1"): "email", FieldPath("f2"): "id"}


def test_collection_references() -> None:
    ds = Collection(
        name="t3",
        fields=[
            ScalarField(
                name="f1",
                references=[
                    (FieldAddress("a", "b", "c"), None),
                    (FieldAddress("a", "b", "d"), None),
                ],
            ),
            ScalarField(name="f2", references=[(FieldAddress("d", "e", "f"), None)]),
            ScalarField(name="f3"),
        ],
    )
    assert ds.references() == {
        FieldPath("f1"): [
            (FieldAddress("a", "b", "c"), None),
            (FieldAddress("a", "b", "d"), None),
        ],
        FieldPath("f2"): [(FieldAddress("d", "e", "f"), None)],
    }


def test_directional_references() -> None:
    ds = Collection(
        name="t3",
        fields=[
            ScalarField(
                name="f1",
                references=[
                    (FieldAddress("a", "b", "c"), "from"),
                    (FieldAddress("a", "b", "d"), "to"),
                ],
            ),
            ScalarField(name="f2", references=[(FieldAddress("d", "e", "f"), None)]),
            ScalarField(name="f3"),
        ],
    )
    assert ds.references() == {
        FieldPath("f1"): [
            (FieldAddress("a", "b", "c"), "from"),
            (FieldAddress("a", "b", "d"), "to"),
        ],
        FieldPath("f2"): [(FieldAddress("d", "e", "f"), None)],
    }


def test_field_key():
    assert FieldPath("a", "b").value == "a.b"
    assert FieldPath("a").keys == ("a",)
    assert FieldPath("a").prepend("b") == FieldPath("b", "a")
    assert FieldPath("a", "b") == FieldPath("a", "b")
