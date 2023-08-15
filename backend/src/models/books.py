from sqlalchemy import Integer, Column, ForeignKey, String

from backend.src.models import Base


class Books(Base):
    __tablename__ = 'Books'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('Users.id'), nullable=False)
    name = Column(String(50), unique=True, nullable=False)
    Author = Column(String(50), unique=True, nullable=False)
    Publisher = Column(String(50), nullable=False)
    book_prize = Column(Integer)
