from pydantic import BaseModel
from fastapi import UploadFile
from typing import Optional


class BookBase(BaseModel):
    book_name: str
    book_file: str
    book_image: str


class BookCreate(BookBase):
    pass


class BookUpdate(BookBase):
    pass


class BookInDBBase(BaseModel):
    book_id: int
    book_name: str
    book_file: str
    book_image: Optional[str]

    class Config:
        orm_mode = True


class Book(BookInDBBase):
    pass


class BookInDB(BookInDBBase):
    pass
