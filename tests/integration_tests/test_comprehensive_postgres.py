import logging
from typing import Dict, Generator
from uuid import uuid4
import yaml

import pytest
from sqlalchemy.orm.exc import ObjectDeletedError

from fidesops.core.config import load_file
from fidesops.db.session import get_db_session, get_db_engine
from fidesops.models.connectionconfig import (
    ConnectionConfig,
    AccessLevel,
    ConnectionType,
)
from fidesops.models.datasetconfig import DatasetConfig
from fidesops.models.policy import (
    ActionType,
    DataCategory,
    Policy,
    Rule,
    RuleTarget,
)
from tests.service.privacy_request.request_runner_service_test import (
    get_privacy_request_results,
)

logger = logging.getLogger(__name__)


def load_dataset(filename: str) -> Dict:
    yaml_file = load_file(filename)
    with open(yaml_file, "r") as file:
        return yaml.safe_load(file).get("dataset", [])


@pytest.fixture(scope="session")
def integration_db() -> Generator:
    """Return a connection to the PostgreSQL example DB"""
    example_postgres_uri = "postgresql://postgres:postgres@comprehensive_postgres_example/comprehensive_postgres_example"
    engine = get_db_engine(database_uri=example_postgres_uri)
    logger.debug(f"Connecting to PostgreSQL example database at: {engine.url}")
    SessionLocal = get_db_session(engine=engine)
    the_session = SessionLocal()
    # Setup above...
    yield the_session
    # Teardown below...
    the_session.close()
    engine.dispose()


@pytest.fixture(scope="session")
def connection_config(
    db,  # This is the application DB
):
    connection_config = ConnectionConfig.create(  # This is the external DB
        db=db,
        data={
            "name": str(uuid4()),
            "key": "comprehensive_postgres_example",
            "connection_type": ConnectionType.postgres,
            "access": AccessLevel.write,
            "secrets": {
                "host": "comprehensive_postgres_example",
                "port": "5432",
                "dbname": "comprehensive_postgres_example",
                "username": "postgres",
                "password": "postgres",
            },
        },
    )
    yield connection_config
    connection_config.delete(db)


@pytest.fixture(scope="session")
def dataset_config(
    connection_config,  # Our previously configured DB connection
    db,  # This is the application DB
):
    dataset = load_dataset("data/dataset/comprehensive_test_dataset.yml")[0]
    fides_key = dataset["fides_key"]
    dataset_config = DatasetConfig.create(
        db=db,
        data={
            "connection_config_id": connection_config.id,
            "fides_key": fides_key,
            "dataset": dataset,
        },
    )
    yield dataset_config
    dataset_config.delete(db=db)


def generate_policy(
    db,
    oauth_client,
    masking_strategy,
    masking_strategy_configuration,
    target_data_category,
    key,
):
    erasure_policy = Policy.create(
        db=db,
        data={
            "name": "example erasure policy",
            "key": key,
            "client_id": oauth_client.id,
        },
    )

    erasure_rule = Rule.create(
        db=db,
        data={
            "action_type": ActionType.erasure.value,
            "client_id": oauth_client.id,
            "name": str(uuid4()),
            "policy_id": erasure_policy.id,
            "masking_strategy": {
                "strategy": masking_strategy,
                "configuration": masking_strategy_configuration,
            },
        },
    )

    rule_target = RuleTarget.create(
        db=db,
        data={
            "client_id": oauth_client.id,
            "data_category": DataCategory(target_data_category).value,
            "rule_id": erasure_rule.id,
        },
    )
    return erasure_policy


@pytest.fixture(scope="session")
def access_all_policy():
    pass


@pytest.mark.integration_postgres
@pytest.mark.integration
@pytest.mark.parametrize(
    "strategy,configuration",
    [
        ("null_rewrite", {}),
        # ("something_else", {"blah": "blah"}),
    ],
)
def test_erasure_all_types(
    strategy,
    configuration,
    cache,
    db,
    oauth_client,
    dataset_config,
    integration_db,
    api_client,
):
    policy = generate_policy(
        db,
        oauth_client,
        masking_strategy=strategy,
        masking_strategy_configuration=configuration,
        target_data_category="system",
        key=f"{strategy}_erasure_policy",
    )
    pr = get_privacy_request_results(
        db,
        policy,
        cache,
        {
            "requested_at": "2021-08-30T16:09:37.359Z",
            "policy_key": policy.key,
            "identity": {"email": "1@example.com"},
        },
    )
    # pr.delete(db=db)
    policy.delete(db=db)

    import pdb

    pdb.set_trace()

    res = integration_db.execute("select * from postgres_types;")
    for r in res:
        print(r)


# @pytest.mark.integration_postgres
# @pytest.mark.integration
# def test_access_all_types():
#     pass
