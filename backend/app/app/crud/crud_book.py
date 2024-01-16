from typing import List
from PyPDF2 import PdfReader
from fastapi import APIRouter, Depends, File, UploadFile, HTTPException
from ..crud import crud_book
from ..schemas import books
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from fastapi import File, UploadFile
from .base import CRUDBase
from ..models import models
from ..schemas.books import BookCreate, BookUpdate
from fastapi.responses import StreamingResponse



class CRUDBook(CRUDBase[models.Books, BookCreate, BookUpdate]):
    def pdf_to_text(pdf_path):
        pdf_path = "backend/app/app/api/api_v1/endpoints/The-Frog-Prince-Landscape-Book-CKF-FKB.pdf"
        text = ''
        with open(pdf_path, 'rb') as file:
            pdf_reader = PdfReader(file)
            for page_num in range(len(pdf_reader.pages)):
                text += pdf_reader.pages[page_num].extract_text()
        return text


    # def create_Book(self, db: Session, *, file: UploadFile, ) -> models.Books:
    #     try:
    #         content = file.file.read()
    #         db_file = File(filename=file.filename, content=content)
    #         db.add(db_file)
    #         db.commit()
    #         db.refresh(db_file)
    #     finally:
    #         db.close()
    #     return db_file
    
    def create_Book(self, db: Session, obj_in: UploadFile, user_id: int):
        try:
            content = obj_in.file.read()
            db_file = models.Books(book_name=obj_in.filename, book_file=content,user_id=user_id)
            print(db_file)
            db.add(db_file)
            db.commit()
            db.refresh(db_file)
            return db_file
        finally:
            db.close()

    
    
    def get_book_id(self, db: Session, id: int):
        return db.query(models.Books).filter(models.Books.book_id == id).first()
    

    def download_book(self, db: Session, book_id: int):
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

        
        
        # text = ''
        # with open(pdf_path, 'rb') as file:
        #     pdf_reader = PdfReader(file)
        #     # for page_num in range(len(pdf_reader.pages)):
        #     #     text += pdf_reader.pages[page_num].extract_text()
        # db.add(db_obj)
        # db.commit()
        # db.refresh(db_obj)
        # return obj_in.book_file.filename

    def get_multi_Books(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[models.Books]:
        return db.query(self.model).offset(skip).limit(limit).all()


Book = CRUDBook(models.Books)
