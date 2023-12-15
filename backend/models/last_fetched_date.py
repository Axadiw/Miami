from sqlalchemy import Column, DateTime, Integer, ForeignKey

from models import Base


class LastFetchedDate(Base):
    __tablename__ = 'LastFetchedDates'

    id = Column(Integer, primary_key=True)
    exchange = Column(Integer, nullable=False)
    symbol = Column(Integer, nullable=False)
    timeframe = Column(Integer, nullable=False)
    last_fetched = Column(DateTime(), nullable=False)
