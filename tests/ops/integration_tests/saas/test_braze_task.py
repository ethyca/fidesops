import logging
import random

import pytest

from fidesops.ops.graph.graph import DatasetGraph
from fidesops.ops.models.privacy_request import PrivacyRequest
from fidesops.ops.schemas.redis_cache import Identity
from fidesops.ops.service.connectors import get_connector
from fidesops.ops.task import graph_task
from tests.ops.graph.graph_test_util import assert_rows_match

logger = logging.getLogger(__name__)


@pytest.mark.integration_saas
@pytest.mark.integration_braze
def test_braze_connection_test(braze_connection_config) -> None:
    get_connector(braze_connection_config).test_connection()


@pytest.mark.integration_saas
@pytest.mark.integration_braze
@pytest.mark.asyncio
async def test_saas_access_request_task(
    db,
    policy,
    braze_connection_config,
    braze_dataset_config,
    braze_identity_email,
) -> None:
    """Full access request based on the braze SaaS config"""

    privacy_request = PrivacyRequest(
        id=f"test_braze_access_request_task_{random.randint(0, 250)}"
    )
    identity_attribute = "email"
    identity_value = braze_identity_email
    identity_kwargs = {identity_attribute: identity_value}
    identity = Identity(**identity_kwargs)
    privacy_request.cache_identity(identity)

    dataset_name = braze_connection_config.get_saas_config().fides_key
    merged_graph = braze_dataset_config.get_graph()
    graph = DatasetGraph(merged_graph)

    v = await graph_task.run_access_request(
        privacy_request,
        policy,
        graph,
        [braze_connection_config],
        {identity_attribute: braze_identity_email},
        db,
    )
    key_users = f"{dataset_name}:users"
    assert_rows_match(
        v[key_users],
        min_size=1,
        keys=[
            "external_id",
            "user_aliases",
            "braze_id",
            "first_name",
            "last_name",
            identity_attribute,
            "custom_attributes",
            "dob",
            "country",
            "home_city",
            "language",
            "gender",
            "phone",
            "time_zone",
            "email_subscribe",
            "email_opted_in_at",
        ],
    )

    for entry in v[key_users]:
        assert identity_value == entry.get(identity_attribute)

    key_subscription_groups = f"{dataset_name}:subscription_groups_email"
    assert_rows_match(
        v[key_subscription_groups],
        min_size=1,
        keys=[
            identity_attribute,
            "phone",
            "external_id",
            "subscription_groups",
        ],
    )

    for entry in v[key_subscription_groups]:
        assert identity_value == entry.get(identity_attribute)
