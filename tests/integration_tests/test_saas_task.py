import pytest
import random

from fidesops.graph.graph import DatasetGraph
from fidesops.models.privacy_request import ExecutionLog, PrivacyRequest
from fidesops.schemas.redis_cache import PrivacyRequestIdentity

from fidesops.task import graph_task
from fidesops.task.filter_results import filter_data_categories
from fidesops.task.graph_task import get_cached_data_for_erasures
from tests.graph.graph_test_util import assert_rows_match, records_matching_fields


@pytest.mark.integration_saas
@pytest.mark.integration_mailchimp
def test_saas_access_request_task(
    db,
    policy,
    connection_config_mailchimp,
    dataset_config_mailchimp,
    mailchimp_identity_email,
) -> None:
    """Full access request based on the Mailchimp SaaS config"""

    privacy_request = PrivacyRequest(
        id=f"test_saas_access_request_task_{random.randint(0, 1000)}"
    )
    identity_attribute = "email"
    identity_value = mailchimp_identity_email
    identity_kwargs = {identity_attribute: identity_value}
    identity = PrivacyRequestIdentity(**identity_kwargs)
    privacy_request.cache_identity(identity)

    dataset_name = connection_config_mailchimp.get_saas_config().fides_key
    merged_graph = dataset_config_mailchimp.get_graph()
    graph = DatasetGraph(merged_graph)

    v = graph_task.run_access_request(
        privacy_request,
        policy,
        graph,
        [connection_config_mailchimp],
        {"email": mailchimp_identity_email},
    )

    assert_rows_match(
        v[f"{dataset_name}:member"],
        min_size=1,
        keys=[
            "id",
            "list_id",
            "email_address",
            "unique_email_id",
            "web_id",
            "email_type",
            "status",
            "merge_fields",
            "ip_signup",
            "timestamp_signup",
            "ip_opt",
            "timestamp_opt",
            "language",
            "email_client",
            "location",
            "source",
            "tags",
        ],
    )
    assert_rows_match(
        v[f"{dataset_name}:conversations"],
        min_size=2,
        keys=["id", "campaign_id", "list_id", "from_email", "from_label", "subject"],
    )
    assert_rows_match(
        v[f"{dataset_name}:messages"],
        min_size=3,
        keys=[
            "id",
            "conversation_id",
            "from_label",
            "from_email",
            "subject",
            "message",
            "read",
            "timestamp",
        ],
    )

    # links
    assert v[f"{dataset_name}:member"][0]["email_address"] == mailchimp_identity_email

    logs = (
        ExecutionLog.query(db=db)
        .filter(ExecutionLog.privacy_request_id == privacy_request.id)
        .all()
    )

    logs = [log.__dict__ for log in logs]
    assert (
        len(
            records_matching_fields(
                logs, dataset_name=dataset_name, collection_name="member"
            )
        )
        > 0
    )
    assert (
        len(
            records_matching_fields(
                logs,
                dataset_name=dataset_name,
                collection_name="conversations",
            )
        )
        > 0
    )
    assert (
        len(
            records_matching_fields(
                logs, dataset_name=dataset_name, collection_name="messages"
            )
        )
        > 0
    )


@pytest.mark.integration_saas
@pytest.mark.integration_mailchimp
def test_saas_erasure_request_task(
    db,
    policy,
    connection_config_mailchimp,
    dataset_config_mailchimp,
    mailchimp_identity_email,
    reset_mailchimp_data,
) -> None:
    """Full erasure request based on the Mailchimp SaaS config"""

    privacy_request = PrivacyRequest(
        id=f"test_saas_erasure_request_task_{random.randint(0, 1000)}"
    )
    identity_attribute = "email"
    identity_value = mailchimp_identity_email
    identity_kwargs = {identity_attribute: identity_value}
    identity = PrivacyRequestIdentity(**identity_kwargs)
    privacy_request.cache_identity(identity)

    dataset_name = connection_config_mailchimp.get_saas_config().fides_key
    merged_graph = dataset_config_mailchimp.get_graph()
    graph = DatasetGraph(merged_graph)

    graph_task.run_access_request(
        privacy_request,
        policy,
        graph,
        [connection_config_mailchimp],
        {"email": mailchimp_identity_email},
    )

    v = graph_task.run_erasure(
        privacy_request,
        policy,
        graph,
        [connection_config_mailchimp],
        {"email": mailchimp_identity_email},
        get_cached_data_for_erasures(privacy_request.id),
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
                logs,
                dataset_name=dataset_name,
                collection_name="conversations",
                message="No values were erased since no primary key was defined for this collection",
            )
        )
        == 1
    )
    assert (
        len(
            records_matching_fields(
                logs,
                dataset_name=dataset_name,
                collection_name="messages",
                message="No values were erased since no primary key was defined for this collection",
            )
        )
        == 1
    )
    assert v == {
        f"{dataset_name}:member": 1,
        f"{dataset_name}:conversations": 0,
        f"{dataset_name}:messages": 0,
    }


