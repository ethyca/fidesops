import logging
import random

import pytest

from fidesops.ops.graph.graph import DatasetGraph
from fidesops.ops.models.privacy_request import PrivacyRequest
from fidesops.ops.schemas.redis_cache import PrivacyRequestIdentity
from fidesops.ops.service.connectors import get_connector
from fidesops.ops.task import graph_task
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
    identity_attribute = "email"
    identity_value = rollbar_identity_email
    identity_kwargs = {identity_attribute: identity_value}

    identity = PrivacyRequestIdentity(**{"email": rollbar_identity_email})
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
    results = v[f"{dataset_name}:instances"]

    assert_rows_match(
        results,
        min_size=1,
        keys=[
            "instances",
        ],
    )
    for instances in results:
        for item in instances["instances"]:
            assert_rows_match(
                [item],
                min_size=1,
                keys=[
                    "id",
                    "timestamp",
                    "data",
                ],
            )
