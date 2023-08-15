from sqlalchemy import Column, Integer, String, ForeignKey

from backend.src.models import Base


class UserConfigs(Base):
    __tablename__ = 'UserConfigs'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('Users.id'), nullable=False)
    key = Column(String(255), nullable=False)
    value = Column(String(255), nullable=False)
