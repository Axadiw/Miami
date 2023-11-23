"""Added funding and openinterest

Revision ID: 9f938c4830e8
Revises: ee45e96153d7
Create Date: 2023-11-22 13:47:46.084538

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '9f938c4830e8'
down_revision: Union[str, None] = 'ee45e96153d7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('Funding',
                    sa.Column('id', sa.BigInteger(), nullable=False),
                    sa.Column('symbol', sa.Integer(), nullable=False),
                    sa.Column('exchange', sa.Integer(), nullable=False),
                    sa.Column('timestamp', sa.DateTime(), nullable=False),
                    sa.Column('value', sa.Numeric(scale=6, precision=9), nullable=False),
                    sa.ForeignKeyConstraint(['symbol'], ['Symbols.id'], ),
                    sa.ForeignKeyConstraint(['exchange'], ['Exchanges.id'], ),
                    sa.PrimaryKeyConstraint('id'),
                    )
    with op.batch_alter_table("Funding") as batch_op:
        batch_op.create_unique_constraint('funding_unique_sett', ['symbol', 'exchange', 'timestamp'])

    op.create_table('OpenInterest',
                    sa.Column('id', sa.BigInteger(), nullable=False),
                    sa.Column('symbol', sa.Integer(), nullable=False),
                    sa.Column('exchange', sa.Integer(), nullable=False),
                    sa.Column('timestamp', sa.DateTime(), nullable=False),
                    sa.Column('value', sa.Numeric(scale=6, precision=20), nullable=False),
                    sa.ForeignKeyConstraint(['symbol'], ['Symbols.id'], ),
                    sa.ForeignKeyConstraint(['exchange'], ['Exchanges.id'], ),
                    sa.PrimaryKeyConstraint('id'),
                    )
    with op.batch_alter_table("OpenInterest") as batch_op:
        batch_op.create_unique_constraint('oi_unique_sett', ['symbol', 'exchange', 'timestamp'])


def downgrade() -> None:
    op.drop_table('Funding')
    op.drop_table('OpenInterest')
