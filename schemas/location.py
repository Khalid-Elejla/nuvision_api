from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional

class LocationBase(BaseModel):
    name: str
    description: Optional[str]=None
    latitude: Optional[float]=None
    longitude: Optional[float]=None

class LocationCreate(LocationBase):
    pass

class Location(LocationBase):
    id: int
    project_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True