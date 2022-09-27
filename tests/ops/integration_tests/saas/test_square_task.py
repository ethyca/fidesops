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
@pytest.mark.integration_square
def test_square_connection_test(square_connection_config) -> None:
    get_connector(square_connection_config).test_connection()


@pytest.mark.integration_saas
@pytest.mark.integration_square
@pytest.mark.asyncio
async def test_square_access_request_task(
    db,
    policy,
    square_connection_config,
    square_dataset_config,
    square_identity_email,
) -> None:
    """Full access request based on the square SaaS config"""

    privacy_request = PrivacyRequest(
        id=f"test_square_access_request_task_{random.randint(0, 1000)}"
    )
    identity = Identity(**{"email": square_identity_email})
    privacy_request.cache_identity(identity)

    dataset_name = square_connection_config.get_saas_config().fides_key
    merged_graph = square_dataset_config.get_graph()
    graph = DatasetGraph(merged_graph)

    v = await graph_task.run_access_request(
        privacy_request,
        policy,
        graph,
        [square_connection_config],
        {"email": square_identity_email},
        db,
    )

    assert_rows_match(
        v[f"{dataset_name}:customer"],
        min_size=1,
        keys=[
            "id",
            "created_at",
            "updated_at",
            "given_name",
            "family_name",
            "nickname",
            "email_address",
            "address",
            "phone_number",
            "company_name",
            "preferences",
            "creation_source",
            "birthday",
            "segment_ids",
            "version",
        ],
    )
    # verify we only returned data for our identity email
    for customer in v[f"{dataset_name}:customer"]:
        assert customer["email_address"] == square_identity_email

    assert_rows_match(
        v[f"{dataset_name}:locations"],
        min_size=1,
        keys=[
            "id",
            "name",
            "address",
            "timezone",
            "capabilities",
            "status",
            "created_at",
            "merchant_id",
            "country",
            "language_code",
            "currency",
            "business_name",
            "type",
            "business_hours",
            "mcc",
        ],
    )
    assert_rows_match(
        v[f"{dataset_name}:orders"],
        min_size=1,
        keys=["id", "location_id", "customer_id", "state"],
    )