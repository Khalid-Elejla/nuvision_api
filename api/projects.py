from fastapi import APIRouter, Depends, HTTPException
from typing import List
from models.project import Project
from models.user import User

from .auth import get_current_user

router = APIRouter()

# Mock database for demonstration
projects_db = []

# Create project endpoint
@router.post("/projects/", response_model=Project)
async def create_project(project: Project, current_user: User = Depends(get_current_user)):
    # Create project logic (e.g., save to database)
    projects_db.append(project)
    return project

# Get all projects endpoint
@router.get("/projects/", response_model=List[Project])
async def read_projects(current_user: User = Depends(get_current_user)):
    return projects_db

# Get project by ID endpoint
@router.get("/projects/{project_id}", response_model=Project)
async def read_project(project_id: int, current_user: User = Depends(get_current_user)):
    project = next((p for p in projects_db if p.id == project_id), None)
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

# Update project endpoint
@router.put("/projects/{project_id}", response_model=Project)
async def update_project(project_id: int, project: Project, current_user: User = Depends(get_current_user)):
    # Update project logic (e.g., update in database)
    index = next((i for i, p in enumerate(projects_db) if p.id == project_id), None)
    if index is None:
        raise HTTPException(status_code=404, detail="Project not found")
    projects_db[index] = project
    return project

# Delete project endpoint
@router.delete("/projects/{project_id}")
async def delete_project(project_id: int, current_user: User = Depends(get_current_user)):
    # Delete project logic (e.g., delete from database)
    global projects_db
    projects_db = [p for p in projects_db if p.id != project_id]
    return {"message": "Project deleted successfully"}
