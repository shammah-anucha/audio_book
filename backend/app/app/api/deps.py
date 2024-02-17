from typing import Generator, Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from ...app.core import security
from ..core.config3 import settings
from ...app.db.session import SessionLocal


def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/login/access-token"
)


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    try:

        payload = jwt.decode(token, settings.SECRET_KEY, security.ALGORITHM)
        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        if username is None or user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate user.",
            )
        return {"username": username, "id": user_id}
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate user.",
        )


"""Maybe for version 2"""

# async def get_current_active_user(
#     current_user: models.Users = Depends(get_current_user),
# ) -> models.Users:
#     if crud_users.user.disabled(current_user):
#         raise HTTPException(status_code=400, detail="Inactive user")
#     return current_user


# async def get_current_active_admin(
#     current_user: models.Users = Depends(get_current_user),
# ) -> models.Users:
#     if not crud_users.user.is_admin(current_user):
#         raise HTTPException(
#             status_code=400, detail="The user doesn't have enough privileges"
#         )
#     return current_user
