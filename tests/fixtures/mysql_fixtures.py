import logging
import pytest

from fidesops.db.session import get_db_session, get_db_engine
from fidesops.service.connectors import MySQLConnector

logger = logging.getLogger(__name__)


@pytest.fixture(scope="function")
def mysql_integration_session_cls(mysql_connection_config):
    example_postgres_uri = MySQLConnector(mysql_connection_config).build_uri()
    engine = get_db_engine(database_uri=example_postgres_uri)
    SessionLocal = get_db_session(
        engine=engine,
        autocommit=True,
        autoflush=True,
    )
    yield SessionLocal


@pytest.fixture(scope="function")
def mysql_integration_session(mysql_integration_session_cls):
    yield mysql_integration_session_cls()


@pytest.fixture(scope="function")
def mysql_integration_db(mysql_integration_session):
    mysql_integration_session.execute(
        """
        TRUNCATE
        product,
        address,
        customer,
        employee,
        payment_card,
        orders,
        order_item,
        visit,
        login,
        service_request,
        report;
    """
    )
    mysql_integration_session.execute(
        """
        INSERT INTO product VALUES
        (1, 'Example Product 1', 10.00),
        (2, 'Example Product 2', 20.00),
        (3, 'Example Product 3', 50.00);

        INSERT INTO address VALUES
        (1, '123', 'Example Street', 'Exampletown', 'NY', '12345'),
        (2, '4', 'Example Lane', 'Exampletown', 'NY', '12321'),
        (3, '555', 'Example Ave', 'Example City', 'NY', '12000');

        INSERT INTO customer VALUES
        (1, 'customer-1@example.com', 'John Customer', '2020-04-01 11:47:42', 1),
        (2, 'customer-2@example.com', 'Jill Customer', '2020-04-01 11:47:42', 2);

        INSERT INTO employee VALUES
        (1, 'employee-1@example.com', 'Jack Employee', 3),
        (2, 'employee-2@example.com', 'Jane Employee', 3);

        INSERT INTO payment_card VALUES
        ('pay_aaa-aaa', 'Example Card 1', 123456789, 321, true, 1, 1),
        ('pay_bbb-bbb', 'Example Card 2', 987654321, 123, false, 2, 1);

        INSERT INTO orders VALUES
        ('ord_aaa-aaa', 1, 2, 'pay_aaa-aaa'),
        ('ord_bbb-bbb', 2, 1, 'pay_bbb-bbb'),
        ('ord_ccc-ccc', 1, 1, 'pay_aaa-aaa'),
        ('ord_ddd-ddd', 1, 1, 'pay_bbb-bbb');

        INSERT INTO order_item VALUES
        ('ord_aaa-aaa', 1, 1, 1),
        ('ord_bbb-bbb', 1, 1, 1),
        ('ord_ccc-ccc', 1, 1, 1),
        ('ord_ccc-ccc', 2, 2, 1),
        ('ord_ddd-ddd', 1, 1, 1);

        INSERT INTO visit VALUES
        ('customer-1@example.com', '2021-01-06 01:00:00'),
        ('customer-2@example.com', '2021-01-06 01:00:00');

        INSERT INTO login VALUES
        (1, 1, '2021-01-01 01:00:00'),
        (2, 1, '2021-01-02 01:00:00'),
        (3, 1, '2021-01-03 01:00:00'),
        (4, 1, '2021-01-04 01:00:00'),
        (5, 1, '2021-01-05 01:00:00'),
        (6, 1, '2021-01-06 01:00:00'),
        (7, 2, '2021-01-06 01:00:00');

        INSERT INTO service_request VALUES
        ('ser_aaa-aaa', 'customer-1@example.com', 'customer-1-alt@example.com', '2021-01-01', '2021-01-03', 1),
        ('ser_bbb-bbb', 'customer-2@example.com', null, '2021-01-04', null, 1),
        ('ser_ccc-ccc', 'customer-3@example.com', null, '2021-01-05', '2020-01-07', 1),
        ('ser_ddd-ddd', 'customer-3@example.com', null, '2021-05-05', '2020-05-08', 2);

        INSERT INTO report VALUES
        (1, 'admin-account@example.com', 'Monthly Report', 2021, 8, 100),
        (2, 'admin-account@example.com', 'Monthly Report', 2021, 9, 100),
        (3, 'admin-account@example.com', 'Monthly Report', 2021, 10, 100),
        (4, 'admin-account@example.com', 'Monthly Report', 2021, 11, 100);
    """
    )
    yield mysql_integration_session
    mysql_integration_session.execute(
        """
        TRUNCATE
        product,
        address,
        customer,
        employee,
        payment_card,
        orders,
        order_item,
        visit,
        login,
        service_request,
        report;
    """
    )
