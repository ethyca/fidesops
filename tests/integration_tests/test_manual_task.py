import random
import pytest

from fidesops.common_exceptions import PrivacyRequestPaused
from fidesops.models.privacy_request import (
    PrivacyRequest,
    ExecutionLog,
    ExecutionLogStatus,
)
from fidesops.task import graph_task

from ..graph.graph_test_util import (
    assert_rows_match,
)
from ..task.traversal_data import postgres_with_manual_node


@pytest.mark.integration_postgres
@pytest.mark.integration
def test_postgres_with_manual_input_access_request_task(
    db,
    policy,
    integration_postgres_config,
    integration_manual_config,
    postgres_integration_db,
    cache,
) -> None:
    ExecutionLog
    privacy_request = PrivacyRequest(
        id=f"test_postgres_access_request_task_{random.randint(0, 1000)}"
    )

    with pytest.raises(PrivacyRequestPaused):
        graph_task.run_access_request(
            privacy_request,
            policy,
            postgres_with_manual_node("postgres_example", "manual_example"),
            [integration_postgres_config, integration_manual_config],
            {"email": "customer-1@example.com"},
        )

    # Graph is paused at the filing cabinet - user needs to manually retrieve some
    # info and add to the graph
    paused_node = privacy_request.get_cached_paused_node()
    assert paused_node == "manual_example:filing_cabinet"

    execution_logs = db.query(ExecutionLog).filter_by(
        privacy_request_id=privacy_request.id
    )
    assert execution_logs.count() == 6

    # Node upstream of manual node
    customer_logs = execution_logs.filter_by(collection_name="customer").order_by(
        "created_at"
    )
    assert customer_logs.count() == 2
    assert [log.status for log in customer_logs] == [
        ExecutionLogStatus.in_processing,
        ExecutionLogStatus.complete,
    ]

    # Node independent of manual node
    order_logs = execution_logs.filter_by(collection_name="orders").order_by(
        "created_at"
    )
    assert order_logs.count() == 2
    assert [log.status for log in order_logs] == [
        ExecutionLogStatus.in_processing,
        ExecutionLogStatus.complete,
    ]

    # Manual node is paused
    manual_logs = execution_logs.filter_by(collection_name="filing_cabinet").order_by(
        "created_at"
    )
    assert manual_logs.count() == 2
    assert [log.status for log in manual_logs] == [
        ExecutionLogStatus.in_processing,
        ExecutionLogStatus.paused,
    ]

    # Node is downstream of manual node - we never made it there
    payment_logs = execution_logs.filter_by(collection_name="payment_card").all()
    assert not len(payment_logs)

    # Node is downstream of manual node
    address_logs = execution_logs.filter_by(collection_name="address").all()
    assert not len(address_logs)

    # Act like the user has added the manual data
    cache.set_encoded_object(
        f"MANUAL_INPUT__{privacy_request.id}__access_request__manual_example:filing_cabinet",
        [{"id": 1, "authorized_user": "Jane Doe", "payment_card_id": "pay_bbb-bbb"}],
    )
    # Restart the same privacy request from the paused node
    v = graph_task.run_access_request(
        privacy_request,
        policy,
        postgres_with_manual_node("postgres_example", "manual_example"),
        [integration_postgres_config, integration_manual_config],
        {"email": "customer-1@example.com"},
        from_paused=True,
    )
    assert_rows_match(
        v["manual_example:filing_cabinet"],
        min_size=1,
        keys=["id", "authorized_user", "payment_card_id"],
    )

    assert_rows_match(
        v["postgres_example:customer"],
        min_size=1,
        keys=["id", "name", "email", "address_id"],
    )

    # Two payment card rows returned, one from customer_id input, other retrieved from a separate manual input
    assert_rows_match(
        v["postgres_example:payment_card"],
        min_size=2,
        keys=["id", "name", "ccn", "customer_id", "billing_address_id"],
    )

    # Assert customer node not re-run
    assert execution_logs.filter_by(collection_name="customer").count() == 2

    # Assert order node not re-run
    assert execution_logs.filter_by(collection_name="orders").count() == 2

    # Assert manual node rerun
    manual_logs = execution_logs.filter_by(collection_name="filing_cabinet").order_by(
        "created_at"
    )
    assert manual_logs.count() == 4
    assert [log.status for log in manual_logs] == [
        ExecutionLogStatus.in_processing,
        ExecutionLogStatus.paused,
        ExecutionLogStatus.in_processing,
        ExecutionLogStatus.complete,
    ]

    # Payment card node can now run because we have manual input from upstream
    payment_logs = execution_logs.filter_by(collection_name="payment_card").order_by(
        "created_at"
    )
    assert [log.status for log in payment_logs] == [
        ExecutionLogStatus.in_processing,
        ExecutionLogStatus.complete,
    ]

    # Address log can now run because we have manual input from upstream
    address_logs = execution_logs.filter_by(collection_name="address").order_by(
        "created_at"
    )
    assert [log.status for log in address_logs] == [
        ExecutionLogStatus.in_processing,
        ExecutionLogStatus.complete,
    ]

    # Paused node removed from cache
    paused_node = privacy_request.get_cached_paused_node()
    assert paused_node is None
