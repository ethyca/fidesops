import logging
import pytest
from typing import Dict, Generator, List
from uuid import uuid4

from sqlalchemy.orm import Session

from fidesops.db.session import get_db_session, get_db_engine
from fidesops.models.connectionconfig import (
    ConnectionConfig,
    AccessLevel,
    ConnectionType,
)
from fidesops.models.datasetconfig import DatasetConfig
from fidesops.models.policy import ActionType
from fidesops.models.privacy_request import (
    ExecutionLog,
    ExecutionLogStatus,
    PrivacyRequest,
)
from fidesops.service.connectors import PostgreSQLConnector

from .application_fixtures import integration_secrets

logger = logging.getLogger(__name__)


@pytest.fixture
def postgres_example_test_dataset_config(
    connection_config: ConnectionConfig,
    db: Session,
    example_datasets: List[Dict],
) -> Generator:
    postgres_dataset = example_datasets[0]
    fides_key = postgres_dataset["fides_key"]
    connection_config.name = fides_key
    connection_config.key = fides_key
    connection_config.save(db=db)
    dataset = DatasetConfig.create(
        db=db,
        data={
            "connection_config_id": connection_config.id,
            "fides_key": fides_key,
            "dataset": postgres_dataset,
        },
    )
    yield dataset
    dataset.delete(db=db)


@pytest.fixture
def postgres_example_test_dataset_config_read_access(
    read_connection_config: ConnectionConfig,
    db: Session,
    example_datasets: List[Dict],
) -> Generator:
    postgres_dataset = example_datasets[0]
    fides_key = postgres_dataset["fides_key"]
    dataset = DatasetConfig.create(
        db=db,
        data={
            "connection_config_id": read_connection_config.id,
            "fides_key": fides_key,
            "dataset": postgres_dataset,
        },
    )
    yield dataset
    dataset.delete(db=db)


@pytest.fixture(scope="function")
def postgres_execution_log(
    db: Session,
    privacy_request: PrivacyRequest,
) -> ExecutionLog:
    el = ExecutionLog.create(
        db=db,
        data={
            "dataset_name": "my-postgres-db",
            "collection_name": "user",
            "fields_affected": [
                {
                    "path": "my-postgres-db:user:email",
                    "field_name": "email",
                    "data_categories": ["user.provided.identifiable.contact.email"],
                }
            ],
            "action_type": ActionType.access,
            "status": ExecutionLogStatus.pending,
            "privacy_request_id": privacy_request.id,
        },
    )
    yield el
    el.delete(db)


# TODO: Consolidate these
@pytest.fixture(scope="function")
def second_postgres_execution_log(
    db: Session, privacy_request: PrivacyRequest
) -> ExecutionLog:
    el = ExecutionLog.create(
        db=db,
        data={
            "dataset_name": "my-postgres-db",
            "collection_name": "address",
            "fields_affected": [
                {
                    "path": "my-postgres-db:address:street",
                    "field_name": "street",
                    "data_categories": ["user.provided.identifiable.contact.street"],
                },
                {
                    "path": "my-postgres-db:address:city",
                    "field_name": "city",
                    "data_categories": ["user.provided.identifiable.contact.city"],
                },
            ],
            "action_type": ActionType.access,
            "status": ExecutionLogStatus.error,
            "privacy_request_id": privacy_request.id,
            "message": "Database timed out.",
        },
    )
    yield el
    el.delete(db)


@pytest.fixture(scope="function")
def connection_config(db: Session) -> Generator:
    connection_config = ConnectionConfig.create(
        db=db,
        data={
            "name": str(uuid4()),
            "key": "my_postgres_db_1",
            "connection_type": ConnectionType.postgres,
            "access": AccessLevel.write,
            "secrets": integration_secrets["postgres_example"],
        },
    )
    yield connection_config
    connection_config.delete(db)


@pytest.fixture(scope="function")
def read_connection_config(db: Session) -> Generator:
    connection_config = ConnectionConfig.create(
        db=db,
        data={
            "name": str(uuid4()),
            "key": "my_postgres_db_1_read_config",
            "connection_type": ConnectionType.postgres,
            "access": AccessLevel.read,
            "secrets": integration_secrets["postgres_example"],
        },
    )
    yield connection_config
    connection_config.delete(db)


@pytest.fixture(scope="function")
def postgres_integration_session_cls(connection_config_postgres):
    example_postgres_uri = PostgreSQLConnector(connection_config_postgres).build_uri()
    engine = get_db_engine(database_uri=example_postgres_uri)
    SessionLocal = get_db_session(
        engine=engine,
        autocommit=True,
        autoflush=True,
    )
    yield SessionLocal


@pytest.fixture(scope="function")
def postgres_integration_session(postgres_integration_session_cls):
    yield postgres_integration_session_cls()


