"""add identity data to privacy_request

Revision ID: cdaac83e0a68
Revises: fc90277bbcde
Create Date: 2022-07-08 09:02:11.717954

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cdaac83e0a68'
down_revision = 'fc90277bbcde'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('privacyrequest', sa.Column('identity_email', sa.String(), nullable=True))
    op.add_column('privacyrequest', sa.Column('identity_phone_number', sa.String(), nullable=True))
    op.create_index(op.f('ix_privacyrequest_identity_email'), 'privacyrequest', ['identity_email'], unique=False)
    op.create_index(op.f('ix_privacyrequest_identity_phone_number'), 'privacyrequest', ['identity_phone_number'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_privacyrequest_identity_phone_number'), table_name='privacyrequest')
    op.drop_index(op.f('ix_privacyrequest_identity_email'), table_name='privacyrequest')
    op.drop_column('privacyrequest', 'identity_phone_number')
    op.drop_column('privacyrequest', 'identity_email')
    # ### end Alembic commands ###
