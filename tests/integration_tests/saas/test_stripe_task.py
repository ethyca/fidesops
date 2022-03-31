import pytest
import random

from fidesops.graph.graph import DatasetGraph
from fidesops.models.privacy_request import ExecutionLog, PrivacyRequest
from fidesops.schemas.redis_cache import PrivacyRequestIdentity

from fidesops.task import graph_task
from tests.graph.graph_test_util import assert_rows_match, records_matching_fields


@pytest.mark.integration_saas
@pytest.mark.integration_stripe
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

    assert v[f"{dataset_name}:customer"][0]["email"] == stripe_identity_email

    assert_rows_match(
        v[f"{dataset_name}:bank_account"],
        min_size=1,
        keys=[
            "account_holder_name",
            "account_holder_type",
            "bank_name",
            "card",
            "country",
            "currency",
            "customer",
            "fingerprint",
            "id",
            "last4",
            "object",
            "routing_number",
            "status",
        ],
    )

    assert_rows_match(
        v[f"{dataset_name}:card"],
        min_size=1,
        keys=[
            "address_city",
            "address_country",
            "address_line1",
            "address_line1_check",
            "address_line2",
            "address_state",
            "address_zip",
            "address_zip_check",
            "brand",
            "country",
            "customer",
            "cvc_check",
            "dynamic_last4",
            "exp_month",
            "exp_year",
            "fingerprint",
            "funding",
            "id",
            "last4",
            "name",
            "object",
            "tokenization_method",
        ],
    )

    assert_rows_match(
        v[f"{dataset_name}:charge"],
        min_size=1,
        keys=[
            "billing_details",
            "currency",
            "customer",
            "description",
            "failure_message",
            "id",
            "invoice",
            "metadata",
            "object",
            "on_behalf_of",
            "order",
            "paid",
            "payment_intent",
            "payment_method",
            "payment_method_details",
            "receipt_email",
            "receipt_number",
            "receipt_url",
            "refunded",
            "refunds",
            "review",
            "shipping",
            "source_transfer",
            "statement_descriptor",
            "statement_descriptor_suffix",
            "status",
        ],
    )

    assert_rows_match(
        v[f"{dataset_name}:credit_note"],
        min_size=1,
        keys=[
            "amount",
            "created",
            "currency",
            "customer",
            "customer_balance_transaction",
            "discount_amount",
            "id",
            "invoice",
            "lines",
            "livemode",
            "memo",
            "metadata",
            "number",
            "object",
            "out_of_band_amount",
            "pdf",
            "reason",
            "refund",
            "status",
            "subtotal",
            "tax_amounts",
            "total",
            "type",
            "voided_at",
        ],
    )

    assert_rows_match(
        v[f"{dataset_name}:customer"],
        min_size=1,
        keys=[
            "address",
            "currency",
            "default_source",
            "description",
            "email",
            "id",
            "invoice_settings",
            "livemode",
            "name",
            "object",
            "phone",
            "preferred_locales",
            "shipping",
            "sources",
            "subscriptions",
            "tax_exempt",
            "tax_ids",
        ],
    )

    assert_rows_match(
        v[f"{dataset_name}:customer_balance_transaction"],
        min_size=1,
        keys=[
            "amount",
            "created",
            "credit_note",
            "currency",
            "customer",
            "description",
            "ending_balance",
            "id",
            "invoice",
            "livemode",
            "metadata",
            "object",
            "type",
        ],
    )

    assert_rows_match(
        v[f"{dataset_name}:dispute"],
        min_size=1,
        keys=[
            "amount",
            "balance_transactions",
            "charge",
            "created",
            "currency",
            "evidence",
            "evidence_details",
            "id",
            "is_charge_refundable",
            "livemode",
            "metadata",
            "object",
            "payment_intent",
            "reason",
            "status",
        ],
    )

    assert_rows_match(
        v[f"{dataset_name}:invoice"],
        min_size=1,
        keys=[
            "account_country",
            "account_name",
            "amount_due",
            "amount_paid",
            "amount_remaining",
            "application_fee_amount",
            "attempt_count",
            "attempted",
            "auto_advance",
            "billing_reason",
            "charge",
            "collection_method",
            "created",
            "currency",
            "custom_fields",
            "customer",
            "customer_address",
            "customer_email",
            "customer_name",
            "customer_phone",
            "customer_shipping",
            "customer_tax_exempt",
            "customer_tax_ids",
            "default_payment_method",
            "default_source",
            "default_tax_rates",
            "description",
            "discount",
            "due_date",
            "ending_balance",
            "footer",
            "hosted_invoice_url",
            "id",
            "invoice_pdf",
            "lines",
            "livemode",
            "next_payment_attempt",
            "number",
            "object",
            "paid",
            "payment_intent",
            "period_end",
            "period_start",
            "post_payment_credit_notes_amount",
            "pre_payment_credit_notes_amount",
            "receipt_number",
            "starting_balance",
            "statement_descriptor",
            "status",
            "status_transitions",
            "subscription",
            "subtotal",
            "tax",
            "tax_percent",
            "total",
            "total_tax_amounts",
            "webhooks_delivered_at",
        ],
    )

    assert_rows_match(
        v[f"{dataset_name}:invoice_item"], min_size=1, keys=["amount", "id", "object"]
    )

    assert_rows_match(
        v[f"{dataset_name}:payment_intent"],
        min_size=1,
        keys=[
            "amount",
            "amount_capturable",
            "amount_received",
            "application",
            "application_fee_amount",
            "canceled_at",
            "cancellation_reason",
            "capture_method",
            "charges",
            "client_secret",
            "confirmation_method",
            "created",
            "currency",
            "customer",
            "description",
            "id",
            "invoice",
            "last_payment_error",
            "livemode",
            "next_action",
            "object",
            "on_behalf_of",
            "payment_method",
            "payment_method_options",
            "payment_method_types",
            "receipt_email",
            "review",
            "setup_future_usage",
            "shipping",
            "source",
            "statement_descriptor",
            "statement_descriptor_suffix",
            "status",
            "transfer_data",
            "transfer_group",
        ],
    )

    assert_rows_match(
        v[f"{dataset_name}:payment_method"],
        min_size=1,
        keys=[
            "billing_details",
            "card",
            "created",
            "customer",
            "id",
            "livemode",
            "object",
            "type",
        ],
    )

    assert_rows_match(
        v[f"{dataset_name}:setup_intent"],
        min_size=1,
        keys=[
            "application",
            "cancellation_reason",
            "client_secret",
            "created",
            "customer",
            "description",
            "id",
            "last_setup_error",
            "livemode",
            "mandate",
            "next_action",
            "object",
            "on_behalf_of",
            "payment_method",
            "payment_method_options",
            "payment_method_types",
            "single_use_mandate",
            "status",
            "usage",
        ],
    )

    assert_rows_match(
        v[f"{dataset_name}:subscription"],
        min_size=1,
        keys=[
            "application_fee_percent",
            "billing_cycle_anchor",
            "billing_thresholds",
            "cancel_at",
            "cancel_at_period_end",
            "canceled_at",
            "collection_method",
            "created",
            "current_period_end",
            "current_period_start",
            "customer",
            "days_until_due",
            "default_payment_method",
            "default_source",
            "default_tax_rates",
            "discount",
            "ended_at",
            "id",
            "items",
            "latest_invoice",
            "livemode",
            "next_pending_invoice_item_invoice",
            "object",
            "pending_invoice_item_interval",
            "pending_setup_intent",
            "pending_update",
            "plan",
            "quantity",
            "schedule",
            "start_date",
            "status",
            "tax_percent",
            "trial_end",
            "trial_start",
        ],
    )

    assert_rows_match(
        v[f"{dataset_name}:tax_id"],
        min_size=1,
        keys=[
            "country",
            "created",
            "customer",
            "id",
            "livemode",
            "object",
            "type",
            "value",
            "verification",
        ],
    )

    logs = (
        ExecutionLog.query(db=db)
        .filter(ExecutionLog.privacy_request_id == privacy_request.id)
        .all()
    )

    logs = [log.__dict__ for log in logs]

    assert (
        len(
            records_matching_fields(
                logs, dataset_name=dataset_name, collection_name="bank_account"
            )
        )
        > 0
    )

    assert (
        len(
            records_matching_fields(
                logs, dataset_name=dataset_name, collection_name="card"
            )
        )
        > 0
    )

    assert (
        len(
            records_matching_fields(
                logs, dataset_name=dataset_name, collection_name="charge"
            )
        )
        > 0
    )

    assert (
        len(
            records_matching_fields(
                logs, dataset_name=dataset_name, collection_name="credit_note"
            )
        )
        > 0
    )

    assert (
        len(
            records_matching_fields(
                logs, dataset_name=dataset_name, collection_name="customer"
            )
        )
        > 0
    )

    assert (
        len(
            records_matching_fields(
                logs,
                dataset_name=dataset_name,
                collection_name="customer_balance_transaction",
            )
        )
        > 0
    )

    assert (
        len(
            records_matching_fields(
                logs, dataset_name=dataset_name, collection_name="dispute"
            )
        )
        > 0
    )

    assert (
        len(
            records_matching_fields(
                logs, dataset_name=dataset_name, collection_name="invoice"
            )
        )
        > 0
    )

    assert (
        len(
            records_matching_fields(
                logs, dataset_name=dataset_name, collection_name="invoice_item"
            )
        )
        > 0
    )

    assert (
        len(
            records_matching_fields(
                logs, dataset_name=dataset_name, collection_name="payment_intent"
            )
        )
        > 0
    )

    assert (
        len(
            records_matching_fields(
                logs, dataset_name=dataset_name, collection_name="payment_method"
            )
        )
        > 0
    )

    assert (
        len(
            records_matching_fields(
                logs, dataset_name=dataset_name, collection_name="setup_intent"
            )
        )
        > 0
    )

    assert (
        len(
            records_matching_fields(
                logs, dataset_name=dataset_name, collection_name="subscription"
            )
        )
        > 0
    )

    assert (
        len(
            records_matching_fields(
                logs, dataset_name=dataset_name, collection_name="tax_id"
            )
        )
        > 0
    )
