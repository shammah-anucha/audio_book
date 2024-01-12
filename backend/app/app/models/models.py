from typing import TYPE_CHECKING

from sqlalchemy import Binary, Column, Integer, String
from sqlalchemy.orm import relationship

from ...app.db.base_class import Base

# from ...app.models.unavailability import Unavailabilities
from sqlalchemy import Column, Integer, Date, ForeignKey, Time



class Users(Base):

   class Users(Base):

    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    Firstname = Column(String, index=True)
    Lastname = Column(String, index=True)
    country_of_residence = Column(String, index=True)



class Books(Base):

    __tablename__ = "books"

    book_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    book_name = Column(String)
    book_file = Column(Binary)


class Audio(Base):
    __tablename__ = "audio"

    audio_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    book_id = Column(Integer, ForeignKey("books.book_id"))
    audio_name = Column(String)
    audio_file = Column(Binary)
