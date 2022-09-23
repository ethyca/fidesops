import random

import pytest
import requests

from fidesops.ops.core.config import config
from fidesops.ops.graph.graph import DatasetGraph
from fidesops.ops.models.privacy_request import PrivacyRequest
from fidesops.ops.schemas.redis_cache import Identity
from fidesops.ops.service.connectors import get_connector
from fidesops.ops.task import graph_task
from fidesops.ops.task.graph_task import get_cached_data_for_erasures
from tests.ops.graph.graph_test_util import assert_rows_match


@pytest.mark.integration_saas
@pytest.mark.integration_fullstory
def test_fullstory_connection_test(fullstory_connection_config) -> None:
    get_connector(fullstory_connection_config).test_connection()


@pytest.mark.integration_saas
@pytest.mark.integration_fullstory
@pytest.mark.asyncio
async def test_fullstory_access_request_task(
    db,
    policy,
    fullstory_connection_config,
    fullstory_dataset_config,
    fullstory_identity_email,
    fullstory_uid,
    # fullstory_access_data,
) -> None:
    """Full access request based on the Fullstory SaaS config"""
    privacy_request = PrivacyRequest(
        id=f"test_fullstory_access_request_task_{random.randint(0, 1000)}"
    )
    identity = Identity(**{"email": fullstory_identity_email})

    privacy_request.cache_identity(identity)

    dataset_name = fullstory_connection_config.get_saas_config().fides_key
    merged_graph = fullstory_dataset_config.get_graph()
    graph = DatasetGraph(merged_graph)

    v = await graph_task.run_access_request(
        privacy_request,
        policy,
        graph,
        [fullstory_connection_config],
        {"id": fullstory_uid},
        db,
    )

    assert_rows_match(
        v[f"{dataset_name}:users"],
        min_size=1,
        keys=[
            "uid",
            "email",
            "displayName",
            "customVars",
            "numSessions",
            "firstSeen",
            "lastSeen",
            "existingOperation",
        ],
    )


# @pytest.mark.integration_saas
# @pytest.mark.integration_fullstory
# @pytest.mark.asyncio
# async def test_fullstory_erasure_request_task(
#     db,
#     policy,
#     erasure_policy_string_rewrite,
#     fullstory_connection_config,
#     fullstory_dataset_config,
#     fullstory_erasure_identity_email,
#     fullstory_uid
# ) -> None:
#     """Full access request based on the Fullstory SaaS config"""
#     privacy_request = PrivacyRequest(
#         id=f"test_fullstory_access_request_task_{random.randint(0, 1000)}"
#     )
#     identity = Identity(**{"email": fullstory_erasure_identity_email})

#     privacy_request.cache_identity(identity)

#     dataset_name = fullstory_connection_config.get_saas_config().fides_key
#     merged_graph = fullstory_dataset_config.get_graph()
#     graph = DatasetGraph(merged_graph)

#     v = await graph_task.run_access_request(
#         privacy_request,
#         policy,
#         graph,
#         [fullstory_connection_config],
#         {"id": fullstory_uid},
#         db,
#     )

#     assert_rows_match(
#         v[f"{dataset_name}:users"],
#         min_size=1,
#         keys=[
#             "uid",
#             "email",
#             "displayName",
#             "customVars",
#             "numSessions",
#             "firstSeen",
#             "lastSeen",
#             "existingOperation"
#         ],
#     )

#     x = await graph_task.run_erasure(
#         privacy_request,
#         erasure_policy_string_rewrite,
#         graph,
#         [fullstory_connection_config],
#         {"email": fullstory_erasure_identity_email},
#         get_cached_data_for_erasures(privacy_request.id),
#         db,
#     )
#     #Add assertions here
