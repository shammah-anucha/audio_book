from typing import Optional, List
from datetime import date
from .audio import Audio
from .books import Book
from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: EmailStr
    Firstname: Optional[str]
    Lastname: Optional[str]
    country_of_residence: Optional[str]


# Properties to receive via API on creation
class UserCreate(UserBase):
    email: EmailStr
    password: str


# Properties to receive via API on update
class UserUpdate(UserBase):
    password: Optional[str] = None


class UserInDBBase(UserBase):
    user_id: int
    book: List[Book] = []
    audio: List[Audio] = []

    class Config:
        orm_mode = True


# Additional properties to return via API
class User(UserInDBBase):
    pass


# Additional properties stored in DB
class UserInDB(UserInDBBase):
    hashed_password: str
