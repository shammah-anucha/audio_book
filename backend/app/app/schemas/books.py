from pydantic import BaseModel
from fastapi import UploadFile

class BookBase(BaseModel):
    book_name: str
    book_file: str 
    # book_file: Optional[UploadFile] = None

class BookCreate(BookBase):
    pass

class BookUpdate(BookBase):
    pass

class BookInDBBase(BaseModel):
    book_id: int   
    book_name: str
    book_file: str  

    class Config:
        orm_mode = True

class Book(BookInDBBase):
    pass

class BookInDB(BookInDBBase):
    pass
