"""Change Users password length

Revision ID: c3667a09d1c9
Revises: 0f68abd19fd9
Create Date: 2023-11-08 15:44:22.239711

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import Column

# revision identifiers, used by Alembic.
revision: str = 'c3667a09d1c9'
down_revision: Union[str, None] = '0f68abd19fd9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # pass
    with op.batch_alter_table("Users") as batch_op:
        batch_op.alter_column('password', type_=sa.String(length=170), existing_type=sa.String(length=110))


def downgrade() -> None:
    pass
