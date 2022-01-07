import logging
from typing import Generator

import pytest
import sqlalchemy as sqlalchemy
from sqlalchemy import func, select, table

from fidesops.db.session import get_db_session, get_db_engine

logger = logging.getLogger(__name__)


MSSQL_URL_TEMPLATE = "mssql+pyodbc://sa:Mssql_pw1@mssql_example:1433/{}?driver=ODBC+Driver+17+for+SQL+Server"
MSSQL_URL = MSSQL_URL_TEMPLATE.format("mssql_example")
MASTER_MSSQL_URL = MSSQL_URL_TEMPLATE.format("master") + "&autocommit=True"


@pytest.fixture(scope="module")
def mssql_setup():
    """
    Set up the SQL Server Database for testing.
    The query file must have each query on a separate line.
    Initial connection must be done to the master database.
    """
    engine = sqlalchemy.create_engine(MASTER_MSSQL_URL)
    with open("data/sql/mssql_example.sql", "r") as query_file:
        queries = [query for query in query_file.read().splitlines() if query != ""]
    for query in queries:
        engine.execute(sqlalchemy.sql.text(query))
    yield engine
    engine.dispose()


@pytest.fixture(scope="module")
def mssql_example_db(mssql_setup) -> Generator:
    """Return a connection to the MsSQL example DB"""
    engine = get_db_engine(database_uri=MSSQL_URL)
    logger.debug(f"Connecting to MsSQL example database at: {engine.url}")
    SessionLocal = get_db_session(engine=engine)
    the_session = SessionLocal()
    # Setup above...
    yield the_session
    # Teardown below...
    the_session.close()
    engine.dispose()


@pytest.mark.integration
def test_mssql_example_data(mssql_example_db):
    """Confirm that the example database is populated with simulated data"""
    expected_counts = {
        "product": 3,
        "address": 4,
        "customer": 3,
        "employee": 2,
        "payment_card": 3,
        "orders": 5,
        "order_item": 6,
        "visit": 2,
        "login": 8,
        "service_request": 4,
        "report": 4,
        "type_link_test": 2
    }

    for table_name, expected_count in expected_counts.items():
        # NOTE: we could use text() here, but we want to avoid SQL string
        # templating as much as possible. instead, use the table() helper to
        # dynamically generate the FROM clause for each table_name
        count_sql = select(func.count()).select_from(table(table_name))
        assert mssql_example_db.execute(count_sql).scalar() == expected_count
