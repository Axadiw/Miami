from sqlalchemy import Column, String, DateTime, Numeric, Integer, BigInteger

from models import Base


class Exchanges(Base):
    __tablename__ = 'Exchanges'

    id = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False, index=True)
