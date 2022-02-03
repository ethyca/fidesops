import copy
import pytest
from datetime import datetime

import dask
from bson import ObjectId

from fidesops.graph.config import (
    CollectionAddress,
    FieldPath,
)
from fidesops.graph.graph import DatasetGraph
from fidesops.graph.traversal import Traversal
from fidesops.models.connectionconfig import ConnectionConfig, ConnectionType
from fidesops.models.policy import Policy
from fidesops.task.graph_task import (
    collect_queries,
    TaskResources,
    EMPTY_REQUEST,
    filter_data_categories,
)
from fidesops.util.cache import get_cache
from .traversal_data import sample_traversal, combined_mongo_postgresql_graph
from ..graph.graph_test_util import (
    MockSqlTask,
    MockMongoTask,
)

dask.config.set(scheduler="processes")

connection_configs = [
    ConnectionConfig(key="mysql", connection_type=ConnectionType.postgres),
    ConnectionConfig(key="postgres", connection_type=ConnectionType.postgres),
    ConnectionConfig(key="mssql", connection_type=ConnectionType.mssql),
]


class TestToDaskInput:
    @pytest.fixture(scope="function")
    def combined_traversal_node_dict(
        self, integration_mongodb_config, integration_postgres_config
    ):
        mongo_dataset, postgres_dataset = combined_mongo_postgresql_graph(
            integration_postgres_config, integration_mongodb_config
        )
        graph = DatasetGraph(mongo_dataset, postgres_dataset)
        identity = {"email": "customer-1@example.com"}
        combined_traversal = Traversal(graph, identity)
        return combined_traversal.traversal_node_dict

    @pytest.fixture(scope="function")
    def make_graph_task(self, integration_mongodb_config, integration_postgres_config):
        def task(node):
            return MockMongoTask(
                node,
                TaskResources(
                    EMPTY_REQUEST,
                    Policy(),
                    [integration_postgres_config, integration_mongodb_config],
                ),
            )

        return task

    def test_to_dask_input_data_scalar(self) -> None:
        t = sample_traversal()
        n = t.traversal_node_dict[CollectionAddress("mysql", "Address")]

        task = MockSqlTask(n, TaskResources(EMPTY_REQUEST, Policy(), connection_configs))
        customers_data = [
            {"contact_address_id": 31, "foo": "X"},
            {"contact_address_id": 32, "foo": "Y"},
        ]
        orders_data = [
            {"billing_address_id": 1, "shipping_address_id": 2},
            {"billing_address_id": 11, "shipping_address_id": 22},
        ]
        v = task.to_dask_input_data(customers_data, orders_data)
        assert set(v["id"]) == {31, 32, 1, 2, 11, 22}

    def test_to_dask_input_nested_identity(
        self, combined_traversal_node_dict, make_graph_task
    ):
        """
        Identity data used to locate record on nested email

        Customer feedback node has one input:
        ROOT.email -> customer_feedback.customer_information.email
        """
        node = combined_traversal_node_dict[
            CollectionAddress("mongo_test", "customer_feedback")
        ]
        root_email_input = [{"email": "customer-1@example.com"}]
        assert make_graph_task(node).to_dask_input_data(root_email_input) == {
            "customer_information.email": ["customer-1@example.com"],
        }

    def test_to_dask_input_customer_feedback_collection(
        self, combined_traversal_node_dict, make_graph_task
    ):
        """
        Nested internal_customer_id used to locate record matching nested internal_id

        Internal customer profile node has two inputs:
        ROOT.email -> internal_customer_profile.derived_emails(string[])
        customer_feedback.customer_information.internal_customer_id -> internal_customer_profile.customer_identifiers.internal_id
        """
        node = combined_traversal_node_dict[
            CollectionAddress("mongo_test", "internal_customer_profile")
        ]
        internal_customer_profile_task = make_graph_task(node)
        root_email_input = [{"email": "customer-1@example.com"}]
        customer_feedback_input = [
            {
                "_id": ObjectId("61eb388ecfb4a3721238a39b"),
                "customer_information": {
                    "email": "customer-1@example.com",
                    "phone": "333-333-3333",
                    "internal_customer_id": "cust_001",
                },
            }
        ]

        assert internal_customer_profile_task.to_dask_input_data(
            root_email_input, customer_feedback_input
        ) == {
            "customer_identifiers.derived_emails": ["customer-1@example.com"],
            "customer_identifiers.internal_id": ["cust_001"],
        }

    def test_to_dask_input_flights_collection(
        self, make_graph_task, combined_traversal_node_dict
    ):
        """
        Array of strings used to locate record with matching value in nested array of strings

        Flights node has one input:
        mongo_test.customer_details.travel_identifiers -> mongo_test.passenger_information.passenger_ids
        """
        node = combined_traversal_node_dict[CollectionAddress("mongo_test", "flights")]
        task = make_graph_task(node)
        truncated_customer_details_output = [
            {
                "_id": ObjectId("61f422e0ddc2559e0c300e95"),
                "travel_identifiers": ["A111-11111", "B111-11111"],
            },
            {
                "_id": ObjectId("61f422e0ddc2559e0c300e95"),
                "travel_identifiers": ["C111-11111"],
            }
        ]
        assert task.to_dask_input_data(truncated_customer_details_output) == {
            "passenger_information.passenger_ids": ["A111-11111", "B111-11111", "C111-11111"],
        }

    def test_to_dask_input_aircraft_collection(
        self, make_graph_task, combined_traversal_node_dict
    ):
        """
        Integer used to locate record with matching value in array of integers

        Aircraft node has one input:
        mongo_test:flights.plane -> mongo_test:aircraft.planes
        """
        node = combined_traversal_node_dict[CollectionAddress("mongo_test", "aircraft")]
        task = make_graph_task(node)
        truncated_flights_output = [
            {"pilots": ["1", "2"], "plane": 10002.0},
            {"pilots": ["3", "4"], "plane": 101010},
        ]
        assert task.to_dask_input_data(truncated_flights_output) == {
            "planes": [10002, 101010],
        }

    def test_to_dask_input_employee_collection(
        self, make_graph_task, combined_traversal_node_dict
    ):
        """
        Array of integers used to locate record with matching integer

        Mongo employee node has two inputs:
        root.email -> mongo_test.employee.email
        mongo_test.flights.pilots -> mongo_test.employee.id
        """
        node = combined_traversal_node_dict[CollectionAddress("mongo_test", "employee")]
        task = make_graph_task(node)
        root_email_input = [{"email": "customer-1@example.com"}]
        truncated_flights_output = [
            {"pilots": ["1", "2"], "plane": 10002.0},
            {"pilots": ["3", "4"], "plane": 101010},
        ]
        assert task.to_dask_input_data(root_email_input, truncated_flights_output) == {
            "id": ["1", "2", "3", "4"],
            "email": ["customer-1@example.com"],
        }

    def test_to_dask_input_conversation_collection(
        self, make_graph_task, combined_traversal_node_dict
    ):
        """
        Array of objects of strings used to locate record within array of objects of scalars

        Mongo conversation node has one input:
        mongo_test:customer_details.comments.comment_id -> mongo_test:conversations.thread.comment
        """
        node = combined_traversal_node_dict[
            CollectionAddress("mongo_test", "conversations")
        ]
        task = make_graph_task(node)
        truncated_customer_details_output = [
            {
                "comments": [
                    {"comment_id": "com_0001"},
                    {"comment_id": "com_0003"},
                    {"comment_id": "com_0005"},
                ]
            },
            {"comments": [{"comment_id": "com_0007"}]},
        ]

        assert task.to_dask_input_data(truncated_customer_details_output) == {
            "thread.comment": ["com_0001", "com_0003", "com_0005", "com_0007"],
        }


