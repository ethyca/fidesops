"""adds provided identity table for identity storage and later identity search

Revision ID: 3c5e1253465d
Revises: fc90277bbcde
Create Date: 2022-07-08 11:53:05.215848

"""
import sqlalchemy as sa
import sqlalchemy_utils
from alembic import op

# revision identifiers, used by Alembic.
revision = "3c5e1253465d"
down_revision = "fc90277bbcde"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "providedidentity",
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
        sa.Column("privacy_request_id", sa.String(), nullable=False),
        sa.Column(
            "field_name",
            sa.Enum("email", "phone_number", name="providedidentitytype"),
            nullable=False,
        ),
        sa.Column("hashed_value", sa.String(), nullable=True),
        sa.Column(
            "encrypted_value",
            sqlalchemy_utils.types.encrypted.encrypted_type.StringEncryptedType(),
            nullable=True,
        ),
        sa.ForeignKeyConstraint(
            ["privacy_request_id"],
            ["privacyrequest.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_providedidentity_hashed_value"),
        "providedidentity",
        ["hashed_value"],
        unique=False,
    )
    op.create_index(
        op.f("ix_providedidentity_id"), "providedidentity", ["id"], unique=False
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_providedidentity_id"), table_name="providedidentity")
    op.drop_index(
        op.f("ix_providedidentity_hashed_value"), table_name="providedidentity"
    )
    op.drop_table("providedidentity")
    # ### end Alembic commands ###
