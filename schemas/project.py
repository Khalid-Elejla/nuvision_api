from pydantic import BaseModel
from typing import List, Optional
from .location import Location

class Project(BaseModel):
    id: int
    name: str
    description: Optional[str]
    locations: List[Location]

    class Config:
        orm_mode = True
