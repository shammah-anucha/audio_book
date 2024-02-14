from fastapi import FastAPI
import uvicorn
from starlette.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from ..app.api.api_v1.api import api_router
from .core.config3 import settings

# main.py


app = FastAPI(
    title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json"
)
# app = FastAPI(
#     title=settings.PROJECT_NAME, openapi_url="https://audio-book-api-m825.onrender.com"
# )

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router, prefix=settings.API_V1_STR)


# @app.get("/")
# def read_root():
#     return "Hello World"


# if __name__ == "__main__":

#     uvicorn.run(app, host="0.0.0.0", port=8000)
