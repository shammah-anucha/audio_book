from fastapi import APIRouter, Depends
from ....crud import crud_audio
from ....schemas import audio
from ... import deps
from sqlalchemy.orm import Session
from ....crud import s3
from ....models import models




router = APIRouter(
    prefix="/audios", tags=["audios"], dependencies=[Depends(deps.get_db)]
)


@router.post("/text_to_audio/{book_id}")
def text_to_audio(book_id: int, file_name: str, db: Session = Depends(deps.get_db)):
    # Post audio streams
    s3.save_audio_to_s3(book_id=book_id, file_name=file_name, db=db)
    return 'Saved successfully'

@router.delete("/{audio_id}")
def delete_audio(audio_id: int, db: Session = Depends(deps.get_db)):
    s3.delete_audio_from_s3(db=db, audio_id=audio_id)
    db.query(models.Audio).filter(models.Audio.audio_id == audio_id).delete()
    db.commit()
    return "Delete Successful"

   