from fastapi import APIRouter, Depends
from ... import deps
from sqlalchemy.orm import Session
from ....crud.s3 import s3_audio
from ....schemas import audio
from ....models import models
from typing import List, Annotated
from ....crud import crud_audio

# for version 2
# from ....celeryworker_pre_start import celery_save_audio_to_s3
from fastapi import Depends, HTTPException
from ....api.deps import get_current_user


router = APIRouter(
    prefix="/audios", tags=["audios"], dependencies=[Depends(deps.get_db)]
)

user_dependency = Annotated[dict, Depends(get_current_user)]


@router.post("/text_to_audio/{book_id}")
def text_to_audio(
    current_user: user_dependency,
    book_id: int,
    file_name: str,
    db: Session = Depends(deps.get_db),
):
    if current_user is None:
        raise HTTPException(status_code=401, detail="Authentication required")
    # try:

    # Post audio streams
    s3_audio.save_audio_to_s3(
        book_id=book_id, file_name=file_name, db=db, user_id=current_user["id"]
    )
    return "Saved successfully"

    # except Exception as e:
    #     # Handle exceptions if needed
    #     print(f"Error in text_to_audio: {e}")
    #     raise HTTPException(status_code=500, detail="Internal Server Error")


# for version 2
# @router.post("/text_to_audio/{book_id}")
# def text_to_audio(book_id: int, file_name: str):
#     try:
#         # Enqueue the Celery task
#         celery_save_audio_to_s3.delay(book_id=book_id, file_name=file_name)
#         return "Task enqueued successfully"
#     except Exception as e:
#         # Handle exceptions if needed
#         print(f"Error in text_to_audio: {e}")
#         raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/", response_model=List[audio.Audio])
def get_user_audio(
    current_user: user_dependency,
    db: Session = Depends(deps.get_db),
):
    if current_user is None:
        raise HTTPException(status_code=401, detail="Authentication required")

    audio = crud_audio.Audio.get_user_audio(db=db, user_id=current_user["id"])
    return audio


"""For Development"""
# # works
# @router.get("/", response_model=List[audio.Audio])
# def read_user_Audio(
#     skip: int = 0, limit: int = 100, db: Session = Depends(deps.get_db)
# ):
#     audio = crud_audio.Audio.get_multi_Audios(db, skip=skip, limit=limit)
#     return audio


@router.delete("/{audio_id}")
def delete_audio(
    current_user: user_dependency, audio_id: int, db: Session = Depends(deps.get_db)
):
    if current_user is None:
        raise HTTPException(status_code=401, detail="Authentication required")
    return crud_audio.Audio.delete_audio(
        audio_id=audio_id, db=db, user_id=current_user["id"]
    )
