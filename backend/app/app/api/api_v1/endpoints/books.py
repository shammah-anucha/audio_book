from fastapi import APIRouter, Depends, File, UploadFile, HTTPException
from ....crud import crud_book
from ....schemas import books
from ....models import models
from ... import deps
from typing import List, Annotated
from sqlalchemy.orm import Session

from ....api.deps import get_current_user


router = APIRouter(prefix="/Books", tags=["Books"], dependencies=[Depends(deps.get_db)])

user_dependency = Annotated[dict, Depends(get_current_user)]


@router.post("/uploadbook/", response_model=books.Book)
def create_Book(
    current_user: user_dependency,
    file: UploadFile = File(...),
    db: Session = Depends(deps.get_db),
):
    if current_user is None:
        raise HTTPException(status_code=401, detail="Authentication required")
    return crud_book.Book.create_Book(db=db, obj_in=file, user_id=current_user["id"])


@router.get("/", response_model=List[books.Book])
def get_user_books(
    current_user: user_dependency,
    db: Session = Depends(deps.get_db),
):
    if current_user is None:
        raise HTTPException(status_code=401, detail="Authentication required")

    books = crud_book.Book.get_user_books(db=db, user_id=current_user["id"])
    return books


"""For personal use"""
# # works
# @router.get("/", response_model=List[books.Book])
# def read_Books(skip: int = 0, limit: int = 100, db: Session = Depends(deps.get_db)):
#     book = crud_book.Book.get_multi_Books(db, skip=skip, limit=limit)
#     return book

"""Not needed"""
# @router.get("/downloadbook/{book_id}")
# def download_book(book_id: int, db: Session = Depends(deps.get_db)):
#     return crud_book.Book.download_book(db=db, book_id=book_id)


"""For Development Purposes"""
# @router.get("/extract-text/{book_id}")
# def extract_text_from_pdf_endpoint(book_id: int, db: Session = Depends(deps.get_db)):
#     crud_book.Book.extract_text_from_pdf_in_db(db=db, book_id=book_id)
#     return {"message": "Text extraction complete, check command line output."}


@router.delete("/{book_id}")
def delete_book(
    current_user: user_dependency, book_id: int, db: Session = Depends(deps.get_db)
):
    if current_user is None:
        raise HTTPException(status_code=401, detail="Authentication required")
    return crud_book.Book.delete_book(
        book_id=book_id, db=db, user_id=current_user["id"]
    )
