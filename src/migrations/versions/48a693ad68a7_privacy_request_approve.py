"""privacy request approve

Revision ID: 48a693ad68a7
Revises: 1dfc5a2d30e7
Create Date: 2022-03-10 19:03:39.338759

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "48a693ad68a7"
down_revision = "5a966cd643d7"
branch_labels = None
depends_on = None


def upgrade():
    op.execute("alter type privacyrequeststatus add value 'approved'")
    op.execute("alter type privacyrequeststatus add value 'denied'")

    op.add_column(
        "privacyrequest",
        sa.Column("approved_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.add_column(
        "privacyrequest", sa.Column("approved_by", sa.String(), nullable=True)
    )


def downgrade():
    op.drop_column("privacyrequest", "approved_by")
    op.drop_column("privacyrequest", "approved_at")

    op.execute("delete from privacyrequest where status in ('approved', 'denied')")

    op.execute("alter type privacyrequeststatus rename to privacyrequeststatus_old")
    op.execute(
        "create type privacyrequeststatus as enum('in_processing', 'complete', 'pending', 'error', 'paused')"
    )
    op.execute(
        (
            "alter table privacyrequest alter column status type privacyrequeststatus using "
            "status::text::privacyrequeststatus"
        )
    )
    op.execute("drop type privacyrequeststatus_old")
