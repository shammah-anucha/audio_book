from fastapi import APIRouter, Depends
from ....crud import crud_audio
from ....schemas import audio
from ... import deps
from typing import List
from sqlalchemy.orm import Session
from fastapi.responses import StreamingResponse
from gtts import gTTS
from io import BytesIO
from ....crud import crud_audio



router = APIRouter(
    prefix="/audios", tags=["audios"], dependencies=[Depends(deps.get_db)]
)

# works
@router.post("/", response_model=audio.Audio)
def create_Audio(Audio: audio.AudioCreate, db: Session = Depends(deps.get_db)):
    return crud_audio.Audio.create_Audio(db=db, obj_in=Audio)


# works
@router.get("/", response_model=List[audio.Audio])
# def read_Audios(book_id: int, page_number: int, db: Session = Depends(deps.get_db)): 
#     pass 

def text_to_audio(book_id: int, page_number: int, db: Session = Depends(deps.get_db)):

    # Convert text to audio
    audio_data = crud_audio.Audio.get_audio(book_id=book_id, page_number=page_number,db=db)

    # Provide audio as a download using StreamingResponse
    return StreamingResponse(
        BytesIO(audio_data), media_type="audio/mpeg", headers={"Content-Disposition": f'attachment; filename="audio.mp3"'}
    )