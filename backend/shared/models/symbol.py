from sqlalchemy import Column, String, Integer

from shared.models import Base


class Symbol(Base):
    __tablename__ = 'Symbols'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, index=True, unique=True)
    exchange = Column(Integer, nullable=False)
