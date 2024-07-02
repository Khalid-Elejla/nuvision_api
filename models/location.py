from pydantic import BaseModel
from typing import List, Optional
from .video import Video

class Location(BaseModel):
    id: int
    name: str
    description: str
    videos: List[Video]
    latitude: Optional[float]
    longitude: Optional[float]

    class Config:
        orm_mode = True
