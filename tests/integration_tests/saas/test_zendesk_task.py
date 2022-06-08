import pytest
import random

from fidesops.graph.graph import DatasetGraph
from fidesops.models.privacy_request import ExecutionLog, PrivacyRequest
from fidesops.schemas.redis_cache import PrivacyRequestIdentity

from fidesops.task import graph_task
from fidesops.task.graph_task import get_cached_data_for_erasures
from tests.graph.graph_test_util import assert_rows_match, records_matching_fields


@pytest.mark.integration_saas
@pytest.mark.integration_zendesk
def test_zendesk_access_request_task(
    db,
    policy,
    zendesk_connection_config,
    zendesk_dataset_config,
    zendesk_identity_email,
) -> None:
    """Full access request based on the Zendesk SaaS config"""

    privacy_request = PrivacyRequest(
        id=f"test_saas_access_request_task_{random.randint(0, 1000)}"
    )
    identity = PrivacyRequestIdentity(**{"email": zendesk_identity_email})
    privacy_request.cache_identity(identity)

    dataset_name = zendesk_connection_config.get_saas_config().fides_key
    merged_graph = zendesk_dataset_config.get_graph()
    graph = DatasetGraph(merged_graph)

    import pdb;
    pdb.set_trace()
    v = graph_task.run_access_request(
        privacy_request,
        policy,
        graph,
        [zendesk_connection_config],
        {"email": zendesk_identity_email},
    )

    # assert_rows_match(
    #     v[f"{dataset_name}:ticket"],
    #     min_size=1,
    #     keys=[
    #         "id",
    #         "external_id",
    #         "created_at",
    #         "updated_at",
    #         "type",
    #         "subject",
    #         "raw_subject",
    #         "description",
    #         "priority",
    #         "status",
    #         "recipient",
    #         "requester_id",
    #         "submitter_id",
    #         "assignee_id",
    #         "organization_id",
    #         "group_id",
    #         "collaborator_ids",
    #         "follower_ids",
    #         "email_cc_ids",
    #         "forum_topic_id",
    #         "problem_id",
    #         "has_incidents",
    #         "is_public",
    #         "due_at",
    #         "tags",
    #         "custom_fields",
    #         "satisfaction_rating",
    #         "sharing_agreement_ids",
    #         "fields",
    #         "followup_ids",
    #         "brand_id",
    #         "allow_channelback",
    #         "allow_attachments"
    #     ],
    # )
    # assert_rows_match(
    #     v[f"{dataset_name}:ticket_soft_delete"],
    #     min_size=2,
    #     keys=["customer_id", "ticket_id"],
    # )
    # assert_rows_match(
    #     v[f"{dataset_name}:comments"],
    #     min_size=1,
    #     keys=[
    #         "id",
    #         "type",
    #         "public",
    #         "data",
    #         "formatted_from",
    #         "formatted_to",
    #         "transcription_visible",
    #         "author_id",
    #         "body",
    #         "html_body",
    #         "trusted",
    #         "attachments",
    #         "created_at",
    #         "via"
    #     ],
    # )
    # assert_rows_match(
    #     v[f"{dataset_name}:identity"],
    #     min_size=2,
    #     keys=[
    #         "id",
    #         "user_id",
    #         "type",
    #         "value",
    #         "verified",
    #         "primary",
    #         "created_at",
    #         "updated_at",
    #         "undeliverable_count",
    #         "deliverable_state"
    #     ],
    # )
    # assert_rows_match(
    #     v[f"{dataset_name}:user_soft_delete"],
    #     min_size=1,
    #     keys=["customer_id"],
    # )
    assert_rows_match(
        v[f"{dataset_name}:users"],
        min_size=1,
        keys=[
            "id",
            "name",
            "email",
            "time_zone",
            "phone",
            "shared_phone_number",
            "photo",
            "locale_id",
            "locale",
            "role",
            "verified",
            "external_id",
            "tags",
            "alias",
            "active",
            "shared",
            "shared_agent",
            "last_login_at",
            "two_factor_auth_enabled",
            "signature",
            "details",
            "notes",
            "role_type",
            "custom_role_id",
            "moderator",
            "ticket_restriction",
            "only_private_comments",
            "restricted_agent",
            "suspended",
            "chat_only",
            "default_group_id",
            "report_csv",
        ],
    )
    # assert v[f"{dataset_name}:member"][0]["email_address"] == zendesk_identity_email

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


# @pytest.mark.integration_saas
# @pytest.mark.integration_zendesk
# def test_zendesk_erasure_request_task(
#     db,
#     policy,
#     erasure_policy_string_rewrite,
#     zendesk_connection_config,
#     zendesk_dataset_config,
#     zendesk_identity_email,
#     reset_zendesk_data,
# ) -> None:
#     """Full erasure request based on the Zendesk SaaS config"""

#     privacy_request = PrivacyRequest(
#         id=f"test_saas_erasure_request_task_{random.randint(0, 1000)}"
#     )
#     identity = PrivacyRequestIdentity(**{"email": zendesk_identity_email})
#     privacy_request.cache_identity(identity)

#     dataset_name = zendesk_connection_config.get_saas_config().fides_key
#     merged_graph = zendesk_dataset_config.get_graph()
#     graph = DatasetGraph(merged_graph)

#     graph_task.run_access_request(
#         privacy_request,
#         policy,
#         graph,
#         [zendesk_connection_config],
#         {"email": zendesk_identity_email},
#     )

#     v = graph_task.run_erasure(
#         privacy_request,
#         erasure_policy_string_rewrite,
#         graph,
#         [zendesk_connection_config],
#         {"email": zendesk_identity_email},
#         get_cached_data_for_erasures(privacy_request.id),
#     )

#     logs = (
#         ExecutionLog.query(db=db)
#         .filter(ExecutionLog.privacy_request_id == privacy_request.id)
#         .all()
#     )
#     logs = [log.__dict__ for log in logs]
#     assert (
#         len(
#             records_matching_fields(
#                 logs,
#                 dataset_name=dataset_name,
#                 collection_name="conversations",
#                 message="No values were erased since no primary key was defined for this collection",
#             )
#         )
#         == 1
#     )
#     assert (
#         len(
#             records_matching_fields(
#                 logs,
#                 dataset_name=dataset_name,
#                 collection_name="messages",
#                 message="No values were erased since no primary key was defined for this collection",
#             )
#         )
#         == 1
#     )
#     assert v == {
#         f"{dataset_name}:member": 1,
#         f"{dataset_name}:conversations": 0,
#         f"{dataset_name}:messages": 0,
#     }
