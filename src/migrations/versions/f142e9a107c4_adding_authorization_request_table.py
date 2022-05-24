"""adding authorization request table

Revision ID: f142e9a107c4
Revises: 5078badb90b9
Create Date: 2022-05-23 17:35:29.976562

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "f142e9a107c4"
down_revision = "5078badb90b9"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "authenticationrequest",
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
        sa.Column("connection_key", sa.String(), nullable=False),
        sa.Column("state", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("connection_key"),
    )
    op.create_index(
        op.f("ix_authenticationrequest_id"),
        "authenticationrequest",
        ["id"],
        unique=True,
    )
    op.create_index(
        op.f("ix_authenticationrequest_state"),
        "authenticationrequest",
        ["state"],
        unique=True,
    )
    op.create_index(
        op.f("ix_authenticationrequest_connection_key"),
        "authenticationrequest",
        ["connection_key"],
        unique=True,
    )


def downgrade():
    op.drop_index(
        op.f("ix_authenticationrequest_connection_key"),
        table_name="authenticationrequest",
    )
    op.drop_index(
        op.f("ix_authenticationrequest_state"), table_name="authenticationrequest"
    )
    op.drop_index(
        op.f("ix_authenticationrequest_id"), table_name="authenticationrequest"
    )
    op.drop_table("authenticationrequest")
