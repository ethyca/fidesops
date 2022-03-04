"""add fidesops_user_table

Revision ID: 028c3385120a
Revises: 1dfc5a2d30e7
Create Date: 2022-03-04 20:11:51.058283

"""
import sqlalchemy_utils
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "028c3385120a"
down_revision = "1dfc5a2d30e7"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "fidesopsuser",
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
        sa.Column("username", sa.String(), nullable=True),
        sa.Column(
            "password",
            sqlalchemy_utils.types.encrypted.encrypted_type.StringEncryptedType(),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_fidesopsuser_id"), "fidesopsuser", ["id"], unique=False)
    op.create_index(
        op.f("ix_fidesopsuser_username"), "fidesopsuser", ["username"], unique=True
    )


def downgrade():
    op.drop_index(op.f("ix_fidesopsuser_username"), table_name="fidesopsuser")
    op.drop_index(op.f("ix_fidesopsuser_id"), table_name="fidesopsuser")
    op.drop_table("fidesopsuser")
