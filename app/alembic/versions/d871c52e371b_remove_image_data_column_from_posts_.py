"""Remove image_data column from Posts_image

Revision ID: d871c52e371b
Revises: 01f893e565da
Create Date: 2024-07-09 15:28:12.799665

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd871c52e371b'
down_revision: Union[str, None] = '01f893e565da'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.drop_column('Posts_image', 'image_data')

def downgrade():
    op.add_column('Posts_image', sa.Column('image_data', sa.LargeBinary(), nullable=True))