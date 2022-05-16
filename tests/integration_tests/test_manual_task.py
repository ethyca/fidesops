import random
import pytest

from fidesops.common_exceptions import PrivacyRequestPaused
from fidesops.models.privacy_request import ExecutionLog, PrivacyRequest
from fidesops.task import graph_task
from fidesops.task.task_resources import TaskResources

from ..graph.graph_test_util import (
    assert_rows_match,
    records_matching_fields
)
from ..task.traversal_data import integration_db_graph, postgres_and_manual_graph


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

    # Act like the user has added the manual data
    cache.set_encoded_object(
        f"MANUAL_INPUT__{privacy_request.id}__access_request__manual_example:filing_cabinet", [{"id": 1, "beneficiary": "Jane Doe"}]
    )

    v = graph_task.test_paused(
        privacy_request,
        policy,
        postgres_and_manual_graph("postgres_example", "manual_example"),
        [integration_postgres_config, integration_manual_config],
        {"email": "customer-1@example.com"},
        "postgres_example:customer"
    )

    assert_rows_match(
        v["manual_example:filing_cabinet"],
        min_size=1,
        keys=["id", "beneficiary"],
    )
