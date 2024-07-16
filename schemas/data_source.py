# schemas/data_source.py
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class DataSourceBase(BaseModel):
    name: str
    description: Optional[str] = None
    source_type: str
    source_url: str
    

class DataSourceCreate(DataSourceBase):
    pass

# class DataSourceUpdate(BaseModel):
#     name: Optional[str] = None
#     description: Optional[str] = None
#     source_type: Optional[str] = None
#     source_url: Optional[str] = None

class DataSource(DataSourceBase):
    id: int
    location_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

