from typing import List, Annotated
from fastapi import UploadFile, HTTPException, Depends
from sqlalchemy.orm import Session
from .base import CRUDBase
from ..models import models
from ..schemas.books import BookCreate, BookUpdate
import pdfplumber
from fastapi import UploadFile
from .s3 import s3_book
from . import crud_users
from .pdf_to_image import convert_pdf_to_image
import tempfile
import os


class CRUDBook(CRUDBase[models.Books, BookCreate, BookUpdate]):

    def create_Book(self, db: Session, obj_in: UploadFile, user_id: int):
        image = convert_pdf_to_image(file=obj_in)
        # print(image)
        max_file_size = 5 * 1024 * 1024
        db_user = crud_users.user.get_user_id(db, id=user_id)

        # Check if the file size exceeds the limit
        if obj_in.size > max_file_size:
            raise HTTPException(
                status_code=413,
                detail="File size is too large. The Maximum File size is 5MB",
            )

        # Check if the seek operation moved the pointer to the correct position
        # assert obj_in.tell() == 0

        if db_user is None:
            raise HTTPException(status_code=404, detail="User not found")

        if not obj_in.filename.lower().endswith(".pdf"):
            raise HTTPException(status_code=404, detail="Please upload PDF")

        try:
            obj_in.file.seek(0)
            url = s3_book.upload_book_to_s3(file=obj_in)
            # url = "test"

            db_file = models.Books(
                book_name=obj_in.filename,
                book_file=url,
                user_id=user_id,
                book_image=image,
            )
            db.add(db_file)
            db.commit()
            db.refresh(db_file)
            return db_file
        finally:
            db.close()

    def get_book_id(self, db: Session, id: int):
        return db.query(models.Books).filter(models.Books.book_id == id).first()

    # def download_book(self, db: Session, book_id: int):
    #     db_book = Book.get_book_id(db=db, id=book_id)
    #     if not db_book:
    #         raise HTTPException(status_code=404, detail="Book not found")

    #     book_file = db.query(models.Books.book_file).filter(models.Books.book_id == book_id).first()
    #     book_name = db.query(models.Books.book_name).filter(models.Books.book_id == book_id).first()

    #     if not book_file or not book_name:
    #         raise HTTPException(status_code=404, detail="Book file or name not found")

    #     content: bytes = book_file[0]  # Assuming book_file is a bytes-like object
    #     filename: str = book_name[0]    # Assuming book_name is a string

    #     def generate():
    #         yield content

    #     return StreamingResponse(content=generate(), media_type="application/pdf", headers={"Content-Disposition": f'attachment; filename="{filename}"'})

    def remove_extra(text):
        pass

    def extract_text_from_pdf_in_db(self, db: Session, book_id: int):
        db_book = Book.get_book_id(db=db, id=book_id)
        if not db_book:
            raise HTTPException(status_code=404, detail="Book not found")

        # Retrieve the PDF url from the database
        pdf_url = (
            db.query(models.Books.book_file)
            .filter(models.Books.book_id == book_id)
            .first()[0]
        )

        pdf_content = s3_book.download_object_from_s3(pdf_url)

        # Split the text
        with pdfplumber.open(pdf_content) as pdf:
            text_list = []
            step_size = 10
            # total_pages =Book.remove_extra(pdf)
            total_pages = len(pdf.pages)

            for start_page in range(1, total_pages, step_size):
                end_page = min(start_page + step_size - 1, total_pages)

                text = ""
                for page_number in range(start_page, end_page + 1):
                    page = pdf.pages[page_number - 1]
                    text += page.extract_text()
                text_list.append(text)

        return text_list

        # Extracting a single text
        # ----------------------------
        # if 0 < page_number <= len(pdf.pages):
        #     # Get the specified page
        #     page = pdf.pages[page_number - 1]

        #     # Extract text from the page
        #     text = page.extract_text()

        #     # Print the text on the command line
        #     return text

        # else:
        #     return "Invalid page number"

    # # Example usage in your FastAPI endpoint
    # @router.get("/extract-text/{pdf_id}/{page_number}")
    # def extract_text_from_pdf_endpoint(pdf_id: int, page_number: int, db: Session = Depends(get_db)):
    #     extract_text_from_pdf_in_db(db, pdf_id, page_number)
    #     return {"message": "Text extraction complete, check command line output."}

    def get_user_books(self, db: Session, user_id: int) -> List[models.Books]:
        db_user_book = (
            db.query(models.Books).filter(models.Books.user_id == user_id).all()
        )
        return db_user_book

    """For personal use"""
    # def get_multi_Books(
    #     self, db: Session, *, skip: int = 0, limit: int = 100
    # ) -> List[models.Books]:
    #     return db.query(self.model).offset(skip).limit(limit).all()

    def delete_book(self, db: Session, book_id: int, user_id: int):
        db_book = Book.get_book_id(db=db, id=book_id)
        db_user_id = (
            db.query(models.Books.user_id)
            .filter(models.Books.book_id == book_id)
            .first()[0]
        )
        if not db_book:
            raise HTTPException(status_code=404, detail="Book not found")
        if user_id != db_user_id:
            raise HTTPException(status_code=404, detail="Book does not belong to you")

        else:
            s3_book.delete_book_from_s3(db=db, book_id=book_id)
            db.query(models.Books).filter(models.Books.book_id == book_id).delete()
            db.commit()
            return "Delete Successful"


Book = CRUDBook(models.Books)
