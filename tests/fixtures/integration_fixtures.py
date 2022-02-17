import logging
import random
from datetime import datetime
from typing import Dict, Any, List
from uuid import uuid4

import pytest
from pymongo import MongoClient
from sqlalchemy import text
from sqlalchemy.engine import Engine

from fidesops.models.connectionconfig import (
    ConnectionConfig,
    ConnectionType,
    AccessLevel,
)
from fidesops.service.connectors import PostgreSQLConnector, MongoDBConnector
from .application_fixtures import faker, integration_secrets

logger = logging.getLogger(__name__)


def generate_integration_records():
    return {
        "customer": [
            {
                "id": 10000,
                "email": "test_one@example.com",
                "name": faker.name(),
                "address_id": 1000,
            },
            {
                "id": 10001,
                "email": "test_two@example.com",
                "name": faker.name(),
                "address_id": 1001,
            },
            {
                "id": 10002,
                "email": "test_three@example.com",
                "name": faker.name(),
                "address_id": 1002,
            },
        ],
        "orders": [
            {
                "id": "test_order_id_10000",
                "customer_id": 10000,
                "payment_card_id": "test_payment_card_1000",
                "shipping_address_id": 1002,
            },
            {
                "id": "test_order_id_10001",
                "customer_id": 10001,
                "payment_card_id": uuid4(),
                "shipping_address_id": 1002,
            },
            {
                "id": "test_order_id_10002",
                "customer_id": 10002,
                "payment_card_id": uuid4(),
                "shipping_address_id": 1002,
            },
        ],
        "payment_card": [
            {
                "id": "test_payment_card_1001",
                "name": faker.name(),
                "ccn": random.randint(10000, 1000000000),
                "billing_address_id": 10001,
            },
            {
                "id": "test_payment_card_1002",
                "name": faker.name(),
                "ccn": random.randint(10000, 1000000000),
                "billing_address_id": 10002,
            },
        ],
        "address": [
            {
                "id": 1000,
                "street": faker.street_address(),
                "city": faker.city(),
                "state": faker.state(),
                "zip": faker.zipcode(),
            },
            {
                "id": 1001,
                "street": faker.street_address(),
                "city": faker.city(),
                "state": faker.state(),
                "zip": faker.zipcode(),
            },
            {
                "id": 1002,
                "street": faker.street_address(),
                "city": faker.city(),
                "state": faker.state(),
                "zip": faker.zipcode(),
            },
        ],
    }


# ======================= postgres ==========================


@pytest.fixture(scope="function")
def integration_postgres_config(postgres_inserts) -> ConnectionConfig:
    return ConnectionConfig(
        name="postgres_test",
        key="postgres_example",
        connection_type=ConnectionType.postgres,
        access=AccessLevel.write,
        secrets=integration_secrets["postgres_example"],
    )


def sql_insert(engine: Engine, table_name: str, record: Dict[str, Any]) -> None:
    fields = record.keys()
    value_keys = [f":{k}" for k in fields]
    insert_str = f"INSERT INTO {table_name} ({','.join(fields)}) VALUES ({ ','.join(value_keys)})"
    text_clause = text(insert_str)
    with engine.connect() as connection:
        connection.execute(text_clause, record)


def sql_delete(engine: Engine, table_name: str, ids: List[Any]) -> None:
    delete_str = f"DELETE FROM {table_name} where id in {tuple(ids)}"
    with engine.connect() as connection:
        connection.execute(delete_str)


@pytest.fixture(scope="function")
def postgres_inserts(postgres_integration_db):
    integration_postgres_db_engine = postgres_integration_db.bind
    records = generate_integration_records()
    for table_name, record_list in records.items():
        for record in record_list:
            sql_insert(integration_postgres_db_engine, table_name, record)
    yield records
    for table_name, record_list in records.items():
        sql_delete(
            integration_postgres_db_engine, table_name, [r["id"] for r in record_list]
        )


# ======================= mongodb  ==========================


@pytest.fixture(scope="session")
def integration_mongodb_config() -> ConnectionConfig:
    return ConnectionConfig(
        key="mongo_example",
        connection_type=ConnectionType.mongodb,
        access=AccessLevel.write,
        secrets=integration_secrets["mongo_example"],
    )


@pytest.fixture(scope="session")
def integration_mongodb_connector(integration_mongodb_config) -> MongoClient:
    return MongoDBConnector(integration_mongodb_config).client()


def mongo_insert(
    client: MongoClient, db_name: str, collection_name: str, record: Dict[str, Any]
) -> None:
    db = client[db_name]
    collection = db[collection_name]
    return collection.insert_one(record).inserted_id


def mongo_delete(
    client: MongoClient,
    db_name: str,
    collection_name: str,
    records: List[Dict[str, Any]],
) -> None:
    """Deletion in the context of this test. This deletion is not using the mongo _id fields,
    since those are generated at the time of the test."""

    db = client[db_name]
    collection = db[collection_name]
    return collection.delete_many({"id": {"$in": [record["id"] for record in records]}})


def generate_mongo_specific_records():
    """These records are generated for mongo erasure tests where we mask some of the data as part of the test"""
    return {
        "customer_details": [
            {
                "id": "001",
                "customer_id": 10000,
                "gender": "male",
                "birthday": datetime(1988, 1, 10),
                "workplace_info": {
                    "employer": "Mountain Baking Company",
                    "position": "Chief Strategist",
                },
            },
            {
                "id": "002",
                "customer_id": 10001,
                "gender": "female",
                "birthday": datetime(1985, 3, 5),
                "workplace_info": {
                    "employer": "Incline Software Company",
                    "position": "Software Engineer",
                },
            },
            {
                "id": "003",
                "customer_id": 10002,
                "gender": "female",
                "birthday": datetime(1990, 2, 28),
            },
        ],
        "customer_feedback": [
            {
                "id": "feed_1",
                "customer_information": {
                    "email": "test_one@example.com",
                    "phone": "333-333-3333",
                    "internal_customer_id": "cust_004",
                },
                "rating": 3,
                "date": datetime(2022, 1, 5),
                "message": "Customer service wait times have increased to over an hour.",
            },
            {
                "id": "feed_2",
                "customer_information": {
                    "email": "test_two@example.com",
                    "phone": "111-111-1111",
                    "internal_customer_id": "cust_005",
                },
                "rating": 5,
                "date": datetime(2022, 1, 10),
                "message": "Customer service rep was very helpful and answered all my questions.",
            },
        ],
        "internal_customer_profile": [
            {
                "id": "prof_1",
                "customer_identifiers": {"internal_id": "cust_004"},
                "derived_interests": ["marketing", "food"],
            },
            {
                "id": "prof_2",
                "customer_identifiers": {"internal_id": "cust_005"},
                "derived_interests": ["programming", "hiking", "skateboarding"],
            },
        ],
    }


@pytest.fixture(scope="function")
def mongo_inserts(integration_mongodb_connector):
    records = generate_integration_records()
    records.update(generate_mongo_specific_records())
    for table_name, record_list in records.items():
        mongo_delete(
            integration_mongodb_connector, "mongo_test", table_name, record_list
        )

    for table_name, record_list in records.items():
        for record in record_list:
            mongo_insert(
                integration_mongodb_connector, "mongo_test", table_name, record
            )
    yield records
