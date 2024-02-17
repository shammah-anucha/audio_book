from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from .base import CRUDBase
from ..models import models
from ..schemas.audio import AudioCreate, AudioUpdate
from fastapi import HTTPException
from gtts import gTTS, gTTSError
from io import BytesIO
import time
import json
import tempfile
from .s3 import s3_audio, s3_book
import os
import requests
import zipfile


class CRUDAudio(CRUDBase[models.Audio, AudioCreate, AudioUpdate]):

    def create_audio_stream(self, text_list: List[str]):
        audio_streams = []

        for i, text in enumerate(text_list, start=1):
            try:
                tts = gTTS(text=text, lang="en", slow=False)
                audio_bytes = BytesIO()
                tts.write_to_fp(audio_bytes)
                audio_bytes.seek(0)
                audio_streams.append(audio_bytes)
            except gTTSError as e:
                if "429" in str(e):
                    # Retry after a delay
                    print(f"Rate limited. Retrying after 10 seconds.")
                    time.sleep(10)  # Introduce an artificial wait
                else:
                    # Handle other errors
                    print(f"Error: {e}")
                    break
        return audio_streams

    def get_audio_id(self, db: Session, id: int):
        return db.query(models.Audio).filter(models.Audio.audio_id == id).first()

    def save_to_database(self, db: Session, *, obj_in: AudioCreate) -> models.Audio:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_user_audio(self, db: Session, user_id: int) -> List[models.Audio]:
        db_user_audio = (
            db.query(models.Audio).filter(models.Audio.user_id == user_id).all()
        )
        return db_user_audio

    """For Development"""
    # def get_multi_Audios(
    #     self, db: Session, *, skip: int = 0, limit: int = 100
    # ) -> List[models.Audio]:
    #     return db.query(self.model).offset(skip).limit(limit).all()

    def delete_audio(self, db: Session, audio_id: int, user_id: int):
        db_audio = Audio.get_audio_id(db=db, id=audio_id)
        db_user_id = (
            db.query(models.Audio.user_id)
            .filter(models.Audio.audio_id == audio_id)
            .first()[0]
        )
        if not db_audio:
            raise HTTPException(status_code=404, detail="Audio not found")
        if user_id != db_user_id:
            raise HTTPException(status_code=404, detail="Audio does not belong to you")
        else:
            s3_audio.delete_audio_from_s3(db=db, audio_id=audio_id)
            db.query(models.Audio).filter(models.Audio.audio_id == audio_id).delete()
            db.commit()
            return "Delete Successful"

    def download_and_zip_audio_files(self, db: Session, audio_id: int, user_id: int):
        db_audio = Audio.get_audio_id(db=db, id=audio_id)
        if not db_audio:
            raise HTTPException(status_code=404, detail="Audio not found")
        db_user_id = (
            db.query(models.Audio.user_id)
            .filter(models.Audio.audio_id == audio_id)
            .first()[0]
        )
        if user_id != db_user_id:
            raise HTTPException(status_code=404, detail="Audio does not belong to you")
        try:
            audio_url = (
                db.query(models.Audio.audio_file)
                .filter(models.Audio.audio_id == audio_id)
                .first()[0]
            )
            audio_url = json.loads(audio_url)

            # Create a temporary directory to store downloaded audio files
            temp_dir = tempfile.mkdtemp()

            # Specify the zip file path
            zip_file_path = os.path.join(temp_dir, "audio_files.zip")

            with zipfile.ZipFile(zip_file_path, "w") as zip_file:
                for url in audio_url:
                    filename = url.split("/")[-1]
                    audio_content = s3_book.download_object_from_s3(url)
                    zip_file.writestr(filename, audio_content.getvalue())

            return zip_file_path

        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Error creating zip file: {str(e)}"
            )


Audio = CRUDAudio(models.Audio)
