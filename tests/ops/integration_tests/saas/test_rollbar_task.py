import logging
import random

import pytest

from fidesops.ops.core.config import config
from fidesops.ops.graph.graph import DatasetGraph
from fidesops.ops.models.privacy_request import PrivacyRequest
from fidesops.ops.schemas.redis_cache import Identity
from fidesops.ops.service.connectors import get_connector
from fidesops.ops.task import graph_task
from fidesops.ops.task.graph_task import get_cached_data_for_erasures
from tests.ops.graph.graph_test_util import assert_rows_match

logger = logging.getLogger(__name__)


@pytest.mark.integration_saas
@pytest.mark.integration_rollbar
def test_rollbar_connection_test(rollbar_connection_config) -> None:
    get_connector(rollbar_connection_config).test_connection()


@pytest.mark.integration_saas
@pytest.mark.integration_rollbar
@pytest.mark.asyncio
async def test_rollbar_access_request_task(
    db,
    policy,
    rollbar_connection_config,
    rollbar_dataset_config,
    rollbar_identity_email,
) -> None:
    """Full access request based on the Rollbar SaaS config"""

    privacy_request = PrivacyRequest(
        id=f"test_rollbar_access_request_task_{random.randint(0, 1000)}"
    )
    identity = Identity(**{"email": rollbar_identity_email})
    privacy_request.cache_identity(identity)

    dataset_name = rollbar_connection_config.get_saas_config().fides_key
    merged_graph = rollbar_dataset_config.get_graph()
    graph = DatasetGraph(merged_graph)

    v = await graph_task.run_access_request(
        privacy_request,
        policy,
        graph,
        [rollbar_connection_config],
        {"email": rollbar_identity_email},
        db,
    )

    assert_rows_match(
        v[f"{dataset_name}:projects"],
        min_size=1,
        keys=[
            "id",
            "account_id",
            "name",
        ],
    )
    assert_rows_match(
        v[f"{dataset_name}:project_access_token"],
        min_size=1,
        keys=[
            "project_id",
            "name",
            "access_token",
        ],
    )
    assert_rows_match(
        v[f"{dataset_name}:instances"],
        min_size=1,
        keys=[
            "id",
            "timestamp",
            "data",
        ],
    )
    # verify we only returned data for our identity email
    for instance in v[f"{dataset_name}:instances"]:
        assert instance["data"]["person"]["email"] == rollbar_identity_email


@pytest.mark.integration_saas
@pytest.mark.integration_rollbar
@pytest.mark.asyncio
async def test_rollbar_erasure_request_task(
    db,
    policy,
    erasure_policy_string_rewrite,
    rollbar_connection_config,
    rollbar_dataset_config,
    rollbar_erasure_identity_email,
    rollbar_erasure_data,
    rollbar_test_client,
) -> None:
    """Full erasure request based on the Rollbar SaaS config"""

    privacy_request = PrivacyRequest(
        id=f"test_rollbar_erasure_request_task_{random.randint(0, 1000)}"
    )
    identity_kwargs = {"email": rollbar_erasure_identity_email}

    identity = Identity(**identity_kwargs)
    privacy_request.cache_identity(identity)

    dataset_name = rollbar_connection_config.get_saas_config().fides_key
    merged_graph = rollbar_dataset_config.get_graph()
    graph = DatasetGraph(merged_graph)
    v = await graph_task.run_access_request(
        privacy_request,
        policy,
        graph,
        [rollbar_connection_config],
        identity_kwargs,
        db,
    )

    assert_rows_match(
        v[f"{dataset_name}:projects"],
        min_size=1,
        keys=[
            "id",
            "account_id",
            "name",
        ],
    )
    assert_rows_match(
        v[f"{dataset_name}:project_access_token"],
        min_size=1,
        keys=[
            "project_id",
            "name",
            "access_token",
        ],
    )
    assert_rows_match(
        v[f"{dataset_name}:instances"],
        min_size=1,
        keys=[
            "id",
            "timestamp",
            "data",
        ],
    )
    # verify we only returned data for our identity email
    for instance in v[f"{dataset_name}:instances"]:
        assert instance["data"]["person"]["email"] == rollbar_erasure_identity_email

    temp_masking = config.execution.masking_strict
    config.execution.masking_strict = True

    x = await graph_task.run_erasure(
        privacy_request,
        erasure_policy_string_rewrite,
        graph,
        [rollbar_connection_config],
        identity_kwargs,
        get_cached_data_for_erasures(privacy_request.id),
        db,
    )
    config.execution.masking_strict = temp_masking
    # verify masking request was issued for endpoints with update actions
    assert erasure == {
        f"{dataset_name}:projects": 0,
        f"{dataset_name}:project_access_token": 0,
        f"{dataset_name}:instances": 1,
    }
