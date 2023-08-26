"""Many to many relationship

Revision ID: 5a23a708ec71
Revises: 3cd17a0f5b5a
Create Date: 2023-08-25 23:55:34.693601

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5a23a708ec71'
down_revision: Union[str, None] = '3cd17a0f5b5a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
