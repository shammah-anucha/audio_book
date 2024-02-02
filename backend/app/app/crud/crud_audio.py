from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from .base import CRUDBase
from ..models import models
from ..schemas.audio import AudioCreate, AudioUpdate
from . import crud_book
from gtts import gTTS, gTTSError
from io import BytesIO
import time

class CRUDAudio(CRUDBase[models.Audio, AudioCreate, AudioUpdate]):

    def create_audio_stream(self, text_list: List[str]):
        audio_streams = []

        for i, text in enumerate(text_list, start=1):
            try:
                tts = gTTS(text=text, lang='en', slow=False)
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
        print(audio_streams)
        return audio_streams
    

    # def save_audio_stream(self, book_id: int, db: Session):
    #     text_list = crud_book.Book.extract_text_from_pdf_in_db(book_id=book_id, db=db)
    #     audio_streams = Audio.create_audio_stream(text_list)
    #     user_id = db.query(models.Books.user_id).filter(models.Books.book_id == book_id).first()[0]
    #     audio_url = upload_to_s3()
    #     try:
    #         for audio_stream in audio_streams:
    #             db_file = models.Audio(user_id=user_id, book_id=book_id, audio_file=audio_stream.read())
    #             print(db_file)
    #             db.add(db_file)
    #             db.commit()
    #             db.refresh(db_file)
        
    #     finally:
    #         db.close()
        

    def save_to_database(self, db: Session, *, obj_in: AudioCreate) -> models.Audio:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi_Audios(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[models.Audio]:
        return db.query(self.model).offset(skip).limit(limit).all()
    


Audio = CRUDAudio(models.Audio)
