from sqlalchemy import Column, String, Integer

from shared.models import Base


class Exchange(Base):
    __tablename__ = 'Exchanges'

    id = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False, index=True, unique=True)
