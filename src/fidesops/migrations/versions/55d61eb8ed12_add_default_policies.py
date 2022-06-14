"""add default policies

Revision ID: 55d61eb8ed12
Revises: 27fe9da9d0f9
Create Date: 2022-06-13 19:26:24.197262

"""
from sqlalchemy.orm import Session

from fidesops.api.v1.scope_registry import SCOPE_REGISTRY
from fidesops.db.session import get_db_session
from fidesops.models.client import ClientDetail
from fidesops.models.policy import ActionType, DrpAction, Policy, Rule, RuleTarget
from fidesops.models.storage import StorageConfig
from fidesops.schemas.storage.storage import StorageType
from fidesops.util.data_category import DataCategory

revision = "55d61eb8ed12"
down_revision = "27fe9da9d0f9"
branch_labels = None
depends_on = None

FIDESOPS_AUTOGENERATED_CLIENT_KEY = "fidesops_autogenerated_client"
FIDESOPS_AUTOGENERATED_STORAGE_KEY = "fidesops_autogenerated_storage_destination"
AUTOGENERATED_ACCCES_KEY = "download"
AUTOGENERATED_ERASURE_KEY = "delete"


def upgrade():
    """Data migration only.

    Create an autogenerated client and storage destination, then use those to create
    autogenerated 'download' and 'delete' policies if they don't already exist."""
    SessionLocal = get_db_session()
    db = SessionLocal()

    default_local_storage = StorageConfig.create(
        db=db,
        data={
            "name": "Fidesops Autogenerated Local Storage",
            "type": StorageType.local,
            "key": FIDESOPS_AUTOGENERATED_STORAGE_KEY,
            "details": {"naming": "request_id"},
        },
    )

    client, _ = ClientDetail.create_client_and_secret(
        db, SCOPE_REGISTRY, fides_key=FIDESOPS_AUTOGENERATED_CLIENT_KEY
    )

    if not Policy.filter(
        db=db, conditions=(Policy.key == AUTOGENERATED_ACCCES_KEY)
    ).first():
        # Only create a "download" policy if one does not already exist
        autogenerate_access_policy(db, client, default_local_storage)
    if not Policy.filter(
        db=db, conditions=(Policy.key == AUTOGENERATED_ERASURE_KEY)
    ).first():
        # Only create a "delete" policy if one does not already exist
        autogenerate_erasure_policy(db, client)

    db.close()


def downgrade():
    """Data migration only.

    Remove 'download' and delete' policies if they were created by the autogenerated client, and then
    attempt to remove the autogenerated client and local storage destination.
    """
    SessionLocal = get_db_session()
    db = SessionLocal()
    client = ClientDetail.filter(
        db=db, conditions=(ClientDetail.fides_key == FIDESOPS_AUTOGENERATED_CLIENT_KEY)
    ).first()

    if not client:
        return

    access_policy = Policy.filter(
        db=db,
        conditions=(
            Policy.key == AUTOGENERATED_ACCCES_KEY and Policy.client_id == client.id
        ),
    ).first()
    if access_policy:
        # Only delete "download" policy if it was created by the autogenerated client
        access_policy.delete(db)

    erasure_policy = Policy.filter(
        db=db,
        conditions=(
            Policy.key == AUTOGENERATED_ERASURE_KEY and Policy.client_id == client.id
        ),
    ).first()

    if erasure_policy:
        # Only delete "delete" policy if it was created by the autogenerated client
        erasure_policy.delete(db)

    try:
        client.delete(db)
        storage = StorageConfig.filter(
            db=db, conditions=(StorageConfig.key == FIDESOPS_AUTOGENERATED_STORAGE_KEY)
        ).first()
        if storage:
            storage.delete(db)
    except Exception:
        pass

    db.close()


def autogenerate_access_policy(
    db: Session, client: ClientDetail, storage: StorageConfig
) -> None:
    """Create an autogenerated 'download' access policy, with an access rule attached,
    targeting user.provided.identifiable data"""
    access_policy = Policy.create_or_update(
        db,
        data={
            "name": "Fidesops Autogenerated Access Policy",
            "key": AUTOGENERATED_ACCCES_KEY,
            "drp_action": DrpAction.access,
            "client_id": client.id,
        },
    )

    access_rule = Rule.create(
        db,
        data={
            "name": "Fidesops Autogenerated Access Rule",
            "action_type": ActionType.access.value,
            "policy_id": access_policy.id,
            "client_id": client.id,
            "storage_destination_id": storage.id,
        },
    )

    RuleTarget.create(
        db=db,
        data={
            "name": "Fidesops Autogenerated Access Target",
            "data_category": DataCategory("user.provided.identifiable").value,
            "rule_id": access_rule.id,
            "client_id": client.id,
        },
    )


def autogenerate_erasure_policy(db: Session, client: ClientDetail) -> None:
    """Create an autogenerated 'deletion' erasure policy, with an erasure rule attached,
    targeting user.provided.identifiable data"""
    erasure_policy = Policy.create_or_update(
        db,
        data={
            "name": "Fidesops Autogenerated Erasure Policy",
            "key": AUTOGENERATED_ERASURE_KEY,
            "drp_action": DrpAction.deletion,
            "client_id": client.id,
        },
    )

    erasure_rule = Rule.create(
        db,
        data={
            "name": "Fidesops Autogenerated Erasure Rule",
            "action_type": ActionType.erasure.value,
            "policy_id": erasure_policy.id,
            "client_id": client.id,
            "masking_strategy": {
                "strategy": "null_rewrite",
                "configuration": {},
            },
        },
    )

    RuleTarget.create(
        db=db,
        data={
            "name": "Fidesops Autogenerated Erasure Target",
            "data_category": DataCategory("user.provided.identifiable").value,
            "rule_id": erasure_rule.id,
            "client_id": client.id,
        },
    )
