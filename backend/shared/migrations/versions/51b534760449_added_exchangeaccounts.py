"""Added ExchangeAccounts

Revision ID: 51b534760449
Revises: 9b99ae6e607f
Create Date: 2024-03-10 13:51:40.978514

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '51b534760449'
down_revision: Union[str, None] = '9b99ae6e607f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('ExchangeAccounts',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('type', sa.String(length=255), nullable=False),
                    sa.Column('name', sa.String(length=255), nullable=False),
                    sa.Column('details', sa.String(length=4096), nullable=False),
                    sa.Column('user_id', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(['user_id'], ['Users.id'], ),
                    sa.PrimaryKeyConstraint('id'),
                    )


def downgrade() -> None:
    op.drop_table('ExchangeAccounts')
