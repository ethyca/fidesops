import logging

import sqlalchemy
import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from fidesops.api.v1.api import api_router
from fidesops.api.v1.urn_registry import V1_URL_PREFIX
from fidesops.db.database import init_db
from fidesops.core.config import config
from fidesops.tasks.scheduled.scheduler import scheduler
from fidesops.tasks.scheduled.tasks import initiate_scheduled_request_intake
from fidesops.util.logger import get_fides_log_record_factory

logging.basicConfig(level=logging.INFO)
logging.setLogRecordFactory(get_fides_log_record_factory())
logger = logging.getLogger(__name__)

app = FastAPI(title="fidesops", openapi_url=f"{V1_URL_PREFIX}/openapi.json")

# Set all CORS enabled origins
if config.security.CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in config.security.CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router)


def start_webserver() -> None:
    """Run any pending DB migrations and start the webserver."""
    logger.info("****************fidesops****************")
    logger.info("Running any pending DB migrations...")
    init_db(config.database.SQLALCHEMY_DATABASE_URI)
    scheduler.start()

    logger.info("Starting scheduled request intake...")
    initiate_scheduled_request_intake()
    mssql_setup()
    logger.info("Starting web server...")
    uvicorn.run(
        "src.fidesops.main:app",
        host="0.0.0.0",
        port=8080,
        log_config=None,
        reload=config.hot_reloading,
    )


if __name__ == "__main__":
    start_webserver()


def mssql_setup():
    """
    Set up the SQL Server Database for testing.
    The query file must have each query on a separate line.
    Initial connection must be done to the master database.
    """
    MSSQL_URL_TEMPLATE = "mssql+pyodbc://sa:Mssql_pw1@mssql_example:1433/{}?driver=ODBC+Driver+17+for+SQL+Server"
    MASTER_MSSQL_URL = MSSQL_URL_TEMPLATE.format("master") + "&autocommit=True"

    engine = sqlalchemy.create_engine(MASTER_MSSQL_URL)
    with open("data/sql/mssql_example.sql", "r") as query_file:
        queries = [query for query in query_file.read().splitlines() if query != ""]
    for query in queries:
        engine.execute(sqlalchemy.sql.text(query))
