"""add saas config to connection config

Revision ID: 1dfc5a2d30e7
Revises: 07014ff34eb2
Create Date: 2022-02-09 23:27:24.742938

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = "1dfc5a2d30e7"
down_revision = "07014ff34eb2"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "connectionconfig",
        sa.Column(
            "saas_config", postgresql.JSONB(astext_type=sa.Text()), nullable=True
        ),
    )


def downgrade():
    op.drop_column("connectionconfig", "saas_config")
