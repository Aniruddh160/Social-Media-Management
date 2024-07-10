"""new count

Revision ID: 194fd500b4ad
Revises: 97e41a4557df
Create Date: 2024-07-04 13:56:32.408985

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '194fd500b4ad'
down_revision: Union[str, None] = '97e41a4557df'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
