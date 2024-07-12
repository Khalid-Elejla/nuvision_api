from sqlalchemy.orm import Session
from database.models.project import Project
from schemas.project import ProjectCreate, Project as ProjectSchema
from datetime import datetime

def get_projects(db: Session, user_id: int):
    return db.query(Project).filter(Project.user_id == user_id).all()

def get_project(db: Session, project_id: int):
    return db.query(Project).filter(Project.id == project_id).first()

def create_project(db: Session, project: ProjectCreate, user_id: int):
    db_project = Project(
        name=project.name,
        description=project.description,
        user_id=user_id,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project

def update_project(db: Session, project_id: int, project: ProjectCreate):
    db_project = db.query(Project).filter(Project.id == project_id).first()
    if db_project:
        db_project.name = project.name
        db_project.description = project.description
        db_project.updated_at = datetime.now()
        db.commit()
        db.refresh(db_project)
    return db_project

def delete_project(db: Session, project_id: int):
    db_project = db.query(Project).filter(Project.id == project_id).first()
    if db_project:
        db.delete(db_project)
        db.commit()
    return db_project