def truncate_all_tables(postgres_integration_session):
    postgres_integration_session.execute(
        """
        TRUNCATE
        public.type_link_test,
        public.report,
        public.service_request,
        public.login,
        public.visit,
        public.order_item,
        public.orders,
        public.payment_card,
        public.employee,
        public.customer,
        public.address,
        public.product,
        public.composite_pk_test;
    """
    )


@pytest.fixture(scope="function")
def postgres_integration_db(postgres_integration_session):
    truncate_all_tables(postgres_integration_session)
    postgres_integration_session.execute(
        """
        INSERT INTO public.composite_pk_test VALUES
            (1,10,'linked to customer 1',1),
            (1,11,'linked to customer 2',2),
            (2,10,'linked to customer 3',3);

        -- Populate tables with some public data
        INSERT INTO public.product VALUES
        (1, 'Example Product 1', '$10.00'),
        (2, 'Example Product 2', '$20.00'),
        (3, 'Example Product 3', '$50.00');

        INSERT INTO public.address VALUES
        (1, '123', 'Example Street', 'Exampletown', 'NY', '12345'),
        (2, '4', 'Example Lane', 'Exampletown', 'NY', '12321'),
        (3, '555', 'Example Ave', 'Example City', 'NY', '12000'),
        (4, '1111', 'Example Place', 'Example Mountain', 'TX', '54321');

        INSERT INTO public.customer VALUES
        (1, 'customer-1@example.com', 'John Customer', '2020-04-01 11:47:42', 1),
        (2, 'customer-2@example.com', 'Jill Customer', '2020-04-01 11:47:42', 2),
        (3, 'jane@example.com', 'Jane Customer', '2020-04-01 11:47:42', 4);

        INSERT INTO public.employee VALUES
        (1, 'employee-1@example.com', 'Jack Employee', 3),
        (2, 'employee-2@example.com', 'Jane Employee', 3);

        INSERT INTO public.payment_card VALUES
        ('pay_aaa-aaa', 'Example Card 1', 123456789, 321, true, 1, 1),
        ('pay_bbb-bbb', 'Example Card 2', 987654321, 123, false, 2, 1),
        ('pay_ccc-ccc', 'Example Card 3', 373719391, 222, false, 3, 4);

        INSERT INTO public.orders VALUES
        ('ord_aaa-aaa', 1, 2, 'pay_aaa-aaa'),
        ('ord_bbb-bbb', 2, 1, 'pay_bbb-bbb'),
        ('ord_ccc-ccc', 1, 1, 'pay_aaa-aaa'),
        ('ord_ddd-ddd', 1, 1, 'pay_bbb-bbb'),
        ('ord_ddd-eee', 3, 4, 'pay-ccc-ccc');

        INSERT INTO public.order_item VALUES
        ('ord_aaa-aaa', 1, 1, 1),
        ('ord_bbb-bbb', 1, 1, 1),
        ('ord_ccc-ccc', 1, 1, 1),
        ('ord_ccc-ccc', 2, 2, 1),
        ('ord_ddd-ddd', 1, 1, 1),
        ('ord_eee-eee', 3, 4, 3);

        INSERT INTO public.visit VALUES
        ('customer-1@example.com', '2021-01-06 01:00:00'),
        ('customer-2@example.com', '2021-01-06 01:00:00');

        INSERT INTO public.login VALUES
        (1, 1, '2021-01-01 01:00:00'),
        (2, 1, '2021-01-02 01:00:00'),
        (3, 1, '2021-01-03 01:00:00'),
        (4, 1, '2021-01-04 01:00:00'),
        (5, 1, '2021-01-05 01:00:00'),
        (6, 1, '2021-01-06 01:00:00'),
        (7, 2, '2021-01-06 01:00:00'),
        (8, 3, '2021-01-06 01:00:00');

        INSERT INTO public.service_request VALUES
        ('ser_aaa-aaa', 'customer-1@example.com', 'customer-1-alt@example.com', '2021-01-01', '2021-01-03', 1),
        ('ser_bbb-bbb', 'customer-2@example.com', null, '2021-01-04', null, 1),
        ('ser_ccc-ccc', 'customer-3@example.com', null, '2021-01-05', '2020-01-07', 1),
        ('ser_ddd-ddd', 'customer-3@example.com', null, '2021-05-05', '2020-05-08', 2);

        INSERT INTO public.report VALUES
        (1, 'admin-account@example.com', 'Monthly Report', 2021, 8, 100),
        (2, 'admin-account@example.com', 'Monthly Report', 2021, 9, 100),
        (3, 'admin-account@example.com', 'Monthly Report', 2021, 10, 100),
        (4, 'admin-account@example.com', 'Monthly Report', 2021, 11, 100);

        INSERT INTO public.type_link_test VALUES
        ('1', 'name1'),
        ('2', 'name2');
    """
    )
    yield postgres_integration_session
    truncate_all_tables(postgres_integration_session)
