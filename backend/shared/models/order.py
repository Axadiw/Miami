from sqlalchemy import Column, String, Integer, Boolean, Numeric, DateTime

from shared.models import Base

STANDARD_ORDER_TYPE = 0
STOP_LOSS_ORDER_TYPE = 1
TAKE_PROFIT_ORDER_TYPE = 2

CREATED_ORDER_STATE = 0
FILLED_ORDER_STATE = 1
PARTIALLY_FILLED_ORDER_STATE = 2
CANCELLED_ORDER_STATE = 3


class Order(Base):
    __tablename__ = 'Orders'

    id = Column(Integer, primary_key=True)
    type = Column(Integer, nullable=False)
    state = Column(Integer, nullable=False)
    create_date = Column(DateTime(), nullable=False)
    closed_date = Column(DateTime(), nullable=True)
    name = Column(String(length=255), nullable=False)
    price = Column(Numeric(scale=10, precision=30), nullable=False)
    amount = Column(Numeric(scale=10, precision=30), nullable=True)
    position_id = Column(Integer, nullable=False)
