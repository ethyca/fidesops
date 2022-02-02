import logging
import pytest

from fidesops.db.session import get_db_session, get_db_engine
from fidesops.service.connectors import MicrosoftSQLServerConnector

logger = logging.getLogger(__name__)


@pytest.fixture(scope="function")
def mssql_integration_session_cls(mssql_connection_config):
    pass


@pytest.fixture(scope="function")
def mssql_integration_session(mssql_integration_session_cls):
    pass


@pytest.fixture(scope="function")
def mssql_integration_db(mssql_integration_session):
    pass
