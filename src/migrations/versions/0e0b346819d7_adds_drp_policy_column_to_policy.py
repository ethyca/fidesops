"""adds drp_policy column to policy

Revision ID: 0e0b346819d7
Revises: 530fb8533ca4
Create Date: 2022-04-28 20:36:01.314299

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.


revision = "0e0b346819d7"
down_revision = "530fb8533ca4"
branch_labels = None
depends_on = None


def upgrade():
    drpaction = postgresql.ENUM(
        "access",
        "deletion",
        "sale_opt_out",
        "sale_opt_in",
        "access_categories",
        "access_specific",
        name="drpaction",
        create_type=False,
    )
    drpaction.create(op.get_bind())
    op.add_column("policy", sa.Column("drp_action", drpaction, nullable=True))
    op.create_index(op.f("ix_policy_drp_action"), "policy", ["drp_action"], unique=True)


def downgrade():
    op.drop_index(op.f("ix_policy_drp_action"), table_name="policy")
    op.drop_column("policy", "drp_action")
    op.execute("DROP TYPE drpaction;")
