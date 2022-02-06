
import pytest

from fidesops.graph.config import Collection, Dataset, FieldAddress, ScalarField
from fidesops.util.saas_util import merge_datasets

def mailchimp_dataset() -> Dataset:
    conversations = Collection(
        name="conversations",
        fields=[ScalarField(name="id")],
    )

    return Dataset(
        name="mailchimp_connector",
        collections=[conversations],
        connection_key="mailchimp_connector",
    )


def mailchimp_config() -> Dataset:
    member = Collection(
        name="member",
        fields=[ScalarField(name="query", identity="email")],
    )
    conversations = Collection(
        name="conversations",
        fields=[ScalarField(name="placeholder", identity="email")],
    )
    messages = Collection(
        name="messages",
        fields=[
            ScalarField(
                name="conversation_id",
                references=[
                    (FieldAddress("mailchimp_connector", "conversations", "id"), "from")
                ],
            ),
        ],
    )

    return Dataset(
        name="mailchimp_connector",
        collections=[member, conversations, messages],
        connection_key="mailchimp_connector",
    )


def manually_merged_dataset() -> Dataset:
    member = Collection(
        name="member",
        fields=[ScalarField(name="query", identity="email")],
    )
    conversations = Collection(
        name="conversations",
        fields=[
            ScalarField(name="placeholder", identity="email"),
            ScalarField(name="id"),
        ],
    )
    messages = Collection(
        name="messages",
        fields=[
            ScalarField(
                name="conversation_id",
                references=[
                    (FieldAddress("mailchimp_connector", "conversations", "id"), "from")
                ],
            ),
        ],
    )

    return Dataset(
        name="mailchimp_connector",
        collections=[member, conversations, messages],
        connection_key="mailchimp_connector",
    )

@pytest.mark.saas_connector
def test_merge_datasets():
    merged_dataset = merge_datasets(mailchimp_config(), mailchimp_dataset())
    assert len(merged_dataset.collections[1].fields) == 2