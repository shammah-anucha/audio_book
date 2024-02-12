from curses import echo
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ....config import settings
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine(settings.SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
