"""Init Bemi

Revision ID: a925526dcc3b
Revises: 6d5d277f6ffc
Create Date: 2024-05-22 12:10:48.503660

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from bemi import Bemi

# revision identifiers, used by Alembic.
revision: str = 'a925526dcc3b'
down_revision: Union[str, None] = '6d5d277f6ffc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    Bemi.migration_upgrade()

def downgrade() -> None:
    Bemi.migration_downgrade()
