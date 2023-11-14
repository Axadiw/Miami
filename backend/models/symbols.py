from sqlalchemy import Column, String, DateTime, Numeric, Integer, BigInteger

from models import Base


class Symbols(Base):
    __tablename__ = 'Symbols'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, index=True, unique=True)
