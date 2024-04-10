"""Added Position and Orders

Revision ID: ae76810e7314
Revises: 51b534760449
Create Date: 2024-03-19 22:38:30.318525

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'ae76810e7314'
down_revision: Union[str, None] = '51b534760449'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('Positions',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('side', sa.Boolean(), nullable=False),
                    sa.Column('size', sa.Numeric(scale=10, precision=30), nullable=False),
                    sa.Column('state', sa.Integer(), nullable=False),
                    sa.Column('create_date', sa.DateTime(), nullable=False),
                    sa.Column('closed_date', sa.DateTime(), nullable=True),
                    sa.Column('account_id', sa.Integer, nullable=False),
                    sa.Column('comment', sa.String(length=4096), nullable=False),
                    sa.Column('position_external_id', sa.String(length=64), nullable=False),
                    sa.Column('helper_url', sa.String(length=4096), nullable=False),
                    sa.Column('symbol', sa.Integer, nullable=False),  # pomyslec
                    sa.Column('move_sl_to_be', sa.Boolean(), nullable=False),
                    sa.Column('soft_stop_loss_timeout', sa.Integer, nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    )
    op.create_table('Orders',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('type', sa.Integer(), nullable=False),
                    sa.Column('state', sa.Integer(), nullable=False),
                    sa.Column('create_date', sa.DateTime(), nullable=False),
                    sa.Column('closed_date', sa.DateTime(), nullable=True),
                    sa.Column('name', sa.String(length=255), nullable=False),
                    sa.Column('price', sa.Numeric(scale=10, precision=30), nullable=False),
                    sa.Column('amount', sa.Numeric(scale=10, precision=30), nullable=True),
                    sa.Column('position_id', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(['position_id'], ['Positions.id'], ),
                    sa.PrimaryKeyConstraint('id'),
                    )


def downgrade() -> None:
    op.drop_table('ExchangeAccounts')