def test_sql_dry_run_queries() -> None:
    traversal = sample_traversal()
    env = collect_queries(
        traversal,
        TaskResources(EMPTY_REQUEST, Policy(), connection_configs),
    )

    assert (
        env[CollectionAddress("mysql", "Customer")]
        == "SELECT customer_id,name,email,contact_address_id FROM Customer WHERE email = ?"
    )

    assert (
        env[CollectionAddress("mysql", "User")]
        == "SELECT id,user_id,name FROM User WHERE user_id = ?"
    )

    assert (
        env[CollectionAddress("postgres", "Order")]
        == "SELECT order_id,customer_id,shipping_address_id,billing_address_id FROM Order WHERE customer_id IN (?, ?)"
    )

    assert (
        env[CollectionAddress("mysql", "Address")]
        == "SELECT id,street,city,state,zip FROM Address WHERE id IN (?, ?)"
    )

    assert (
        env[CollectionAddress("mssql", "Address")]
        == "SELECT id,street,city,state,zip FROM Address WHERE id IN (:id_in_stmt_generated_0, :id_in_stmt_generated_1)"
    )


def test_mongo_dry_run_queries() -> None:
    from .traversal_data import integration_db_graph

    traversal = Traversal(integration_db_graph("postgres"), {"email": ["x"]})
    env = collect_queries(
        traversal,
        TaskResources(
            EMPTY_REQUEST,
            Policy(),
            [
                ConnectionConfig(key="mysql", connection_type=ConnectionType.mongodb),
                ConnectionConfig(
                    key="postgres", connection_type=ConnectionType.mongodb
                ),
            ],
        ),
    )

    assert (
        env[CollectionAddress("postgres", "customer")]
        == "db.postgres.customer.find({'email': ?}, {'id': 1, 'name': 1, 'email': 1, 'address_id': 1})"
    )

    assert (
        env[CollectionAddress("postgres", "orders")]
        == "db.postgres.orders.find({'customer_id': {'$in': [?, ?]}}, {'id': 1, 'customer_id': 1, 'shipping_address_id': 1, 'payment_card_id': 1})"
    )

    assert (
        env[CollectionAddress("postgres", "address")]
        == "db.postgres.address.find({'id': {'$in': [?, ?]}}, {'id': 1, 'street': 1, 'city': 1, 'state': 1, 'zip': 1})"
    )


