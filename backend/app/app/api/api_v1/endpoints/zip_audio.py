from fastapi import APIRouter, Depends, HTTPException
from ... import deps
from sqlalchemy.orm import Session
from typing import Annotated
from ....crud import crud_audio
from fastapi.responses import FileResponse
from ....api.deps import get_current_user


router = APIRouter(
    prefix="/download_audio",
    tags=["download audio"],
    dependencies=[Depends(deps.get_db)],
)

user_dependency = Annotated[dict, Depends(get_current_user)]


@router.get(
    "/",
)
async def download_and_zip_audio_files(
    current_user: user_dependency, audio_id: int, db: Session = Depends(deps.get_db)
):
    if current_user is None:
        raise HTTPException(status_code=401, detail="Authentication required")

    zip_file_path = crud_audio.Audio.download_and_zip_audio_files(
        db=db, audio_id=audio_id, user_id=current_user["id"]
    )

    return FileResponse(
        zip_file_path, filename="audio_files.zip", media_type="application/zip"
    )
