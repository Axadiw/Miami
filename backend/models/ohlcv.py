from sqlalchemy import Column, String, DateTime, Numeric, Integer, BigInteger, ForeignKey

from models import Base


class OHLCV(Base):
    __tablename__ = 'OHLCV'

    id = Column(Integer, primary_key=True)
    exchange = Column(Integer, ForeignKey('Exchanges.id'), nullable=False)
    symbol = Column(Integer, ForeignKey('Symbols.id'), nullable=False)
    timeframe = Column(Integer, ForeignKey('Timeframes.id'), nullable=False)
    timestamp = Column(DateTime(), nullable=False)
    open = Column(Numeric(scale=7, precision=22))
    high = Column(Numeric(scale=7, precision=22))
    low = Column(Numeric(scale=7, precision=22))
    close = Column(Numeric(scale=7, precision=22))
    volume = Column(Numeric(scale=7, precision=22))