def cache_input_helper(privacy_request_id, collection_address_str, value):
    """Test helper for caching input data into a collection for a given privacy request in Redis"""
    cache = get_cache()
    key = f"INPUT__{privacy_request_id}__access_request__{collection_address_str}"
    cache.set_encoded_object(key, value)


def test_filter_data_categories():
    """Test different combinations of data categories to ensure the access_request_results are filtered properly"""
    access_request_results = {
        "postgres_example:supplies": [
            {
                "foods": {
                    "vegetables": True,
                    "fruits": {
                        "apples": True,
                        "oranges": False,
                        "berries": {"strawberries": True, "blueberries": False},
                    },
                    "grains": {"rice": False, "wheat": True},
                },
                "clothing": True,
            }
        ]
    }

    data_category_fields = {
        CollectionAddress("postgres_example", "supplies"): {
            "A": [FieldPath("foods", "fruits", "apples"), FieldPath("clothing")],
            "B": [FieldPath("foods", "vegetables")],
            "C": [
                FieldPath("foods", "grains", "rice"),
                FieldPath("foods", "grains", "wheat"),
            ],
            "D": [],
            "E": [
                FieldPath("foods", "fruits", "berries", "strawberries"),
                FieldPath("foods", "fruits", "oranges"),
            ],
        }
    }

    only_a_categories = filter_data_categories(
        copy.deepcopy(access_request_results), {"A"}, data_category_fields, "test_id"
    )

    assert only_a_categories == {
        "postgres_example:supplies": [
            {"foods": {"fruits": {"apples": True}}, "clothing": True}
        ]
    }

    only_b_categories = filter_data_categories(
        copy.deepcopy(access_request_results), {"B"}, data_category_fields, "test_id"
    )
    assert only_b_categories == {
        "postgres_example:supplies": [
            {
                "foods": {
                    "vegetables": True,
                }
            }
        ]
    }

    only_c_categories = filter_data_categories(
        copy.deepcopy(access_request_results), {"C"}, data_category_fields, "test_id"
    )
    assert only_c_categories == {
        "postgres_example:supplies": [
            {"foods": {"grains": {"rice": False, "wheat": True}}}
        ]
    }

    only_d_categories = filter_data_categories(
        copy.deepcopy(access_request_results), {"D"}, data_category_fields, "test_id"
    )
    assert only_d_categories == {}

    only_e_categories = filter_data_categories(
        copy.deepcopy(access_request_results), {"E"}, data_category_fields, "test_id"
    )
    assert only_e_categories == {
        "postgres_example:supplies": [
            {
                "foods": {
                    "fruits": {
                        "oranges": False,
                        "berries": {"strawberries": True},
                    }
                }
            }
        ]
    }


