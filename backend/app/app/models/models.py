from typing import TYPE_CHECKING, List

from sqlalchemy import (
    LargeBinary,
    Column,
    Integer,
    ForeignKey,
    VARCHAR,
    Text,
    DateTime,
    func,
)
from ..db.base_class import Base


class Users(Base):

    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(VARCHAR(30), unique=True, index=True)
    hashed_password = Column(Text)
    Firstname = Column(VARCHAR(30), index=True)
    Lastname = Column(VARCHAR(30), index=True)
    country_of_residence = Column(VARCHAR(30), index=True)


class Books(Base):

    __tablename__ = "books"

    book_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    book_name = Column(VARCHAR(80), nullable=False)
    book_file = Column(Text, nullable=False)
    book_image = Column(Text)


class Audio(Base):
    __tablename__ = "audio"

    audio_id = Column(Integer, primary_key=True, index=True)
    audio_name = Column(Text)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    book_id = Column(Integer, ForeignKey("books.book_id"))
    audio_file = Column(Text, nullable=False)


class CeleryResult(Base):
    __tablename__ = "celery_result"

    table_id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer)
    audio_id = Column(Integer, ForeignKey("users.user_id"))
    user_id = Column(Integer, ForeignKey("users.user_id"))
    book_id = Column(Integer, ForeignKey("books.book_id"))
    task_name = Column(Text, nullable=False)
    result = Column(Text, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    finished_at = Column(DateTime, default=None, nullable=True)
