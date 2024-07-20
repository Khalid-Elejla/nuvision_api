# locations.py or your FastAPI router file for locations
from core.security import get_current_user
from crud import crud_location, crud_project
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database.database import get_db  # Adjust import paths as necessary
from schemas.location import LocationCreate, LocationUpdate, Location
from schemas.user import User

router = APIRouter()


# Create location endpoint
@router.post("/projects/{project_id}/locations/", response_model=Location)
async def create_location(
    project_id: int,
    location: LocationCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Ensure the current user owns the project
    project = crud_project.get_project(db, project_id=project_id)
    if not project or project.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to create locations for this project")

    location.project_id = project_id  # Set the project_id in the location object
    return crud_location.create_location(db=db, location=location, user_id=current_user.id)


# Get all locations for a project
@router.get("/projects/{project_id}/locations", response_model=List[Location])
async def get_locations_by_project(
    project_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return crud_location.get_locations(db, project_id)

# Get location by ID endpoint
@router.get("/locations/{location_id}", response_model=Location)
async def read_location(
    location_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    location = crud_location.get_location(db, location_id)
    if location is None:
        raise HTTPException(status_code=404, detail="Location not found")
    return location

# Update location endpoint
@router.patch("/locations/{location_id}", response_model=Location)
async def update_location(
    location_id: int,
    location_update: LocationUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    updated_location = crud_location.update_location(db, location_id, location_update)
    
    if updated_location is None:
        raise HTTPException(status_code=404, detail="Location not found")
    return updated_location

##
# Delete location endpoint
@router.delete("/locations/{location_id}", response_model=Location)
async def delete_location(
    location_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    deleted_location = crud_location.delete_location(db, location_id)
    if deleted_location is None:
        raise HTTPException(status_code=404, detail="Location not found")
    return deleted_location