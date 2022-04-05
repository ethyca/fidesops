"""seed privacy request data

Revision ID: 295b9b40e54d
Revises: 906d7198df28
Create Date: 2022-03-31 20:21:49.222391

"""
from datetime import datetime, timedelta
import string
from uuid import uuid4

from alembic import op
import sqlalchemy as sa
from sqlalchemy import orm

from fidesops.models.client import ClientDetail
from fidesops.models.policy import ActionType, Policy, Rule, RuleTarget
from fidesops.models.privacy_request import PrivacyRequest, PrivacyRequestStatus
from fidesops.util.data_category import DataCategory


# revision identifiers, used by Alembic.
revision = "295b9b40e54d"
down_revision = "906d7198df28"
branch_labels = None
depends_on = None

MIGRATED_DATA_KEY = "migrated_example_data"


def _create_policy(db: orm.Session, action_type: str, client_id: str) -> Policy:
    rand = string.ascii_lowercase[:5]
    policy = Policy.create(
        db=db,
        data={
            "name": f"example {action_type} policy {rand}",
            "key": f"example_{action_type}_policy_{rand}",
            "client_id": client_id,
        },
    )

    rule = Rule.create(
        db=db,
        data={
            "action_type": ActionType.erasure.value,
            "name": f"{action_type} Rule {rand}",
            "policy_id": policy.id,
            "masking_strategy": {
                "strategy": "null_rewrite",
                "configuration": {},
            },
            "client_id": client_id,
        },
    )

    RuleTarget.create(
        db=db,
        data={
            "data_category": DataCategory("user.provided.identifiable.name").value,
            "rule_id": rule.id,
            "client_id": client_id,
        },
    )
    return policy


def upgrade():
    """
    Adds some demo data to this Fidesops instance
    """
    bind = op.get_bind()
    db = orm.Session(bind=bind)

    client = ClientDetail.create(
        db=db,
        data={
            "fides_key": MIGRATED_DATA_KEY,
            "hashed_secret": "autoseededdata",
            "salt": "autoseededdata",
            "scopes": [],
        },
    )

    for action in ActionType.__members__.values():
        policy = _create_policy(db, action.value, client.id)

        for status in PrivacyRequestStatus.__members__.values():
            PrivacyRequest.create(
                db=db,
                data={
                    "external_id": f"ext-{uuid4()}",
                    "started_processing_at": datetime.utcnow(),
                    "requested_at": datetime.utcnow() - timedelta(days=1),
                    "status": status,
                    "origin": f"https://example.com/{status.value}/",
                    "policy_id": policy.id,
                    "client_id": policy.client_id,
                },
            )


def downgrade():
    """
    Removes the demo data added in `upgrade()`
    """
    bind = op.get_bind()
    db = orm.Session(bind=bind)

    client = ClientDetail.get_by(
        db=db,
        field="fides_key",
        value=MIGRATED_DATA_KEY,
    )

    if client is None:
        return

    models = [PrivacyRequest, RuleTarget, Rule, Policy]
    for Model in models:
        qs = Model.filter(db=db, conditions=(Model.client_id == client.id))
        for obj in qs:
            obj.delete(db=db)

    client.delete(db=db)
