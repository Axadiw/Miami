from sqlalchemy import Column, String, DateTime, Numeric, Integer, BigInteger, ForeignKey

from models import Base


class Symbol(Base):
    __tablename__ = 'Symbols'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, index=True, unique=True)
    exchange = Column(Integer, nullable=False)
