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
@pytest.mark.integration_amplitude
def test_amplitude_connection_test(amplitude_connection_config) -> None:
    get_connector(amplitude_connection_config).test_connection()


@pytest.mark.integration_saas
@pytest.mark.integration_amplitude
def test_user_profile_task(
    db,
    policy,
    amplitude_connection_config,
    amplitude_dataset_config,
    amplitude_user_id,
) -> None:
    """Full access request based on the Amplitude SaaS config"""

    privacy_request = PrivacyRequest(
        id=f"test_amplitude_access_request_task_{random.randint(0, 10)}"
    )
    identity_attribute = "email"
    identity_value = amplitude_user_id
    identity_kwargs = {identity_attribute: identity_value}
    identity = PrivacyRequestIdentity(**identity_kwargs)
    privacy_request.cache_identity(identity)

    dataset_name = amplitude_connection_config.get_saas_config().fides_key
    merged_graph = amplitude_dataset_config.get_graph()
    graph = DatasetGraph(merged_graph)
    v = graph_task.run_access_request(
        privacy_request,
        policy,
        graph,
        [amplitude_connection_config],
        {"email": amplitude_user_id},
        db,
    )

    import pdb; pdb.set_trace()


    assert all(
        [
            True
            if key
            in ("recommendations", "user_id", "device_id", "amp_props", "cohort_ids")
            else False
            for key in v[f"{dataset_name}:user-profile"]
        ]
    )

    assert_rows_match(
        v[f"{dataset_name}:user-profile"].get("recommendations"),
        min_size=1,
        keys=[
            "rec_id",
            "child_rec_id",
            "items",
            "is_control",
            "recommendation_source",
            "last_updated",
        ],
    )
    assert amplitude_user_id == v[f"{dataset_name}:user-profile"].get("id")


    privacy_request = PrivacyRequest(
        id=f"test_amplitude_access_request_task_{random.randint(0, 10)}"
    )
    identity_attribute = "email"
    identity_value = amplitude_user_id
    identity_kwargs = {identity_attribute: identity_value}
    identity = PrivacyRequestIdentity(**identity_kwargs)
    privacy_request.cache_identity(identity)

    dataset_name = amplitude_connection_config.get_saas_config().fides_key
    merged_graph = amplitude_dataset_config.get_graph()
    graph = DatasetGraph(merged_graph)
    v = graph_task.run_access_request(
        privacy_request,
        policy,
        graph,
        [amplitude_connection_config],
        {"email": amplitude_user_id},
        db,
    )

    assert all(
        [
            True
            if key
            in (
                "schemas",
                "id",
                "userName",
                "name",
                "active",
                "emails",
                "groups",
                "meta",
                "resourceType",
            )
            else False
            for key in v[f"{dataset_name}:scim-users"]
        ]
    )

    assert_rows_match(
        v[f"{dataset_name}:scim-users"].get("emails"),
        min_size=1,
        keys=["primary", "value"],
    )

    assert_rows_match(
        v[f"{dataset_name}:scim-users"].get("meta"), min_size=1, keys=["resourceType"]
    )

    assert all(
        True if key in v[f"{dataset_name}:scim-users"].get("name") else False
        for key in ("givenName", "familyName")
    )

    assert amplitude_user_id == v[f"{dataset_name}:scim-users"].get("id")


@pytest.mark.integration_saas
@pytest.mark.integration_amplitude
def test_scim_users_task(
    db,
    policy,
    amplitude_connection_config,
    amplitude_dataset_config,
    amplitude_user_id,
) -> None:
    """Full access request based on the Amplitude SaaS config"""

    privacy_request = PrivacyRequest(
        id=f"test_amplitude_access_request_task_{random.randint(0, 10)}"
    )
    identity_attribute = "email"
    identity_value = amplitude_user_id
    identity_kwargs = {identity_attribute: identity_value}
    identity = PrivacyRequestIdentity(**identity_kwargs)
    privacy_request.cache_identity(identity)

    dataset_name = amplitude_connection_config.get_saas_config().fides_key
    merged_graph = amplitude_dataset_config.get_graph()
    graph = DatasetGraph(merged_graph)
    v = graph_task.run_access_request(
        privacy_request,
        policy,
        graph,
        [amplitude_connection_config],
        {"email": amplitude_user_id},
        db,
    )

    # Need to understand flow of this as Data creation takes more than 30 minutes to get created.
