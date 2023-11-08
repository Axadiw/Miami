from sqlalchemy import Column, String, Integer, Boolean

from models import Base


class Users(Base):
    __tablename__ = 'Users'

    id = Column(Integer, primary_key=True)
    public_id = Column(String(36), nullable=False, unique=True)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(170), nullable=False)
    email = Column(String(255), nullable=False)
    admin = Column(Boolean, default=False)
