"""add_execution_timeframe

Revision ID: bde646a6f51e
Revises: c2f7a29c4780
Create Date: 2022-09-01 15:46:47.954354

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bde646a6f51e'
down_revision = 'c2f7a29c4780'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('policy', sa.Column('execution_timeframe', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('policy', 'execution_timeframe')
    # ### end Alembic commands ###
