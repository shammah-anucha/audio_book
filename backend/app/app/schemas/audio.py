from datetime import time, date

from pydantic import BaseModel


class AudioBase(BaseModel):
    audio_name: str
    audio_file: str


class AudioCreate(AudioBase):
    name: str


class AudioUpdate(AudioBase):
    pass


class AudioInDBBase(AudioBase):
    audio_id: int
    # user_id: int

    class Config:
        orm_mode = True


# Properties to return to client
class Audio(AudioInDBBase):
    pass


# Properties properties stored in DB
class AudioInDB(AudioInDBBase):
    pass
