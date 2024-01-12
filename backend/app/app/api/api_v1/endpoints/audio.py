from fastapi import APIRouter, Depends
from ....crud import crud_audio
from ....schemas import audio
from ... import deps
from typing import List
from sqlalchemy.orm import Session


router = APIRouter(
    prefix="/audios", tags=["audios"], dependencies=[Depends(deps.get_db)]
)

# works
@router.post("/", response_model=audio.Audio)
def create_Audio(Audio: audio.AudioCreate, db: Session = Depends(deps.get_db)):
    return crud_audio.Audio.create_Audio(db=db, obj_in=Audio)


# works
@router.get("/", response_model=List[audio.Audio])
def read_Audios(skip: int = 0, limit: int = 100, db: Session = Depends(deps.get_db)):
    roster = crud_audio.Audio.get_multi_Audios(db, skip=skip, limit=limit)
    return roster
