from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database.database import get_db
from schemas.token import Token
from schemas.user import UserCreate, User
from crud import crud_user
from core.security import authenticate_user, create_access_token, get_current_user
from datetime import timedelta

router = APIRouter()

@router.post("/register", response_model=User)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = crud_user.get_user_by_username(db, username=user.username)
    db_email = crud_user.get_user_by_email(db, email=user.email)

    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    elif db_email:
        raise HTTPException(status_code=400, detail="User email already registered")
    return crud_user.create_user(db=db, user=user)

@router.post("/login", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user= authenticate_user (db = db, username=form_data.username, password=form_data.password)
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/users/me", response_model=User)
def read_users_me(current_user:User = Depends(get_current_user)):
    return current_user