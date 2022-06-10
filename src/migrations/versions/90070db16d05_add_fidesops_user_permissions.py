"""add fidesops user permissions

Revision ID: 90070db16d05
Revises: 530fb8533ca4
Create Date: 2022-04-27 17:24:31.548916

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "90070db16d05"
down_revision = "530fb8533ca4"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "fidesopsuserpermissions",
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
        sa.Column("user_id", sa.String(), nullable=False),
        sa.Column("scopes", sa.ARRAY(sa.String()), nullable=False),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["fidesopsuser.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("user_id"),
    )
    op.create_index(
        op.f("ix_fidesopsuserpermissions_id"),
        "fidesopsuserpermissions",
        ["id"],
        unique=False,
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(
        op.f("ix_fidesopsuserpermissions_id"), table_name="fidesopsuserpermissions"
    )
    op.drop_table("fidesopsuserpermissions")
    # ### end Alembic commands ###
