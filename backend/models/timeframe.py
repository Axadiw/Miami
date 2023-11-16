from sqlalchemy import Column, String, DateTime, Numeric, Integer, BigInteger

from models import Base


class Timeframe(Base):
    __tablename__ = 'Timeframes'

    id = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False, index=True, unique=True)
    seconds = Column(Integer, nullable=False, unique=True)
