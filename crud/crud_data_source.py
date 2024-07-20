from datetime import datetime
from sqlalchemy.orm import Session
from database.models.data_source import DataSource
from schemas.data_source import DataSourceCreate, DataSourceUpdate
from fastapi import HTTPException

def get_data_sources(db: Session, location_id: int):
    return db.query(DataSource).filter(DataSource.location_id == location_id).all()

def get_data_source(db: Session, data_source_id: int):
    return db.query(DataSource).filter(DataSource.id == data_source_id).first()

def create_data_source(db: Session, data_source: DataSourceCreate):
    db_data_source = DataSource(
        name=data_source.name,
        description=data_source.description,
        source_type=data_source.source_type,
        source_url=data_source.source_url,
        location_id=data_source.location_id,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    db.add(db_data_source)
    db.commit()
    db.refresh(db_data_source)
    return db_data_source

def update_data_source(db: Session, data_source_id: int, data_source_update: DataSourceUpdate):
    db_data_source = db.query(DataSource).filter(DataSource.id == data_source_id).first()
    if not db_data_source:
        return None

    update_data = data_source_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_data_source, key, value)

    db_data_source.updated_at = datetime.now()
    db.commit()
    db.refresh(db_data_source)
    return db_data_source

def delete_data_source(db: Session, data_source_id: int):
    db_data_source = db.query(DataSource).filter(DataSource.id == data_source_id).first()
    if db_data_source:
        db.delete(db_data_source)
        db.commit()
    return db_data_source
