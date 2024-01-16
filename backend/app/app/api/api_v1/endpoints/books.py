from fastapi import APIRouter, Depends, File, UploadFile, HTTPException
from ....crud import crud_book
from ....schemas import books
from ....models import models
from ... import deps
from typing import List
from sqlalchemy.orm import Session
from fastapi.responses import StreamingResponse

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
    db_book = crud_book.Book.get_book_id(db=db, id=book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    book_file = db.query(models.Books.book_file).filter(models.Books.book_id == book_id).first()
    book_name = db.query(models.Books.book_name).filter(models.Books.book_id == book_id).first()

    if not book_file or not book_name:
        raise HTTPException(status_code=404, detail="Book file or name not found")

    content: bytes = book_file[0]  # Assuming book_file is a bytes-like object
    filename: str = book_name[0]    # Assuming book_name is a string

    def generate():
        yield content

    return StreamingResponse(content=generate(), media_type="application/pdf", headers={"Content-Disposition": f'attachment; filename="{filename}"'})
