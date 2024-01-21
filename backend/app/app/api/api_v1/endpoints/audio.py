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


@router.get("/text_to_audio/{book_id}")
def text_to_audio(book_id: int, db: Session = Depends(deps.get_db)):
    # Get audio streams
    audio_streams = crud_audio.Audio.get_audio_stream(book_id=book_id, db=db)

    print(audio_streams)

    # Define a generator function to yield audio chunks
    def audio_generator():
        for audio_stream in audio_streams:
            yield audio_stream.read()

    # Return a StreamingResponse with the generator function
    return StreamingResponse(audio_generator(), media_type="audio/mpeg", )

   