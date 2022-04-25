"""add_fidesops_user_permissions

Revision ID: 5411bd415315
Revises: 906d7198df28
Create Date: 2022-04-22 16:02:50.900479

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "5411bd415315"
down_revision = "906d7198df28"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "fidesopsuserpermissions",
        sa.Column("id", sa.String(length=255), primary_key=True, nullable=False),
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
        sa.Column(
            "user_id",
            sa.String(),
            sa.ForeignKey("fidesopsuser.id"),
            nullable=False,
            unique=True,
        ),
        sa.Column("scopes", sa.ARRAY(sa.String()), nullable=False),
    )
    op.create_index(
        op.f("ix_fidesopsuserpermissions_user_id"),
        "fidesopsuserpermissions",
        ["user_id"],
        unique=False,
    )


def downgrade():
    op.drop_table("fidesopsuserpermissions")
