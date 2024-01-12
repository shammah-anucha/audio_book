from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from .base import CRUDBase
from ..models import models
from ..schemas.audio import AudioCreate, AudioUpdate


class CRUDAudio(CRUDBase[models.Audio, AudioCreate, AudioUpdate]):
    def create_Audio(self, db: Session, *, obj_in: AudioCreate) -> models.Audio:
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
