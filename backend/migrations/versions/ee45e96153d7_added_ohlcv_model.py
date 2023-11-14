"""Added ohlcv model

Revision ID: ee45e96153d7
Revises: c3667a09d1c9
Create Date: 2023-11-10 23:00:56.073299

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'ee45e96153d7'
down_revision: Union[str, None] = 'c3667a09d1c9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('Exchanges',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('name', sa.String(length=20), nullable=False),
                    sa.UniqueConstraint('name'),
                    sa.PrimaryKeyConstraint('id'),
                    )

    op.create_table('Symbols',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('name', sa.String(length=255), nullable=False),
                    sa.UniqueConstraint('name'),
                    sa.PrimaryKeyConstraint('id'),
                    )

    op.create_table('Timeframes',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('name', sa.String(length=20), nullable=False),
                    sa.Column('seconds', sa.Integer(), nullable=False),
                    sa.UniqueConstraint('name'),
                    sa.UniqueConstraint('seconds'),
                    sa.PrimaryKeyConstraint('id'),
                    )

    op.create_table('OHLCV',
                    sa.Column('id', sa.BigInteger(), nullable=False),
                    sa.Column('symbol', sa.Integer(), nullable=False),
                    sa.Column('exchange', sa.Integer(), nullable=False),
                    sa.Column('timeframe', sa.Integer(), nullable=False),
                    sa.Column('timestamp', sa.DateTime(), nullable=False),
                    sa.Column('open', sa.Numeric(scale=20, precision=40), nullable=False),
                    sa.Column('high', sa.Numeric(scale=20, precision=40), nullable=False),
                    sa.Column('low', sa.Numeric(scale=20, precision=40), nullable=False),
                    sa.Column('close', sa.Numeric(scale=20, precision=40), nullable=False),
                    sa.Column('volume', sa.Numeric(scale=20, precision=40), nullable=False),
                    sa.ForeignKeyConstraint(['symbol'], ['Symbols.id'], ),
                    sa.ForeignKeyConstraint(['exchange'], ['Exchanges.id'], ),
                    sa.ForeignKeyConstraint(['timeframe'], ['Timeframes.id'], ),
                    sa.PrimaryKeyConstraint('id'),
                    )


def downgrade() -> None:
    op.drop_table('OHLCV')
    op.drop_table('Exchanges')
    op.drop_table('Symbols')
    op.drop_table('Timeframes')
