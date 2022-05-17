import random
import pytest

from fidesops.common_exceptions import PrivacyRequestPaused
from fidesops.models.privacy_request import PrivacyRequest
from fidesops.task import graph_task

from ..graph.graph_test_util import (
    assert_rows_match,
)
from ..task.traversal_data import postgres_and_manual_graph


@pytest.mark.integration_postgres
@pytest.mark.integration
def test_postgres_with_manual_input_access_request_task(
    db,
    policy,
    integration_postgres_config,
    integration_manual_config,
    postgres_integration_db,
    cache
) -> None:

    privacy_request = PrivacyRequest(
        id=f"test_postgres_access_request_task_{random.randint(0, 1000)}"
    )

    with pytest.raises(PrivacyRequestPaused):
        graph_task.run_access_request(
            privacy_request,
            policy,
            postgres_and_manual_graph("postgres_example", "manual_example"),
            [integration_postgres_config, integration_manual_config],
            {"email": "customer-1@example.com"},
        )

    # Graph is paused at the filing cabinet - user needs to manually retrieve some
    # info and add to the graph
    paused_node = privacy_request.get_cached_paused_node()
    assert paused_node == "manual_example:filing_cabinet"

    # Act like the user has added the manual data
    cache.set_encoded_object(
        f"MANUAL_INPUT__{privacy_request.id}__access_request__manual_example:filing_cabinet", [{"id": 1, "beneficiary": "Jane Doe"}]
    )

    # Restart the same privacy request from the paused node
    v = graph_task.run_access_request(
        privacy_request,
        policy,
        postgres_and_manual_graph("postgres_example", "manual_example"),
        [integration_postgres_config, integration_manual_config],
        {"email": "customer-1@example.com"},
        from_paused=True
    )
    assert_rows_match(
        v["manual_example:filing_cabinet"],
        min_size=1,
        keys=["id", "beneficiary"],
    )

    assert_rows_match(
        v["postgres_example:customer"],
        min_size=1,
        keys=["id", "name", "email", "address_id"],
    )

    # Paused node removed from cache
    paused_node = privacy_request.get_cached_paused_node()
    assert paused_node is None
