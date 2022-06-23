from fidesops.graph.config import Collection, Field, ScalarField
from fidesops.graph.data_type import IntTypeConverter, StringTypeConverter
from tests.test_helpers.dataset_utils import generate_collections


class TestGenerateCollections:
    def test_empty_values(self):
        response = {"example:user": [{"a": None, "b": "", "c": [], "d": {}}]}
        assert generate_collections("example", response, {}) == [
            {
                "name": "user",
                "fields": [
                    {"name": "a", "data_categories": ["system.operations"]},
                    {"name": "b", "data_categories": ["system.operations"]},
                    {"name": "c", "data_categories": ["system.operations"]},
                    {"name": "d", "data_categories": ["system.operations"]},
                ],
            }
        ]

    def test_boolean_true(self):
        response = {"example:user": [{"active": True}]}
        assert generate_collections("example", response, {}) == [
            {
                "name": "user",
                "fields": [
                    {
                        "name": "active",
                        "data_categories": ["system.operations"],
                        "fidesops_meta": {"data_type": "boolean"},
                    }
                ],
            }
        ]

    def test_boolean_false(self):
        response = {"example:user": [{"active": False}]}
        assert generate_collections("example", response, {}) == [
            {
                "name": "user",
                "fields": [
                    {
                        "name": "active",
                        "data_categories": ["system.operations"],
                        "fidesops_meta": {"data_type": "boolean"},
                    }
                ],
            }
        ]

    def test_integer(self):
        response = {"example:user": [{"id": 1}]}
        assert generate_collections("example", response, {}) == [
            {
                "name": "user",
                "fields": [
                    {
                        "name": "id",
                        "data_categories": ["system.operations"],
                        "fidesops_meta": {"data_type": "integer"},
                    }
                ],
            }
        ]

    def test_zero(self):
        response = {"example:user": [{"id": 0}]}
        assert generate_collections("example", response, {}) == [
            {
                "name": "user",
                "fields": [
                    {
                        "name": "id",
                        "data_categories": ["system.operations"],
                        "fidesops_meta": {"data_type": "integer"},
                    }
                ],
            }
        ]

    def test_float(self):
        response = {"example:user": [{"balance": 2.0}]}
        assert generate_collections("example", response, {}) == [
            {
                "name": "user",
                "fields": [
                    {
                        "name": "balance",
                        "data_categories": ["system.operations"],
                        "fidesops_meta": {"data_type": "float"},
                    }
                ],
            }
        ]

    def test_float_zero(self):
        response = {"example:user": [{"balance": 0.0}]}
        assert generate_collections("example", response, {}) == [
            {
                "name": "user",
                "fields": [
                    {
                        "name": "balance",
                        "data_categories": ["system.operations"],
                        "fidesops_meta": {"data_type": "float"},
                    }
                ],
            }
        ]

    def test_string(self):
        response = {"example:user": [{"first_name": "test"}]}
        assert generate_collections("example", response, {}) == [
            {
                "name": "user",
                "fields": [
                    {
                        "name": "first_name",
                        "data_categories": ["system.operations"],
                        "fidesops_meta": {"data_type": "string"},
                    }
                ],
            }
        ]

    def test_object(self):
        response = {
            "example:user": [
                {"address": {"street1": "123 Fake St.", "city": "Springfield"}}
            ]
        }
        assert generate_collections("example", response, {}) == [
            {
                "name": "user",
                "fields": [
                    {
                        "name": "address",
                        "fidesops_meta": {"data_type": "object"},
                        "fields": [
                            {
                                "name": "street1",
                                "data_categories": ["system.operations"],
                                "fidesops_meta": {"data_type": "string"},
                            },
                            {
                                "name": "city",
                                "data_categories": ["system.operations"],
                                "fidesops_meta": {"data_type": "string"},
                            },
                        ],
                    }
                ],
            }
        ]

    def test_integer_list(self):
        response = {"example:user": [{"ids": [1]}]}
        assert generate_collections("example", response, {}) == [
            {
                "name": "user",
                "fields": [
                    {
                        "name": "ids",
                        "data_categories": ["system.operations"],
                        "fidesops_meta": {"data_type": "integer[]"},
                    }
                ],
            }
        ]

    def test_float_list(self):
        response = {"example:user": [{"times": [2.0]}]}
        assert generate_collections("example", response, {}) == [
            {
                "name": "user",
                "fields": [
                    {
                        "name": "times",
                        "data_categories": ["system.operations"],
                        "fidesops_meta": {"data_type": "float[]"},
                    }
                ],
            }
        ]

    def test_string_list(self):
        response = {"example:user": [{"names": ["first last"]}]}
        assert generate_collections("example", response, {}) == [
            {
                "name": "user",
                "fields": [
                    {
                        "name": "names",
                        "data_categories": ["system.operations"],
                        "fidesops_meta": {"data_type": "string[]"},
                    }
                ],
            }
        ]

    def test_object_list(self):
        response = {
            "example:user": [
                {
                    "bank_accounts": [
                        {"bank_name": "Wells Fargo", "status": "active"},
                        {"bank_name": "Schools First", "status": "active"},
                    ]
                }
            ]
        }
        assert generate_collections("example", response, {}) == [
            {
                "name": "user",
                "fields": [
                    {
                        "name": "bank_accounts",
                        "fidesops_meta": {"data_type": "object[]"},
                        "fields": [
                            {
                                "name": "bank_name",
                                "data_categories": ["system.operations"],
                                "fidesops_meta": {"data_type": "string"},
                            },
                            {
                                "name": "status",
                                "data_categories": ["system.operations"],
                                "fidesops_meta": {"data_type": "string"},
                            },
                        ],
                    }
                ],
            }
        ]


class TestMergeCollections:
    def test_empty_values(self):
        response = {"example:user": [{"a": None, "b": "", "c": [], "d": {}}]}
        existing_collection = {
            "user": Collection(
                name="user",
                fields=[
                    ScalarField(
                        name="a",
                        data_categories=["user.provided"],
                        data_type_converter=IntTypeConverter(),
                    )
                ],
            )
        }
        assert generate_collections("example", response, existing_collection) == [
            {
                "name": "user",
                "fields": [
                    {
                        "name": "a",
                        "data_categories": ["user.provided"],
                        "fidesops_meta": {"data_type": "integer"},
                    },
                    {
                        "name": "b",
                        "data_categories": ["system.operations"],
                    },
                    {
                        "name": "c",
                        "data_categories": ["system.operations"],
                    },
                    {"name": "d", "data_categories": ["system.operations"]},
                ],
            }
        ]
