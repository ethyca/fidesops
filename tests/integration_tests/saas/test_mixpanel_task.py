import random
import time

import pytest
from fidesops.core.config import config
from fidesops.graph.graph import DatasetGraph
from fidesops.models.privacy_request import PrivacyRequest
from fidesops.schemas.redis_cache import PrivacyRequestIdentity
from fidesops.task import graph_task
from fidesops.task.filter_results import filter_data_categories
from fidesops.task.graph_task import get_cached_data_for_erasures
from tests.graph.graph_test_util import assert_rows_match


@pytest.mark.integration_saas
@pytest.mark.integration_mixpanel
def test_mixpanel_saas_access_request_task(
    db,
    policy,
    mixpanel_connection_config,
    mixpanel_dataset_config,
    mixpanel_create_test_data,
) -> None:
    """Full access request based on the Mixpanel SaaS config"""

    email = mixpanel_create_test_data

    privacy_request = PrivacyRequest(
        id=f"test_saas_access_request_task_{random.randint(0, 1000)}"
    )
    identity = PrivacyRequestIdentity(**{"email": email})
    privacy_request.cache_identity(identity)

    dataset_name = mixpanel_connection_config.get_saas_config().fides_key
    merged_graph = mixpanel_dataset_config.get_graph()
    graph = DatasetGraph(merged_graph)

    v = _wait_for_user_data(
        privacy_request, policy, graph, mixpanel_connection_config, dataset_name, email
    )

    assert_rows_match(
        v[f"{dataset_name}:user"],
        min_size=1,
        keys=[
            "$distinct_id",
            "$properties",
        ],
    )

    assert v[f"{dataset_name}:user"][0]["$properties"]["$email"] == email

    assert_rows_match(
        v[f"{dataset_name}:events"],
        min_size=1,
        keys=["event", "properties"],
    )

    target_categories = {"user"}
    filtered_results = filter_data_categories(
        v, target_categories, graph.data_category_field_mapping
    )

    assert set(filtered_results.keys()) == {
        f"{dataset_name}:user",
        f"{dataset_name}:events",
    }

    assert set(filtered_results[f"{dataset_name}:user"][0]["$properties"].keys()) == {
        "$first_name",
        "$email",
        "$city",
        "$last_name",
    }

    assert set(filtered_results[f"{dataset_name}:events"][0]["properties"].keys()) == {
        "distinct_id",
        "$insert_id",
        "$city",
        "mp_country_code",
    }


@pytest.mark.integration_saas
@pytest.mark.integration_mixpanel
def test_mixpanel_saas_erasure_request_task(
    db,
    policy,
    mixpanel_connection_config,
    mixpanel_dataset_config,
    mixpanel_create_test_data,
) -> None:
    """Full erasure request based on the Mixpanel SaaS config"""
    config.execution.MASKING_STRICT = False  # Allow GDPR Delete

    # Create user for GDPR delete
    erasure_email = mixpanel_create_test_data

    privacy_request = PrivacyRequest(
        id=f"test_saas_access_request_task_{random.randint(0, 1000)}"
    )
    identity = PrivacyRequestIdentity(**{"email": erasure_email})
    privacy_request.cache_identity(identity)

    dataset_name = mixpanel_connection_config.get_saas_config().fides_key
    merged_graph = mixpanel_dataset_config.get_graph()
    graph = DatasetGraph(merged_graph)

    _wait_for_user_data(
        privacy_request,
        policy,
        graph,
        mixpanel_connection_config,
        dataset_name,
        erasure_email,
    )

    response = graph_task.run_erasure(
        privacy_request,
        policy,
        graph,
        [mixpanel_connection_config],
        {"email": erasure_email},
        get_cached_data_for_erasures(privacy_request.id),
    )

    assert response == {
        "mixpanel_connector_example:user": 1,
        "mixpanel_connector_example:events": 0,
    }

    config.execution.MASKING_STRICT = True  # Reset


def _wait_for_user_data(
    privacy_request, policy, graph, mixpanel_connection_config, dataset_name, email
):
    retries = 10
    while retries:
        v = graph_task.run_access_request(
            privacy_request,
            policy,
            graph,
            [mixpanel_connection_config],
            {"email": email},
        )

        if v.get(f"{dataset_name}:user") and v.get(f"{dataset_name}:events"):
            return v

        retries -= 1
        
        time.sleep(5)
    else:
        raise Exception(
            "The user endpoint did not return the required data for testing during the time limit"
        )
