from sqlalchemy import Column, DateTime, Integer, ForeignKey

from models import Base


class LastFetchedDate(Base):
    __tablename__ = 'LastFetchedDates'

    id = Column(Integer, primary_key=True)
    exchange = Column(Integer, ForeignKey('Exchanges.id'), nullable=False)
    symbol = Column(Integer, ForeignKey('Symbols.id'), nullable=False)
    timeframe = Column(Integer, ForeignKey('Timeframes.id'), nullable=False)
    last_fetched = Column(DateTime(), nullable=False)
