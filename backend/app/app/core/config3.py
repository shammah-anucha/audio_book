import secrets
from typing import List, Optional, Union
from pydantic import AnyHttpUrl, BaseSettings, validator
from dotenv import load_dotenv
import os


load_dotenv(".env")

SQLALCHEMY_DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URL")


class Settings(BaseSettings):
    # development
    # API_V1_STR: str = "/api/v1"
    # production
    API_V1_STR: str = "/ HTTP/1.1"
    SECRET_KEY = secrets.token_urlsafe(32)
    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 8
    SQLALCHEMY_DATABASE_URL: Optional[str] = SQLALCHEMY_DATABASE_URL

    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    PROJECT_NAME: str = "Audio Book"


settings = Settings()


# # Establish a connection to the database
# connection = mysql.connector.connect(**db_config)

# # Create a cursor object to execute SQL queries
# cursor = connection.cursor()
