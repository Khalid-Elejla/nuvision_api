from database.models.project import Project
from fastapi import HTTPException, HTTPException, Request
from crud import crud_project
from schemas.user import User
from sqlalchemy.orm import Session
from datetime import datetime
from database.models.location import Location
from schemas.location import LocationCreate, LocationUpdate


def get_current_project_by_location_id(db: Session, location:Location, current_user: User):

    project = db.query(Project).filter(Project.id == location.project_id, Project.user_id == current_user.id).first()
    return project

def get_locations(db: Session, project_id: int):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    return db.query(Location).filter(Location.project_id == project_id).all()

def get_location(db: Session, location_id: int):
    return db.query(Location).filter(Location.id == location_id).first()

def create_location(db: Session, location: LocationCreate, user_id: int):
    # Ensure the current user owns the project
    project = crud_project.get_project(db, project_id=location.project_id)
    if not project or project.user_id != user_id:
        return None
    db_location = Location(
        name=location.name,
        description=location.description,
        latitude=location.latitude,
        longitude=location.longitude,
        project_id=location.project_id,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    db.add(db_location)
    db.commit()
    db.refresh(db_location)
    return db_location

def update_location(db: Session, location_id: int, location_update: LocationUpdate):
    db_location = db.query(Location).filter(Location.id == location_id).first()
    if not db_location:
        return None

    update_data = location_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_location, key, value)

    db_location.updated_at = datetime.now()
    db.commit()
    db.refresh(db_location)
    return db_location

def delete_location(db: Session, location_id: int):
    db_location = db.query(Location).filter(Location.id == location_id).first()
    if db_location:
        db.delete(db_location)
        db.commit()
    return db_location
