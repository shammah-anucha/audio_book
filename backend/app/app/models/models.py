from typing import TYPE_CHECKING

from sqlalchemy import LargeBinary, Column, Integer, ForeignKey, VARCHAR, Text
from ..db.base_class import Base



class Users(Base):

    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True,autoincrement=True)
    email = Column(VARCHAR(30), unique=True, index=True)
    hashed_password = Column(Text)
    Firstname = Column(VARCHAR(30), index=True)
    Lastname = Column(VARCHAR(30), index=True)
    country_of_residence = Column(VARCHAR(30), index=True)



class Books(Base):

    __tablename__ = "books"

    book_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"),nullable=False)
    book_name = Column(VARCHAR(80))
    book_file = Column(LargeBinary)


class Audio(Base):
    __tablename__ = "audio"

    audio_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    book_id = Column(Integer, ForeignKey("books.book_id"))
    audio_file = Column(LargeBinary)
