from sqlalchemy import Column, DateTime, Numeric, Integer, ForeignKey

from models import Base


class Funding(Base):
    __tablename__ = 'Funding'

    id = Column(Integer, primary_key=True)
    exchange = Column(Integer, ForeignKey('Exchanges.id'), nullable=False)
    symbol = Column(Integer, ForeignKey('Symbols.id'), nullable=False)
    timestamp = Column(DateTime(), nullable=False)
    value = Column(Numeric(scale=6, precision=9), nullable=False)
