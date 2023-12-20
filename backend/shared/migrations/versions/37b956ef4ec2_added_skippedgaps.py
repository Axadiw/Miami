"""Added SkippedGaps

Revision ID: 37b956ef4ec2
Revises: 9f938c4830e8
Create Date: 2023-12-08 13:18:55.455639

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '37b956ef4ec2'
down_revision: Union[str, None] = '9f938c4830e8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('SkippedGaps',
                    sa.Column('id', sa.BigInteger(), nullable=False),
                    sa.Column('symbol', sa.Integer(), nullable=False),
                    sa.Column('exchange', sa.Integer(), nullable=False),
                    sa.Column('timeframe', sa.Integer(), nullable=False),
                    sa.Column('start', sa.DateTime(), nullable=False),
                    sa.Column('end', sa.DateTime(), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    )
    with op.batch_alter_table("SkippedGaps") as batch_op:
        batch_op.create_unique_constraint('skippedgaps_unique_sett',
                                          ['symbol', 'exchange', 'timeframe', 'start', 'end'])


def downgrade() -> None:
    op.drop_table('SkippedGaps')
