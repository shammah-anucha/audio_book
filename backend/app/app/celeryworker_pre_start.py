from celery import Celery, Task
from backend.app.app.crud.s3 import s3_audio
from sqlalchemy.orm import Session
from fastapi import Depends
from backend.app.app.api.deps import get_db  # Import the function to get a new session
from backend.app.app.db.session import engine
from backend.app.app.models import models
from backend.app.app.crud import crud_audio
from datetime import datetime


app = Celery('tasks', broker='amqps://crzdkstj:G-hUTDewvxVDPquGMVXbX6iUU_ph1Q7b@sparrow.rmq.cloudamqp.com/crzdkstj')


@app.task
def celery_save_audio_to_s3(book_id: int, file_name: str):
    db = Session(bind=engine)
    # Obtain a new session within the Celery task
    # db = Session()
    try:
        s3_audio.save_audio_to_s3(book_id=book_id, file_name=file_name, db=db)
        
    except Exception as e:
        print(f"Error in celery_save_audio_to_s3: {e}")


# class SaveResultTask(Task):
#     name='save_result_task'
#     def on_success(self, retval, task_id, args, kwargs):
#         try:
#             db = Session(bind=engine)
#             book_id, file_name = args  # Unpack the arguments
#             task_name = "celery_save_audio_to_s3"

#             # Retrieve the actual result of the task
#             result = app.AsyncResult(task_id)
#             celery_task_result = result.result if result.ready() else "pending.."

#             # Get necessary information from the database
#             audio_id = db.query(models.Audio.audio_id).filter(models.Books.book_id == book_id).first()[0]
#             user_id = db.query(models.Audio.user_id).filter(models.Books.book_id == book_id).first()[0]

#             # Create a CeleryResult instance and save it to the database
#             task_result = models.CeleryResult(
#                 audio_id=audio_id,
#                 user_id=user_id,
#                 task_id=task_id,
#                 book_id=book_id,
#                 task_name=task_name,
#                 result=celery_task_result,
#                 finished_at=datetime.utcnow()
#             )
            
#             db.add(task_result)
#             db.commit()
#         finally:
#             db.close()


