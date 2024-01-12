from datetime import time, date

from pydantic import BaseModel


class BookBase(BaseModel):
    book_name: str
    book_file: str



class BookCreate(BookBase):
    name: str


class BookUpdate(BookBase):
    pass


class BookInDBBase(BookBase):
    book_id: int
    # user_id: int

    class Config:
        orm_mode = True


# Properties to return to client
class Book(BookInDBBase):
    pass


# Properties properties stored in DB
class BookInDB(BookInDBBase):
    pass
