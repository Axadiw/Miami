from sqlalchemy import Column, String, Integer, Boolean, Numeric, DateTime

from shared.models import Base

LONG_SIDE = 'Long'
SHORT_SIDE = 'Short'

CREATED_POSITION_STATE = 0
FINISHED_POSITION_STATE = 1
CANCELLED_POSITION_STATE = 2


def serialize_side(side: str):
    return 1 if side == LONG_SIDE else 0


def deserialize_side(serialized_side: int):
    return LONG_SIDE if serialized_side == 1 else SHORT_SIDE


class Position(Base):
    __tablename__ = 'Positions'

    id = Column(Integer, primary_key=True)
    side = Column(Integer, nullable=False)
    state = Column(Integer, nullable=False)
    create_date = Column(DateTime(), nullable=False)
    closed_date = Column(DateTime(), nullable=True)
    size = Column(Numeric(scale=10, precision=30))
    account_id = Column(Integer, nullable=False)
    comment = Column(String(length=4096), nullable=False)
    position_external_id = Column(String(length=64), nullable=False)
    helper_url = Column(String(length=4096), nullable=False)
    symbol = Column(Integer, nullable=False)
    move_sl_to_be = Column(Boolean, nullable=False)
    soft_stop_loss_timeout = Column(Integer, nullable=False)
