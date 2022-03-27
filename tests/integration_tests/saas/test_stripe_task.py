import pytest
import random

from fidesops.graph.graph import DatasetGraph
from fidesops.models.privacy_request import ExecutionLog, PrivacyRequest
from fidesops.schemas.redis_cache import PrivacyRequestIdentity

from fidesops.task import graph_task
from tests.graph.graph_test_util import assert_rows_match, records_matching_fields


@pytest.mark.integration
@pytest.mark.integration_saas
def test_stripe_access_request_task(
    db,
    policy,
    stripe_connection_config,
    stripe_dataset_config,
    stripe_identity_email,
) -> None:
    """Full access request based on the Stripe SaaS config"""

    privacy_request = PrivacyRequest(
        id=f"test_stripe_access_request_task_{random.randint(0, 1000)}"
    )
    identity_attribute = "email"
    identity_value = stripe_identity_email
    identity_kwargs = {identity_attribute: identity_value}
    identity = PrivacyRequestIdentity(**identity_kwargs)
    privacy_request.cache_identity(identity)

    dataset_name = stripe_connection_config.get_saas_config().fides_key
    merged_graph = stripe_dataset_config.get_graph()
    graph = DatasetGraph(merged_graph)

    v = graph_task.run_access_request(
        privacy_request,
        policy,
        graph,
        [stripe_connection_config],
        {"email": stripe_identity_email},
    )

    assert_rows_match(
        v[f"{dataset_name}:customer"],
        min_size=1,
        keys=[
            "id",
            "object",
            "address",
            "currency",
            "default_source",
            "description",
            "email",
            "invoice_settings",
            "livemode",
            "name",
            "phone",
            "preferred_locales",
            "shipping",
            "sources",
            "subscriptions",
            "tax_exempt",
            "tax_ids",
        ],
    )

    # links
    assert v[f"{dataset_name}:customer"][0]["email"] == stripe_identity_email

    logs = (
        ExecutionLog.query(db=db)
        .filter(ExecutionLog.privacy_request_id == privacy_request.id)
        .all()
    )

    logs = [log.__dict__ for log in logs]
    assert (
        len(
            records_matching_fields(
                logs, dataset_name=dataset_name, collection_name="customer"
            )
        )
        > 0
    )