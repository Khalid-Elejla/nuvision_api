# data_sources.py or your FastAPI router file for data sources
from core.security import get_current_user
from crud import crud_data_source, crud_location
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database.database import get_db  # Adjust import paths as necessary
from schemas.data_source import DataSourceCreate, DataSourceUpdate, DataSource
from schemas.user import User

router = APIRouter()

# Create data source endpoint
@router.post("/locations/{location_id}/data_sources/", response_model=DataSource)
async def create_data_source(
    location_id: int,
    data_source: DataSourceCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Ensure the current user owns the location

    location = crud_location.get_location(db, location_id=location_id)
    if not location or location.project.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to create data sources for this location")
    data_source.location_id = location_id  # Set the location_id in the data source object

    return crud_data_source.create_data_source(db=db, data_source=data_source)

# Get all data sources for a location
@router.get("/locations/{location_id}/data_sources", response_model=List[DataSource])
async def get_data_sources_by_location(
    location_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Ensure the current user owns the location
    location = crud_location.get_location(db, location_id=location_id)
    if not location or location.project.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to view data sources for this location")
    
    return crud_data_source.get_data_sources(db, location_id)
##########################

# Get data source by ID endpoint
@router.get("/data_sources/{data_source_id}", response_model=DataSource)
async def read_data_source(
    data_source_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    data_source = crud_data_source.get_data_source(db, data_source_id)
    if data_source is None:
        raise HTTPException(status_code=404, detail="Data source not found")
    return data_source

# Update data source endpoint
@router.patch("/data_sources/{data_source_id}", response_model=DataSource)
async def update_data_source(
    data_source_id: int,
    data_source_update: DataSourceUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    updated_data_source = crud_data_source.update_data_source(db, data_source_id, data_source_update)
    
    if updated_data_source is None:
        raise HTTPException(status_code=404, detail="Data source not found")
    return updated_data_source

# Delete data source endpoint
@router.delete("/data_sources/{data_source_id}", response_model=DataSource)
async def delete_data_source(
    data_source_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    deleted_data_source = crud_data_source.delete_data_source(db, data_source_id)
    if deleted_data_source is None:
        raise HTTPException(status_code=404, detail="Data source not found")
    return deleted_data_source
