from fastapi import APIRouter, Depends
from ... import deps
from sqlalchemy.orm import Session
from typing import List
from ....crud import crud_audio
from fastapi.responses import FileResponse


router = APIRouter(
    prefix="/download_audio",
    tags=["download audio"],
    dependencies=[Depends(deps.get_db)],
)


@router.get(
    "/",
)
async def download_and_zip_audio_files(
    audio_id: int, db: Session = Depends(deps.get_db)
):

    zip_file_path = crud_audio.Audio.download_and_zip_audio_files(
        db=db, audio_id=audio_id
    )

    return FileResponse(
        zip_file_path, filename="audio_files.zip", media_type="application/zip"
    )
