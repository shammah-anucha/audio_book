from fastapi import APIRouter, HTTPException, Depends, status
from typing import Any, List, Annotated
from sqlalchemy.orm import Session
from .....app.schemas.users import User, UserCreate
from .....app.models import models
from .....app.api import deps
from ....crud import crud_users


router = APIRouter()


user_dependency = Annotated[dict, Depends(crud_users.user.get_current_user)]


# works
@router.get("/user/", status_code=status.HTTP_200_OK, tags=["users"])
def user_login(user: user_dependency, db: Session = Depends(deps.get_db)):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")
    return {"User": user}


# works
@router.get("/users/", response_model=List[User], tags=["users"])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(deps.get_db)):
    users = crud_users.user.get_multi_user(db, skip=skip, limit=limit)
    return users


@router.delete("/users/{user_id}", tags=["users"])
def delete_user(user_id: int, db: Session = Depends(deps.get_db)):
    db_user = crud_users.user.get_user_id(db, id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    else:
        db.query(models.Users).filter(models.Users.user_id == user_id).delete()
        db.commit()
        return "Delete Successful"
