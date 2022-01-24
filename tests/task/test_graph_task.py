import copy
from datetime import datetime
from typing import Dict, Any

import dask
from bson import ObjectId

from fidesops.graph.config import (
    CollectionAddress,
    FieldPath,
)
from fidesops.graph.graph import DatasetGraph
from fidesops.graph.traversal import Traversal, TraversalNode
from fidesops.models.connectionconfig import ConnectionConfig, ConnectionType
from fidesops.models.datasetconfig import convert_dataset_to_graph
from fidesops.models.policy import Policy
from fidesops.schemas.dataset import FidesopsDataset
from fidesops.task.graph_task import (
    collect_queries,
    TaskResources,
    EMPTY_REQUEST,
    filter_data_categories,
    GraphTask,
)
from .traversal_data import sample_traversal, combined_mongo_postgresql_graph
from ..fixtures import example_datasets
from ..graph.graph_test_util import (
    MockSqlTask,
    MockMongoTask,
)

dask.config.set(scheduler="processes")

connection_configs = [
    ConnectionConfig(key="mysql", connection_type=ConnectionType.postgres),
    ConnectionConfig(key="postgres", connection_type=ConnectionType.postgres),
    ConnectionConfig(key="mssql", connection_type=ConnectionType.mssql)
]


def test_to_dask_input_data_scalar() -> None:
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


def test_to_dask_input_data_nested(
    integration_postgres_config, integration_mongodb_config
):

    mongo_dataset, postgres_dataset = combined_mongo_postgresql_graph(
        integration_postgres_config, integration_mongodb_config
    )
    graph = DatasetGraph(mongo_dataset, postgres_dataset)
    identity = {"email": "customer-1@example.com"}
    combined_traversal = Traversal(graph, identity)
    n = combined_traversal.traversal_node_dict[
        CollectionAddress("mongo_test", "internal_customer_profile")
    ]

    customer_feedback_data = [
        {
            "_id": ObjectId("61eb388ecfb4a3721238a39b"),
            "customer_information": {
                "email": "customer-1@example.com",
                "phone": "333-333-3333",
                "internal_customer_id": "cust_001",
            },
            "rating": 3.0,
            "date": datetime(2022, 1, 5, 0, 0),
            "message": "Product was cracked!",
        }
    ]
    task = MockMongoTask(
        n,
        TaskResources(
            EMPTY_REQUEST,
            Policy(),
            [integration_postgres_config, integration_mongodb_config],
        ),
    )

    dask_input_data = task.to_dask_input_data(customer_feedback_data)
    # Output of function returns nested keys as dot-separated where applicable.
    assert dask_input_data == {"customer_identifiers.internal_id": ["cust_001"]}


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
        copy.deepcopy(access_request_results), {"A"}, data_category_fields
    )

    assert only_a_categories == {
        "postgres_example:supplies": [
            {"foods": {"fruits": {"apples": True}}, "clothing": True}
        ]
    }

    only_b_categories = filter_data_categories(
        copy.deepcopy(access_request_results), {"B"}, data_category_fields
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
        copy.deepcopy(access_request_results), {"C"}, data_category_fields
    )
    assert only_c_categories == {
        "postgres_example:supplies": [
            {"foods": {"grains": {"rice": False, "wheat": True}}}
        ]
    }

    only_d_categories = filter_data_categories(
        copy.deepcopy(access_request_results), {"D"}, data_category_fields
    )
    assert only_d_categories == {}

    only_e_categories = filter_data_categories(
        copy.deepcopy(access_request_results), {"E"}, data_category_fields
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
