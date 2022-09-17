from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.events import Event
from app.schemas.events import EventCreate


class CRUDEvent(CRUDBase[Event, EventCreate]):
    def create_event(self, db: Session, *, obj_in: EventCreate) -> Event:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi_events(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[Event]:
        return db.query(self.model).offset(skip).limit(limit).all()


event = CRUDEvent(Event)
