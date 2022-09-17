"""Add consent request

Revision ID: 021d288d0ce3
Revises: a0e6feb5bdc8
Create Date: 2022-09-17 01:26:43.187484

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '021d288d0ce3'
down_revision = 'a0e6feb5bdc8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('consentrequest',
    sa.Column('id', sa.String(length=255), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('provided_identity_id', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['provided_identity_id'], ['providedidentity.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_consentrequest_id'), 'consentrequest', ['id'], unique=False)
    op.alter_column('consent', 'provided_identity_id',
               existing_type=sa.VARCHAR(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('consent', 'provided_identity_id',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.drop_index(op.f('ix_consentrequest_id'), table_name='consentrequest')
    op.drop_table('consentrequest')
    # ### end Alembic commands ###
