from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from schemas.project import ProjectCreate, Project, ProjectUpdate
from schemas.user import User
from crud import crud_project
from database.database import get_db
from core.security import get_current_user

router = APIRouter()

# Create project endpoint
@router.post("/projects/", response_model=Project)
async def create_project(
    project: ProjectCreate, 
    current_user: User = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    return crud_project.create_project(db=db, project=project, user_id=current_user.id)

# Get all projects endpoint
@router.get("/projects/", response_model=List[Project])
async def read_projects(
    current_user: User = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    return crud_project.get_projects(db=db, user_id=current_user.id)

# Get project by ID endpoint
@router.get("/projects/{project_id}", response_model=Project)
async def read_project(
    project_id: int, 
    current_user: User = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    project = crud_project.get_project(db=db, project_id=project_id)
    if project is None or project.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

# Update project endpoint
@router.put("/projects/{project_id}", response_model=Project)
async def update_project(
    project_id: int, 
    project: ProjectCreate, 
    current_user: User = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    updated_project = crud_project.update_project(db=db, project_id=project_id, project_update=project)
    if updated_project is None or updated_project.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Project not found")
    return updated_project

# Patch project endpoint
@router.patch("/projects/{project_id}", response_model=Project)
def patch_project(
    project_id: int,
    project_update: ProjectUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    updated_project = crud_project.patch_project(db, project_id, project_update)
    if updated_project is None or updated_project.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Project not found")    
    return updated_project

# Delete project endpoint
@router.delete("/projects/{project_id}", response_model=Project)
async def delete_project(
    project_id: int, 
    current_user: User = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
#    existing_project = crud_project.get_project(db=db, project_id=project_id)
    deleted_project= crud_project.delete_project(db=db, project_id=project_id)
    if deleted_project is None or deleted_project.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Project not found")
    return {"message": "Project deleted successfully"}
