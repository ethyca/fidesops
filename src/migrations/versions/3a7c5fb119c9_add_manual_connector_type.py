"""add manual connector type

Revision ID: 3a7c5fb119c9
Revises: 5078badb90b9
Create Date: 2022-05-13 19:18:45.400669

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "3a7c5fb119c9"
down_revision = "5078badb90b9"
branch_labels = None
depends_on = None


def upgrade():
    op.execute("alter type connectiontype add value 'manual'")


def downgrade():
    op.execute("delete from connectionconfig where connection_type in ('manual')")
    op.execute("alter type connectiontype rename to connectiontype_old")
    op.execute(
        "create type connectiontype as enum('postgres', 'mongodb', 'mysql', 'https', 'snowflake', 'redshift', 'mssql', 'mariadb', 'bigquery', 'saas')"
    )
    op.execute(
        (
            "alter table connectionconfig alter column connection_type type connectiontype using "
            "connection_type::text::connectiontype"
        )
    )
    op.execute("drop type connectiontype_old")
