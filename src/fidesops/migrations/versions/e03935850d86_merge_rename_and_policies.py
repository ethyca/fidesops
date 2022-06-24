"""Merge rename and policies

Revision ID: e03935850d86
Revises: 46f7a577b933, 55d61eb8ed12
Create Date: 2022-06-24 12:31:43.540964

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e03935850d86'
down_revision = ('46f7a577b933', '55d61eb8ed12')
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
