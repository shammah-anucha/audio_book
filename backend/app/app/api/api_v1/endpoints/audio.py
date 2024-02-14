# from fastapi import APIRouter, Depends
# from ... import deps
# from sqlalchemy.orm import Session
# from ....crud.s3 import s3_audio
# from ....schemas import audio
# from ....models import models
# from typing import List
# from ....crud import crud_audio
# from ....celeryworker_pre_start import celery_save_audio_to_s3
# from fastapi import FastAPI, Depends, HTTPException


# router = APIRouter(
#     prefix="/audios", tags=["audios"], dependencies=[Depends(deps.get_db)]
# )


# @router.post("/audios/text_to_audio/{book_id}")
# def text_to_audio(book_id: int, file_name: str):
#     try:
#         # Enqueue the Celery task
#         celery_save_audio_to_s3.delay(book_id=book_id, file_name=file_name)
#         return 'Task enqueued successfully'
#     except Exception as e:
#         # Handle exceptions if needed
#         print(f"Error in text_to_audio: {e}")
#         raise HTTPException(status_code=500, detail="Internal Server Error")

# # @router.post("/text_to_audio/{book_id}")
# # def text_to_audio(book_id: int, file_name: str, db: Session = Depends(deps.get_db)):
# #     # Post audio streams
# #     s3_audio.save_audio_to_s3(book_id=book_id, file_name=file_name, db=db)
# #     return 'Saved successfully'

# # works
# @router.get("/", response_model=List[audio.Audio])
# def read_Audio(skip: int = 0, limit: int = 100, db: Session = Depends(deps.get_db)):
#     audio = crud_audio.Audio.get_multi_Audios(db, skip=skip, limit=limit)
#     return audio

# @router.delete("/{audio_id}")
# def delete_audio(audio_id: int, db: Session = Depends(deps.get_db)):
#     return crud_audio.Audio.delete_audio(audio_id=audio_id,db=db)
