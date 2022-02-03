import os
from typing import Generator, List, Dict
from uuid import uuid4

import pytest

from sqlalchemy.orm import Session

from fidesops.db.session import get_db_engine, get_db_session
from fidesops.models.connectionconfig import AccessLevel, ConnectionType, ConnectionConfig
from fidesops.models.datasetconfig import DatasetConfig
from fidesops.schemas.connection_configuration import BigQuerySchema
from fidesops.service.connectors import BigQueryConnector, get_connector
from fixtures.application_fixtures import integration_config


@pytest.fixture(scope="function")
def bigquery_connection_config(db: Session) -> Generator:
    connection_config = ConnectionConfig.create(
        db=db,
        data={
            "name": str(uuid4()),
            "key": "my_bigquery_config",
            "connection_type": ConnectionType.bigquery,
            "access": AccessLevel.write,
        },
    )
    # Pulling from integration config file or GitHub secrets
    keyfile_creds = integration_config.get("bigquery", {}).get("keyfile_creds") or os.environ.get(
        "BIGQUERY_KEYFILE_CREDS"
    )
    dataset = integration_config.get("bigquery", {}).get(
        "dataset"
    ) or os.environ.get("BIGQUERY_DATASET")
    if keyfile_creds:
        schema = BigQuerySchema(keyfile_creds=keyfile_creds, dataset=dataset)
        connection_config.secrets = schema.dict()
        connection_config.save(db=db)

    yield connection_config
    connection_config.delete(db)


@pytest.fixture
def bigquery_example_test_dataset_config(
        connection_config: ConnectionConfig,
        db: Session,
        example_datasets: List[Dict],
) -> Generator:
    bigquery_dataset = example_datasets[6]
    fides_key = bigquery_dataset["fides_key"]
    connection_config.name = fides_key
    connection_config.key = fides_key
    connection_config.save(db=db)
    dataset = DatasetConfig.create(
        db=db,
        data={
            "connection_config_id": connection_config.id,
            "fides_key": fides_key,
            "dataset": bigquery_dataset,
        },
    )
    yield dataset
    dataset.delete(db=db)


@pytest.fixture(scope="session")
def bigquery_test_engine() -> Generator:
    """Return a connection to a Google BigQuery Warehouse"""

    connection_config = ConnectionConfig(
        name="My BigQuery Config",
        key="test_bigquery_key",
        connection_type=ConnectionType.bigquery,
    )

    # Pulling from integration config file or GitHub secrets
    keyfile_creds = integration_config.get("bigquery", {}).get("keyfile_creds") or os.environ.get(
        "BIGQUERY_KEYFILE_CREDS"
    )
    dataset = integration_config.get("bigquery", {}).get(
        "dataset"
    ) or os.environ.get("BIGQUERY_DATASET")
    if keyfile_creds:
        schema = BigQuerySchema(keyfile_creds=keyfile_creds, dataset=dataset)
        connection_config.secrets = schema.dict()

    connector: BigQueryConnector = get_connector(connection_config)
    engine = connector.client()
    bigquery_integration_session = get_db_session(engine=engine,
                                  autocommit=True,
                                  autoflush=True,
                                  )
    seed_bigquery_integration_db(bigquery_integration_session)
    yield engine
    engine.dispose()


