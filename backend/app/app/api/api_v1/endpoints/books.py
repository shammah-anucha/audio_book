from fastapi import APIRouter, Depends, File, UploadFile
from ....crud import crud_book
from ....schemas import books
from ... import deps
from typing import List
from sqlalchemy.orm import Session


router = APIRouter(
    prefix="/Books", tags=["Books"], dependencies=[Depends(deps.get_db)]
)

# works
@router.post("/uploadbook", response_model=books.Book)
def create_Book(user_id: int, file: UploadFile=File(...),  db: Session = Depends(deps.get_db)):
    return crud_book.Book.create_Book(db=db, obj_in=file, user_id=user_id)


# works
@router.get("/", response_model=List[books.Book])
def read_Books(skip: int = 0, limit: int = 100, db: Session = Depends(deps.get_db)):
    roster = crud_book.Book.get_multi_Books(db, skip=skip, limit=limit)
    return roster



@router.get("/downloadbook/{book_id}")
def download_book(book_id: int, db: Session = Depends(deps.get_db)):
    return crud_book.Book.download_book(db=db, book_id=book_id)
