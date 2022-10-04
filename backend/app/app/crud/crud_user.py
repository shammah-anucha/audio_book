from typing import Any, Dict, Optional, Union, List

from sqlalchemy.orm import Session

from ...app.core.security import get_password_hash, verify_password
from ...app.crud.base import CRUDBase
from ...app.models import models
from ...app.schemas.users import UserCreate, UserUpdate


class CRUDUser(CRUDBase[models.Users, UserCreate, UserUpdate]):
    def get_user_by_email(self, db: Session, email: str) -> Optional[models.Users]:
        return db.query(models.Users).filter(models.Users.email == email).first()

    def create(self, db: Session, *, obj_in: UserCreate) -> models.Users:
        db_user = models.Users(
            email=obj_in.email,
            username=obj_in.username,
            Firstname=obj_in.Firstname,
            Lastname=obj_in.Lastname,
            D_O_B=obj_in.D_O_B,
            country_of_residence=obj_in.country_of_residence,
            phone=obj_in.phone,
            is_admin=obj_in.is_admin,
            hashed_password=get_password_hash(obj_in.password),
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    def update(
        self,
        db: Session,
        *,
        db_obj: models.Users,
        obj_in: Union[UserUpdate, Dict[str, Any]]
    ) -> models.Users:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        if update_data["password"]:
            hashed_password = get_password_hash(update_data["password"])
            del update_data["password"]
            update_data["hashed_password"] = hashed_password
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def get_multi_user(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[models.Users]:
        return db.query(self.model).offset(skip).limit(limit).all()

    def get_user_id(self, db: Session, id: Any):
        return db.query(models.Users).filter(models.Users.user_id == id).first()

    def authenticate_user(
        self, db: Session, *, email: str, password: str
    ) -> Optional[models.Users]:
        user = self.get_user_by_email(db, email=email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    def disabled(self, user: models.Users) -> bool:
        return user.disabled

    def is_admin(self, user: models.Users) -> bool:
        return user.is_admin


user = CRUDUser(models.Users)
