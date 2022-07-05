from tests.test_helpers.dataset_utils import generate_collections, generate_dataset


class TestGenerateCollections:
    def test_empty_values(self):
        api_data = {"user": [{"a": None, "b": "", "c": [], "d": {}}]}
        assert generate_collections(api_data) == [
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
        api_data = {"user": [{"active": True}]}
        assert generate_collections(api_data) == [
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
        api_data = {"user": [{"active": False}]}
        assert generate_collections(api_data) == [
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
        api_data = {"user": [{"id": 1}]}
        assert generate_collections(api_data) == [
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
        api_data = {"user": [{"id": 0}]}
        assert generate_collections(api_data) == [
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
        api_data = {"user": [{"balance": 2.0}]}
        assert generate_collections(api_data) == [
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
        api_data = {"user": [{"balance": 0.0}]}
        assert generate_collections(api_data) == [
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
        api_data = {"user": [{"first_name": "test"}]}
        assert generate_collections(api_data) == [
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
        api_data = {
            "user": [{"address": {"street1": "123 Fake St.", "city": "Springfield"}}]
        }
        assert generate_collections(api_data) == [
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
        api_data = {"user": [{"ids": [1]}]}
        assert generate_collections(api_data) == [
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
        api_data = {"user": [{"times": [2.0]}]}
        assert generate_collections(api_data) == [
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
        api_data = {"user": [{"names": ["first last"]}]}
        assert generate_collections(api_data) == [
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
        api_data = {
            "user": [
                {
                    "bank_accounts": [
                        {"bank_name": "Wells Fargo", "status": "active"},
                        {"bank_name": "Schools First", "status": "active"},
                    ]
                }
            ]
        }
        assert generate_collections(api_data) == [
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


class TestGenerateDataset:
    def test_dataset_merge(self):
        existing_dataset = {
            "fides_key": "example",
            "name": "Example Dataset",
            "description": "An example dataset",
            "collections": [
                {
                    "name": "user",
                    "fields": [
                        {
                            "name": "a",
                            "data_categories": ["user.provided"],
                            "fidesops_meta": {"data_type": "string"},
                        }
                    ],
                }
            ],
        }
        api_data = {"user": [{"a": None, "b": "", "c": [], "d": {}}]}

        generated_dataset = generate_dataset(existing_dataset, api_data)

        assert generated_dataset == {
            "fides_key": "example",
            "name": "Example Dataset",
            "description": "An example dataset",
            "collections": [
                {
                    "name": "user",
                    "fields": [
                        {
                            "name": "a",
                            "data_categories": ["user.provided"],
                            "fidesops_meta": {"data_type": "string"},
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
            ],
        }

    def test_empty_values(self):
        existing_dataset = {
            "fides_key": "example",
            "name": "Example Dataset",
            "description": "An example dataset",
            "collections": [
                {
                    "name": "user",
                    "fields": [
                        {
                            "name": "a",
                            "data_categories": ["user.provided"],
                            "fidesops_meta": {"data_type": "string"},
                        }
                    ],
                }
            ],
        }
        api_data = {"user": [{"a": None, "b": "", "c": [], "d": {}}]}

        assert generate_dataset(existing_dataset, api_data) == {
            "fides_key": "example",
            "name": "Example Dataset",
            "description": "An example dataset",
            "collections": [
                {
                    "name": "user",
                    "fields": [
                        {
                            "name": "a",
                            "data_categories": ["user.provided"],
                            "fidesops_meta": {"data_type": "string"},
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
            ],
        }
