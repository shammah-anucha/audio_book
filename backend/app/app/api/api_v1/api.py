# from fastapi import APIRouter
# from fastapi import Depends


# from ....app.api import deps
# from ....app.api.api_v1.endpoints import users, login, books, audio


# api_router = APIRouter(dependencies=[Depends(deps.get_db)])


# api_router.include_router(login.router)
# api_router.include_router(users.router)
# api_router.include_router(books.router)
# api_router.include_router(audio.router)
