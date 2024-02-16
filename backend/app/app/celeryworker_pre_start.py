""" Add celery in version 2"""

# from celery import Celery
# from backend.app.app.crud.s3 import s3_audio
# from sqlalchemy.orm import Session
# from backend.app.app.db.session import engine
# from dotenv import load_dotenv
# import os


# load_dotenv(".env")

# broker = os.getenv("broker")


# app = Celery("tasks", broker=broker)


# @app.task
# def celery_save_audio_to_s3(book_id: int, file_name: str):
#     db = Session(bind=engine)
#     # Obtain a new session within the Celery task
#     try:
#         s3_audio.save_audio_to_s3(book_id=book_id, file_name=file_name, db=db)

#     except Exception as e:
#         print(f"Error in celery_save_audio_to_s3: {e}")
