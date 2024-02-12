from pydantic import BaseModel


class S3UrlBase(BaseModel):
    url: str
    # S3Url_file: Optional[UploadFile] = None


class S3UrlCreate(S3UrlBase):
    pass


class S3UrlUpdate(S3UrlBase):
    pass


class S3UrlInDBBase(BaseModel):
    user_id: int
    url: str

    class Config:
        orm_mode = True


class S3Url(S3UrlInDBBase):
    pass


class S3UrlInDB(S3UrlInDBBase):
    pass
