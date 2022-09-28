import random

import pytest
from firebase_admin import auth
from firebase_admin.auth import UserRecord

from fidesops.ops.graph.graph import DatasetGraph
from fidesops.ops.models.privacy_request import PrivacyRequest
from fidesops.ops.schemas.redis_cache import Identity
from fidesops.ops.service.saas_request.override_implementations.firebase_auth_request_overrides import (
    initialize_firebase,
)
from fidesops.ops.task import graph_task
from fidesops.ops.task.graph_task import get_cached_data_for_erasures
from tests.ops.graph.graph_test_util import assert_rows_match


@pytest.mark.integration_saas
@pytest.mark.integration_saas_override
@pytest.mark.asyncio
async def test_firebase_auth_access_request(
    db,
    policy,
    firebase_auth_connection_config,
    firebase_auth_dataset_config,
    firebase_auth_user: UserRecord,
) -> None:
    """Full access request based on the Firebase Auth SaaS config"""

    privacy_request = PrivacyRequest(
        id=f"test_firebase_access_request_task_{random.randint(0, 1000)}"
    )
    identity = Identity(**{"email": firebase_auth_user.email})
    privacy_request.cache_identity(identity)

    dataset_name = firebase_auth_connection_config.get_saas_config().fides_key
    merged_graph = firebase_auth_dataset_config.get_graph()
    graph = DatasetGraph(merged_graph)

    v = await graph_task.run_access_request(
        privacy_request,
        policy,
        graph,
        [firebase_auth_connection_config],
        {"email": firebase_auth_user.email},
        db,
    )

    assert_rows_match(
        v[f"{dataset_name}:user"],
        min_size=1,
        keys=[
            "uid",
            "email",
            "display_name",
            "disabled",
            "email_verified",
        ],
    )


@pytest.mark.integration_saas
@pytest.mark.integration_saas_override
@pytest.mark.asyncio
async def test_firebase_auth_update_request(
    db,
    policy,
    firebase_auth_connection_config,
    firebase_auth_dataset_config,
    firebase_auth_user: UserRecord,
    erasure_policy_string_rewrite,
    firebase_auth_secrets,
) -> None:
    """Update request based on the Firebase Auth SaaS config"""

    privacy_request = PrivacyRequest(
        id=f"test_firebase_update_request_task_{random.randint(0, 1000)}"
    )
    identity = Identity(**{"email": firebase_auth_user.email})
    privacy_request.cache_identity(identity)

    dataset_name = firebase_auth_connection_config.get_saas_config().fides_key
    merged_graph = firebase_auth_dataset_config.get_graph()
    graph = DatasetGraph(merged_graph)

    v = await graph_task.run_access_request(
        privacy_request,
        policy,
        graph,
        [firebase_auth_connection_config],
        {"email": firebase_auth_user.email},
        db,
    )

    assert_rows_match(
        v[f"{dataset_name}:user"],
        min_size=1,
        keys=[
            "uid",
            "email",
            "display_name",
            "disabled",
            "email_verified",
        ],
    )

    v = await graph_task.run_erasure(
        privacy_request,
        erasure_policy_string_rewrite,
        graph,
        [firebase_auth_connection_config],
        {"email": firebase_auth_user.email},
        get_cached_data_for_erasures(privacy_request.id),
        db,
    )

    app = initialize_firebase(firebase_auth_secrets)
    user: UserRecord = auth.get_user(firebase_auth_user.uid, app=app)
    assert user.display_name == "MASKED"
    assert user.email == firebase_auth_user.email
    assert user.photo_url == firebase_auth_user.photo_url
    assert user.disabled == firebase_auth_user.disabled
    assert user.email_verified == firebase_auth_user.email_verified
