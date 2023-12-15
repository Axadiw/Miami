from sqlalchemy import Column, String, DateTime, Numeric, Integer, BigInteger, ForeignKey

from models import Base


class OHLCV(Base):
    __tablename__ = 'OHLCV'

    id = Column(Integer, primary_key=True)
    exchange = Column(Integer, nullable=False)
    symbol = Column(Integer, nullable=False)
    timeframe = Column(Integer, nullable=False)
    timestamp = Column(DateTime(), nullable=False)
    open = Column(Numeric(scale=10, precision=30))
    high = Column(Numeric(scale=10, precision=30))
    low = Column(Numeric(scale=10, precision=30))
    close = Column(Numeric(scale=10, precision=30))
    volume = Column(Numeric(scale=10, precision=30))

    def __repr__(self):
        return f'Symbol: {self.symbol} TF:{self.timeframe} Timestamp{str(self.timestamp)}'
