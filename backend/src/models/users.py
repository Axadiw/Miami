from sqlalchemy import Column, String, Integer, Boolean

from backend.src.models import Base


class Users(Base):
    __tablename__ = 'Users'

    id = Column(Integer, primary_key=True)
    public_id = Column(Integer)
    name = Column(String(50), nullable=False, unique=True)
    password = Column(String(90), nullable=False)
    admin = Column(Boolean)
