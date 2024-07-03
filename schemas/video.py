from pydantic import BaseModel

class Video(BaseModel):
    id: int
    name: str
    url: str
    duration: int  # in seconds

    class Config:
        orm_mode = True