def test_filter_data_categories_arrays():
    access_request_results = {
        "postgres_example:flights": [
            {
                "people": {
                    "passenger_ids": [222, 445, 311, 4444],
                    "pilot_ids": [123, 12, 112],
                },
                "flight_number": 101,
            }
        ]
    }

    data_category_fields = {
        CollectionAddress("postgres_example", "flights"): {
            "A": [FieldPath("people", "passenger_ids")],
            "B": [FieldPath("people", "pilot_ids")],
        }
    }

    only_a_category = filter_data_categories(
        copy.deepcopy(access_request_results), {"A"}, data_category_fields, "test_id"
    )

    # Nested array field retrieved
    assert only_a_category == {
        "postgres_example:flights": [
            {"people": {"passenger_ids": [222, 445, 311, 4444]}}
        ]
    }

    # Only matching cached value in nested array retrieved
    cache_input_helper(
        privacy_request_id="test_id",
        collection_address_str="postgres_example:flights",
        value={"people.pilot_ids": [112]},
    )
    only_b_category = filter_data_categories(
        copy.deepcopy(access_request_results), {"B"}, data_category_fields, "test_id"
    )
    assert only_b_category == {
        "postgres_example:flights": [{"people": {"pilot_ids": [112]}}]
    }


def test_filter_data_categories_limited_results():
    """
    Test scenario where the related data for a given identity is only a small subset of all the annotated fields.
    """
    jane_results = {
        "mongo_test:customer_details": [
            {
                "_id": ObjectId("61f2bc8d6362fd78d72d8791"),
                "customer_id": 3.0,
                "gender": "female",
                "birthday": datetime(1990, 2, 28, 0, 0),
            }
        ],
        "postgres_example:order_item": [],
        "postgres_example:report": [],
        "postgres_example:orders": [
            {"customer_id": 3, "id": "ord_ddd-eee", "shipping_address_id": 4}
        ],
        "postgres_example:employee": [],
        "postgres_example:address": [
            {
                "city": "Example Mountain",
                "house": 1111,
                "id": 4,
                "state": "TX",
                "street": "Example Place",
                "zip": "54321",
            }
        ],
        "postgres_example:visit": [],
        "postgres_example:product": [],
        "postgres_example:customer": [
            {
                "address_id": 4,
                "created": datetime(2020, 4, 1, 11, 47, 42),
                "email": "jane@example.com",
                "id": 3,
                "name": "Jane Customer",
            }
        ],
        "postgres_example:service_request": [],
        "postgres_example:payment_card": [
            {
                "billing_address_id": 4,
                "ccn": 373719391,
                "code": 222,
                "customer_id": 3,
                "id": "pay_ccc-ccc",
                "name": "Example Card 3",
                "preferred": False,
            }
        ],
        "mongo_test:customer_feedback": [],
        "postgres_example:login": [
            {"customer_id": 3, "id": 8, "time": datetime(2021, 1, 6, 1, 0)}
        ],
        "mongo_test:internal_customer_profile": [],
    }

    target_categories = {"user.provided.identifiable"}

    data_category_fields = {
        CollectionAddress.from_string("postgres_example:address"): {
            "user.provided.identifiable.contact.city": [
                FieldPath(
                    "city",
                )
            ],
            "user.provided.identifiable.contact.street": [
                FieldPath(
                    "house",
                ),
                FieldPath(
                    "street",
                ),
            ],
            "system.operations": [
                FieldPath(
                    "id",
                )
            ],
            "user.provided.identifiable.contact.state": [
                FieldPath(
                    "state",
                )
            ],
            "user.provided.identifiable.contact.postal_code": [
                FieldPath(
                    "zip",
                )
            ],
        },
        CollectionAddress.from_string("postgres_example:customer"): {
            "system.operations": [
                FieldPath(
                    "address_id",
                ),
                FieldPath(
                    "created",
                ),
            ],
            "user.provided.identifiable.contact.email": [
                FieldPath(
                    "email",
                )
            ],
            "user.derived.identifiable.unique_id": [
                FieldPath(
                    "id",
                )
            ],
            "user.provided.identifiable.name": [
                FieldPath(
                    "name",
                )
            ],
        },
        CollectionAddress.from_string("postgres_example:employee"): {
            "system.operations": [
                FieldPath(
                    "address_id",
                )
            ],
            "user.provided.identifiable.contact.email": [
                FieldPath(
                    "email",
                )
            ],
            "user.derived.identifiable.unique_id": [
                FieldPath(
                    "id",
                )
            ],
            "user.provided.identifiable.name": [
                FieldPath(
                    "name",
                )
            ],
        },
        CollectionAddress.from_string("postgres_example:login"): {
            "user.derived.identifiable.unique_id": [
                FieldPath(
                    "customer_id",
                )
            ],
            "system.operations": [
                FieldPath(
                    "id",
                )
            ],
            "user.derived.nonidentifiable.sensor": [
                FieldPath(
                    "time",
                )
            ],
        },
        CollectionAddress.from_string("postgres_example:order_item"): {
            "system.operations": [
                FieldPath(
                    "order_id",
                ),
                FieldPath(
                    "product_id",
                ),
                FieldPath(
                    "quantity",
                ),
            ]
        },
        CollectionAddress.from_string("postgres_example:orders"): {
            "user.derived.identifiable.unique_id": [
                FieldPath(
                    "customer_id",
                )
            ],
            "system.operations": [
                FieldPath(
                    "id",
                ),
                FieldPath(
                    "shipping_address_id",
                ),
            ],
        },
        CollectionAddress.from_string("postgres_example:payment_card"): {
            "system.operations": [
                FieldPath(
                    "billing_address_id",
                ),
                FieldPath(
                    "id",
                ),
            ],
            "user.provided.identifiable.financial.account_number": [
                FieldPath(
                    "ccn",
                )
            ],
            "user.provided.identifiable.financial": [
                FieldPath(
                    "code",
                ),
                FieldPath(
                    "name",
                ),
            ],
            "user.derived.identifiable.unique_id": [
                FieldPath(
                    "customer_id",
                )
            ],
            "user.provided.nonidentifiable": [
                FieldPath(
                    "preferred",
                )
            ],
        },
        CollectionAddress.from_string("postgres_example:product"): {
            "system.operations": [
                FieldPath(
                    "id",
                ),
                FieldPath(
                    "name",
                ),
                FieldPath(
                    "price",
                ),
            ]
        },
        CollectionAddress.from_string("postgres_example:report"): {
            "user.provided.identifiable.contact.email": [
                FieldPath(
                    "email",
                )
            ],
            "system.operations": [
                FieldPath(
                    "id",
                ),
                FieldPath(
                    "month",
                ),
                FieldPath(
                    "name",
                ),
                FieldPath(
                    "total_visits",
                ),
                FieldPath(
                    "year",
                ),
            ],
        },
        CollectionAddress.from_string("postgres_example:service_request"): {
            "user.provided.identifiable.contact.email": [
                FieldPath(
                    "alt_email",
                )
            ],
            "system.operations": [
                FieldPath(
                    "closed",
                ),
                FieldPath(
                    "email",
                ),
                FieldPath(
                    "id",
                ),
                FieldPath(
                    "opened",
                ),
            ],
            "user.derived.identifiable.unique_id": [
                FieldPath(
                    "employee_id",
                )
            ],
        },
        CollectionAddress.from_string("postgres_example:visit"): {
            "user.provided.identifiable.contact.email": [
                FieldPath(
                    "email",
                )
            ],
            "system.operations": [
                FieldPath(
                    "last_visit",
                )
            ],
        },
        CollectionAddress.from_string("mongo_test:customer_details"): {
            "system.operations": [
                FieldPath(
                    "_id",
                )
            ],
            "user.provided.identifiable.date_of_birth": [
                FieldPath(
                    "birthday",
                )
            ],
            "user.derived.identifiable.unique_id": [
                FieldPath(
                    "customer_id",
                )
            ],
            "user.provided.identifiable.gender": [
                FieldPath(
                    "gender",
                )
            ],
            "user.provided.identifiable.job_title": [
                FieldPath("workplace_info", "position")
            ],
        },
        CollectionAddress.from_string("mongo_test:customer_feedback"): {
            "system.operations": [
                FieldPath(
                    "_id",
                )
            ],
            "user.provided.identifiable.contact.phone_number": [
                FieldPath("customer_information", "phone")
            ],
            "user.provided.nonidentifiable": [
                FieldPath(
                    "message",
                ),
                FieldPath(
                    "rating",
                ),
            ],
        },
        CollectionAddress.from_string("mongo_test:internal_customer_profile"): {
            "user.derived": [
                FieldPath(
                    "derived_interests",
                )
            ]
        },
    }

    filtered_results = filter_data_categories(
        copy.deepcopy(jane_results), target_categories, data_category_fields, "test_id"
    )

    assert filtered_results == {
        "mongo_test:customer_details": [
            {"gender": "female", "birthday": datetime(1990, 2, 28)}
        ],
        "postgres_example:address": [
            {
                "city": "Example Mountain",
                "house": 1111,
                "state": "TX",
                "street": "Example Place",
                "zip": "54321",
            }
        ],
        "postgres_example:customer": [
            {"email": "jane@example.com", "name": "Jane Customer"}
        ],
        "postgres_example:payment_card": [
            {"ccn": 373719391, "code": 222, "name": "Example Card 3"}
        ],
    }
