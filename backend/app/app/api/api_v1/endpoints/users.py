from fastapi import APIRouter, HTTPException, Depends
from typing import Any, List
from sqlalchemy.orm import Session
from .....app.schemas.users import User, UserCreate
from .....app.models import models
from .....app.api import deps
from ....crud import crud_users


router = APIRouter()

# works
@router.post("/users/", response_model=User, tags=["users"])
def create_user(*, users_in: UserCreate, db: Session = Depends(deps.get_db)) -> Any:
    """Create new user."""
    user = crud_users.user.get_user_by_email(db, email=users_in.email)
    if user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud_users.user.create(db=db, obj_in=users_in)


# works
@router.get("/users/", response_model=List[User], tags=["users"])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(deps.get_db)):
    users = crud_users.user.get_multi_user(db, skip=skip, limit=limit)
    return users


# works
@router.get("/users/{user_id}", response_model=User, tags=["users"])
def read_user(user_id: int, db: Session = Depends(deps.get_db)):
    db_user = crud_users.user.get_user_id(db, id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.delete("/users/{user_id}", tags=["users"])
def delete_user(user_id: int, db: Session = Depends(deps.get_db)):
    db_user = crud_users.user.get_user_id(db, id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    else:
        db.query(models.Users).filter(models.Users.user_id == user_id).delete()
        db.commit()
        return "Delete Successful"
