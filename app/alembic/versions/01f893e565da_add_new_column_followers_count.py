"""Add new column followers_count

Revision ID: 01f893e565da
Revises: 194fd500b4ad
Create Date: 2024-07-04 13:58:33.476868

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '01f893e565da'
down_revision: Union[str, None] = '194fd500b4ad'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('Users', sa.Column('followers_count', sa.Integer(), nullable=False, server_default='0'))


def downgrade():
    op.drop_column('Users', 'followers_count')