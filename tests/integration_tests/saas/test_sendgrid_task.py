import pytest
import random

from fidesops.graph.graph import DatasetGraph
from fidesops.models.privacy_request import ExecutionLog, PrivacyRequest
from fidesops.schemas.redis_cache import PrivacyRequestIdentity

from fidesops.task import graph_task
from fidesops.task.graph_task import get_cached_data_for_erasures
from tests.graph.graph_test_util import assert_rows_match, records_matching_fields


@pytest.mark.integration_saas
@pytest.mark.integration_sendgrid
def test_sendgrid_access_request_task(
    db,
    policy,
    sendgrid_connection_config,
    sendgrid_dataset_config,
    sendgrid_identity_email,
) -> None:
    """Full access request based on the Sendgrid SaaS config"""
    privacy_request = PrivacyRequest(
        id=f"test_saas_access_request_task_{random.randint(0, 1000)}"
    )
    identity = PrivacyRequestIdentity(**{"email": sendgrid_identity_email})
    privacy_request.cache_identity(identity)

    dataset_name = sendgrid_connection_config.get_saas_config().fides_key
    merged_graph = sendgrid_dataset_config.get_graph()
    graph = DatasetGraph(merged_graph)

    v = graph_task.run_access_request(
        privacy_request,
        policy,
        graph,
        [sendgrid_connection_config],
        {"email": sendgrid_identity_email},
    )

    assert_rows_match(
        v[f"{dataset_name}:contacts"],
        min_size=1,
        keys=[
            "id",
            "first_name",
            "last_name",
            "email",
            "alternate_emails",
            "address_line_1",
            "address_line_2",
            "city",
            "state_province_region",
            "country",
            "postal_code",
            "phone_number",
            "whatsapp",
            "list_ids",
            "segment_ids",
            "created_at",
            "updated_at",
        ],
    )
