"""add_policy_webhooks

Revision ID: 67b501ca2804
Revises: f206d4e7574d
Create Date: 2021-11-24 20:59:41.395000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "67b501ca2804"
down_revision = "f206d4e7574d"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "policywebhook",
        sa.Column("id", sa.String(length=255), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("key", sa.String(), nullable=False),
        sa.Column("policy_id", sa.String(), nullable=False),
        sa.Column("connection_config_id", sa.String(), nullable=False),
        sa.Column(
            "direction",
            sa.Enum("one_way", "two_way", name="webhookdirection"),
            nullable=False,
        ),
        sa.Column(
            "hook_type", sa.Enum("pre", "post", name="webhooktype"), nullable=False
        ),
        sa.Column("order", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["connection_config_id"],
            ["connectionconfig.id"],
        ),
        sa.ForeignKeyConstraint(
            ["policy_id"],
            ["policy.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_index(op.f("ix_policywebhook_id"), "policywebhook", ["id"], unique=False)
    op.create_index(op.f("ix_policywebhook_key"), "policywebhook", ["key"], unique=True)


def downgrade():
    op.drop_index(op.f("ix_policywebhook_key"), table_name="policywebhook")
    op.drop_index(op.f("ix_policywebhook_id"), table_name="policywebhook")
    op.drop_table("policywebhook")
