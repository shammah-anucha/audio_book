from celery import Celery, Task
from backend.app.app.crud.s3 import s3_audio
from sqlalchemy.orm import Session
from fastapi import Depends
from backend.app.app.api.deps import get_db  # Import the function to get a new session
from backend.app.app.db.session import engine
from backend.app.app.models import models
from backend.app.app.crud import crud_audio
from datetime import datetime
from dotenv import load_dotenv
import os


load_dotenv(".env")

broker = os.getenv("broker")


app = Celery('tasks', broker=broker)


@app.task
def celery_save_audio_to_s3(book_id: int, file_name: str):
    db = Session(bind=engine)
    # Obtain a new session within the Celery task
    # db = Session()
    try:
        s3_audio.save_audio_to_s3(book_id=book_id, file_name=file_name, db=db)
        
    except Exception as e:
        print(f"Error in celery_save_audio_to_s3: {e}")


