from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from .base import CRUDBase
from ..models import models
from ..schemas.audio import AudioCreate, AudioUpdate
from . import crud_book
from gtts import gTTS
from io import BytesIO
import gtts
from gtts.tokenizer import pre_processors

class CRUDAudio(CRUDBase[models.Audio, AudioCreate, AudioUpdate]):

    
    def get_audio(self, book_id: int, page_number: int, db: Session):
        text = crud_book.Book.extract_text_from_pdf_in_db(book_id=book_id, page_number=page_number,db=db)
        tts = gTTS(text=text, lang='en', slow=False,)
        # pre_processors.tone_marks()
        audio_bytes = BytesIO()
        tts.write_to_fp(audio_bytes)
        return audio_bytes.getvalue()

        

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
