"""create SaaS connection config

Revision ID: 1dfc5a2d30e7
Revises: 07014ff34eb2
Create Date: 2022-02-09 23:27:24.742938

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = '1dfc5a2d30e7'
down_revision = '07014ff34eb2'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "saasconnectionconfig",
        sa.Column("id", sa.String(length=255), nullable=False),
        sa.Column("saas_config", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.ForeignKeyConstraint(
            ["id"],
            ["connectionconfig.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_saasconnectionconfig_id"), "connectionconfig", ["id"], unique=False
    )


def downgrade():
    op.drop_index(op.f("ix_saasconnectionconfig_id"), table_name="saasconnectionconfig")
    op.drop_table("saasconnectionconfig")