from sqlalchemy import Column, String, Integer, Boolean

from shared.models import Base


class ExchangeAccount(Base):
    __tablename__ = 'ExchangeAccounts'

    id = Column(Integer, primary_key=True)
    type = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False)
    details = Column(String(4096), nullable=False)
    user_id = Column(Integer, nullable=False)