@pytest.mark.integration_saas
@pytest.mark.saas_connector_sentry
def test_sentry_saas_access_request_task(
    db,
    policy,
    connection_config_sentry,
    dataset_config_sentry,
    sentry_identity_email,
) -> None:
    """Full access request based on the Sentry SaaS config"""

    privacy_request = PrivacyRequest(
        id=f"test_saas_access_request_task_{random.randint(0, 1000)}"
    )
    identity = PrivacyRequestIdentity(**{"email": sentry_identity_email})
    privacy_request.cache_identity(identity)

    dataset_name = connection_config_sentry.get_saas_config().fides_key
    merged_graph = dataset_config_sentry.get_graph()
    graph = DatasetGraph(merged_graph)

    v = graph_task.run_access_request(
        privacy_request,
        policy,
        graph,
        [connection_config_sentry],
        {"email": sentry_identity_email},
    )

    assert_rows_match(
        v["sentry_connector:organizations"],
        min_size=1,
        keys=[
            "id",
            "slug",
            "status",
            "name",
            "dateCreated",
            "isEarlyAdopter",
            "require2FA",
            "requireEmailVerification",
            "avatar",
            "features",
        ],
    )
    assert_rows_match(
        v["sentry_connector:employees"],
        min_size=1,
        keys=[
            "id",
            "email",
            "name",
            "user",
            "role",
            "roleName",
            "pending",
            "expired",
            "flags",
            "dateCreated",
            "inviteStatus",
            "inviterName",
            "projects",
        ],
    )
    assert_rows_match(
        v["sentry_connector:projects"],
        min_size=3,
        keys=[
            "id",
            "slug",
            "name",
            "isPublic",
            "isBookmarked",
            "color",
            "dateCreated",
            "firstEvent",
            "firstTransactionEvent",
            "hasSessions",
            "features",
            "status",
            "platform",
            "isInternal",
            "isMember",
            "hasAccess",
            "avatar",
            "organization",
        ],
    )

    # TODO add test for issues once data is populated

    assert_rows_match(
        v["sentry_connector:user_feedback"],
        min_size=1,
        keys=[
            "id",
            "eventID",
            "name",
            "email",
            "comments",
            "dateCreated",
            "user",
            "event",
            "issue",
        ],
    )

    # Person returns empty dicts
    assert_rows_match(
        v["sentry_connector:person"],
        min_size=1,
        keys=[
            "id",
            "hash",
            "tagValue",
            "identifier",
            "username",
            "email",
            "name",
            "ipAddress",
            "dateCreated",
            "avatarUrl",
        ],
    )

    target_categories = {"user.provided"}
    filtered_results = filter_data_categories(
        v,
        target_categories,
        graph.data_category_field_mapping,
    )

    assert set(filtered_results.keys()) == {
        "sentry_connector:person",
        "sentry_connector:employees",
        "sentry_connector:user_feedback",
    }

    assert set(filtered_results["sentry_connector:person"][0].keys()) == {
        "email",
        "name",
        "username",
    }
    assert (
        filtered_results["sentry_connector:person"][0]["email"] == sentry_identity_email
    )

    assert set(filtered_results["sentry_connector:employees"][0].keys()) == {
        "email",
        "user",
        "name",
    }
    assert (
        filtered_results["sentry_connector:employees"][0]["email"]
        == sentry_identity_email
    )
    assert set(filtered_results["sentry_connector:employees"][0]["user"].keys()) == {
        "email",
        "name",
        "avatarUrl",
        "username",
        "emails",
    }

    assert (
        filtered_results["sentry_connector:employees"][0]["user"]["email"]
        == sentry_identity_email
    )
    assert filtered_results["sentry_connector:employees"][0]["user"]["emails"] == [
        {"email": sentry_identity_email}
    ]

    assert set(filtered_results["sentry_connector:user_feedback"][0].keys()) == {
        "email",
        "user",
        "comments",
        "name",
    }
    assert (
        filtered_results["sentry_connector:user_feedback"][0]["email"]
        == sentry_identity_email
    )

    assert set(
        filtered_results["sentry_connector:user_feedback"][0]["user"].keys()
    ) == {
        "email",
        "name",
        "username",
    }
    assert (
        filtered_results["sentry_connector:user_feedback"][0]["user"]["email"]
        == sentry_identity_email
    )
