"""user table and client updates

Revision ID: 48e8d9dcd839
Revises: 1dfc5a2d30e7
Create Date: 2022-03-07 18:38:38.602291

"""
import sqlalchemy_utils
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "48e8d9dcd839"
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
    op.add_column("client", sa.Column("fides_key", sa.String(), nullable=True))
    op.add_column("client", sa.Column("username", sa.String(), nullable=True))
    op.create_index(op.f("ix_client_fides_key"), "client", ["fides_key"], unique=True)
    op.create_index(op.f("ix_client_username"), "client", ["username"], unique=True)


def downgrade():
    op.drop_index(op.f("ix_client_username"), table_name="client")
    op.drop_index(op.f("ix_client_fides_key"), table_name="client")
    op.drop_column("client", "username")
    op.drop_column("client", "fides_key")
    op.drop_index(op.f("ix_fidesopsuser_username"), table_name="fidesopsuser")
    op.drop_index(op.f("ix_fidesopsuser_id"), table_name="fidesopsuser")
    op.drop_table("fidesopsuser")
