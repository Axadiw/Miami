from sqlalchemy import Column, String, DateTime, Numeric, Integer, BigInteger, ForeignKey

from models import Base


class OpenInterest(Base):
    __tablename__ = 'OpenInterest'

    id = Column(Integer, primary_key=True)
    exchange = Column(Integer, ForeignKey('Exchanges.id'), nullable=False)
    symbol = Column(Integer, ForeignKey('Symbols.id'), nullable=False)
    timestamp = Column(DateTime(), nullable=False)
    value = Column(Numeric(scale=6, precision=20))
