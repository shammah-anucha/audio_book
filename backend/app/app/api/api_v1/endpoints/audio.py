from fastapi import APIRouter, Depends
from ....crud import crud_audio
from ....schemas import audio
from ... import deps
from sqlalchemy.orm import Session
from ....crud import crud_audio



router = APIRouter(
    prefix="/audios", tags=["audios"], dependencies=[Depends(deps.get_db)]
)


@router.post("/text_to_audio/{book_id}")
def text_to_audio(book_id: int, db: Session = Depends(deps.get_db)):
    # Get audio streams
    crud_audio.Audio.save_audio_stream(book_id=book_id, db=db)
    return 'Saved successfully'
  

   