def seed_bigquery_integration_db(bigquery_integration_session) -> None:
    """This helper only needs to be run once EVER, but just in case we need it in the future"""
    statements = [
        """
        CREATE SCHEMA test
        OPTIONS(
            description="Used to run integration tests in Fidesops",
        )
        """,
        """
        DROP TABLE IF EXISTS test.report;
        """,
        """
        DROP TABLE IF EXISTS test.service_request;
        """,
        """
        DROP TABLE IF EXISTS test.login;
        """,
        """
        DROP TABLE IF EXISTS test.visit;
        """,
        """
        DROP TABLE IF EXISTS test.order_item;
        """,
        """
        DROP TABLE IF EXISTS test.orders;
        """,
        """
        DROP TABLE IF EXISTS test.payment_card;
        """,
        """
        DROP TABLE IF EXISTS test.employee;
        """,
        """
        DROP TABLE IF EXISTS test.customer;
        """,
        """
        DROP TABLE IF EXISTS test.address;
        """,
        """
        DROP TABLE IF EXISTS test.product;

        """,
        """
        CREATE TABLE test.product (
            id INT PRIMARY KEY,
                           name CHARACTER VARYING(100),
                                          price DECIMAL(10,2)
        );
        """,
        """
        CREATE TABLE test.address (
            id BIGINT PRIMARY KEY,
                              house INT,
                                    street CHARACTER VARYING(100),
                                                     city CHARACTER VARYING(100),
                                                                    state CHARACTER VARYING(100),
                                                                                    zip CHARACTER VARYING(100)
        );
        """,
        """
        CREATE TABLE test.customer (
            id INT PRIMARY KEY,
                           email CHARACTER VARYING(100),
                                           name  CHARACTER VARYING(100),
                                                           created TIMESTAMP,
                                                                   address_id BIGINT
        );
        """,
        """
        CREATE TABLE test.employee (
            id INT PRIMARY KEY,
                           email CHARACTER VARYING(100),
                                           name CHARACTER VARYING(100),
                                                          address_id BIGINT
        );
        """,
        """
        CREATE TABLE test.payment_card (
            id CHARACTER VARYING(100) PRIMARY KEY,
                                              name CHARACTER VARYING(100),
                                                             ccn BIGINT,
                                                                 code SMALLINT,
                                                                      preferred BOOLEAN,
                                                                                customer_id INT,
                                                                                            billing_address_id BIGINT
        );
        """,
        """
        CREATE TABLE test.orders (
            id CHARACTER VARYING(100) PRIMARY KEY,
                                              customer_id INT,
                                                          shipping_address_id BIGINT,
                                                                              payment_card_id CHARACTER VARYING(100)
        );
        """,
        """
        CREATE TABLE test.order_item (
            order_id CHARACTER VARYING(100),
                               item_no SMALLINT,
                                       product_id INT,
                                                  quantity SMALLINT
        );
        """,
        """
        CREATE TABLE test.visit (
            email CHARACTER VARYING(100),
                            last_visit TIMESTAMP
        );
        """,
        """
        CREATE TABLE test.login (
            id INT PRIMARY KEY,
                           customer_id INT,
                                       time TIMESTAMP
        );
        """,
        """
        CREATE TABLE test.service_request (
            id CHARACTER VARYING(100) PRIMARY KEY,
                                              email CHARACTER VARYING(100),
                                                              alt_email CHARACTER VARYING(100),
                                                                                  opened DATE,
                                                                                         closed DATE,
                                                                                                employee_id INT
        );
        """,
        """
        CREATE TABLE test.report (
            id INT PRIMARY KEY,
                           email CHARACTER VARYING(100),
                                           name CHARACTER VARYING(100),
                                                          year INT,
                                                               month INT,
                                                                     total_visits INT
        );
        """,
        """
        INSERT INTO product VALUES
        (1, 'Example Product 1', 10.00),
        (2, 'Example Product 2', 20.00),
        (3, 'Example Product 3', 50.00);
        """,
        """
        INSERT INTO address VALUES
        (1, '123', 'Example Street', 'Exampletown', 'NY', '12345'),
        (2, '4', 'Example Lane', 'Exampletown', 'NY', '12321'),
        (3, '555', 'Example Ave', 'Example City', 'NY', '12000');
        """,
        """
        INSERT INTO customer VALUES
        (1, 'customer-1@example.com', 'John Customer', '2020-04-01 11:47:42', 1),
        (2, 'customer-2@example.com', 'Jill Customer', '2020-04-01 11:47:42', 2);
        """,
        """
        INSERT INTO employee VALUES
        (1, 'employee-1@example.com', 'Jack Employee', 3),
        (2, 'employee-2@example.com', 'Jane Employee', 3);
        """,
        """
        INSERT INTO payment_card VALUES
        ('pay_aaa-aaa', 'Example Card 1', 123456789, 321, true, 1, 1),
        ('pay_bbb-bbb', 'Example Card 2', 987654321, 123, false, 2, 1);
        """,
        """
        INSERT INTO orders VALUES
        ('ord_aaa-aaa', 1, 2, 'pay_aaa-aaa'),
        ('ord_bbb-bbb', 2, 1, 'pay_bbb-bbb'),
        ('ord_ccc-ccc', 1, 1, 'pay_aaa-aaa'),
        ('ord_ddd-ddd', 1, 1, 'pay_bbb-bbb');
        """,
        """
        INSERT INTO order_item VALUES
        ('ord_aaa-aaa', 1, 1, 1),
        ('ord_bbb-bbb', 1, 1, 1),
        ('ord_ccc-ccc', 1, 1, 1),
        ('ord_ccc-ccc', 2, 2, 1),
        ('ord_ddd-ddd', 1, 1, 1);
        """,
        """
        INSERT INTO visit VALUES
        ('customer-1@example.com', '2021-01-06 01:00:00'),
        ('customer-2@example.com', '2021-01-06 01:00:00');
        """,
        """
        INSERT INTO login VALUES
        (1, 1, '2021-01-01 01:00:00'),
        (2, 1, '2021-01-02 01:00:00'),
        (5, 1, '2021-01-05 01:00:00'),
        (6, 1, '2021-01-06 01:00:00'),
        (7, 2, '2021-01-06 01:00:00');
        """,
        """
        INSERT INTO service_request VALUES
        ('ser_aaa-aaa', 'customer-1@example.com', 'customer-1-alt@example.com', '2021-01-01', '2021-01-03', 1),
        ('ser_bbb-bbb', 'customer-2@example.com', null, '2021-01-04', null, 1),
        ('ser_ccc-ccc', 'customer-3@example.com', null, '2021-01-05', '2020-01-07', 1),
        ('ser_ddd-ddd', 'customer-3@example.com', null, '2021-05-05', '2020-05-08', 2);
        """,
        """
        INSERT INTO report VALUES
        (1, 'admin-account@example.com', 'Monthly Report', 2021, 8, 100),
        (2, 'admin-account@example.com', 'Monthly Report', 2021, 9, 100),
        (3, 'admin-account@example.com', 'Monthly Report', 2021, 10, 100),
        (4, 'admin-account@example.com', 'Monthly Report', 2021, 11, 100);
        """,
    ]
    [bigquery_integration_session.execute(stmt) for stmt in statements]
