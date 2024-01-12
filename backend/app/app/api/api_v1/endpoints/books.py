from fastapi import APIRouter, Depends
from ....crud import crud_book
from ....schemas import books
from ... import deps
from typing import List
from sqlalchemy.orm import Session


router = APIRouter(
    prefix="/Books", tags=["Books"], dependencies=[Depends(deps.get_db)]
)

# works
@router.post("/", response_model=books.Book)
def create_Book(Book: books.BookCreate, db: Session = Depends(deps.get_db)):
    return crud_book.Book.create_Book(db=db, obj_in=Book)


# works
@router.get("/", response_model=List[books.Book])
def read_Books(skip: int = 0, limit: int = 100, db: Session = Depends(deps.get_db)):
    roster = crud_book.Book.get_multi_Books(db, skip=skip, limit=limit)
    return roster
