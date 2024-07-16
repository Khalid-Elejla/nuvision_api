from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database.database import get_db
from schemas.token import Token
from schemas.user import UserCreate, User
from crud import crud_user
from core.security import authenticate_user, create_access_token, get_user
from datetime import timedelta
from core.config import Settings

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


@router.post("/token", response_model=Token)
def login_for_access_token(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    #user = authenticate_user(db, form_data.username, form_data.password)
    user = get_user(form_data.username)

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=Settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

#################################################################################
# import os
# from fastapi import APIRouter, Depends, HTTPException, status
# from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
# from datetime import datetime, timedelta
# from jose import JWTError, jwt
# from passlib.context import CryptContext
# from typing import Optional
# from database.models.user import User
# from dotenv import load_dotenv


# # Load environment variables
# load_dotenv()

# SECRET_KEY = os.getenv("SECRET_KEY")
# ALGORITHM = os.getenv("ALGORITHM")
# ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

# router = APIRouter()

# # Mock database for demonstration
# fake_users_db = {
#     "user@example.com": {
#         "username": "user@example.com",
#         "email": "user@example.com",
#         "hashed_password": "$2b$12$rAPM7zUJBkgrdrPHQZGnsOEbSccuia9oMcWwS7PVk/0ks5tQS3I/2",  # hashed version of "password"
#     }
# }

# # Password hashing
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# # OAuth2PasswordBearer for token handling
# #oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/login")

# # Function to verify password
# def verify_password(plain_password, hashed_password):
#     return pwd_context.verify(plain_password, hashed_password)

# # Function to get user from database
# def get_user(email: str):
#     if email in fake_users_db:
#         user_dict = fake_users_db[email]
#         return User(**user_dict)

# # Function to create access token
# def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
#     to_encode = data.copy()
#     if expires_delta:
#         expire = datetime.now() + expires_delta
#     else:
#         expire = datetime.now() + timedelta(minutes=15)
#     to_encode.update({"exp": expire})
#     encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
#     return encoded_jwt

# # Login endpoint
# @router.post("/login")
# async def login(form_data: OAuth2PasswordRequestForm = Depends()):
#     user = get_user(form_data.username)
#     if not user or not verify_password(form_data.password, user.hashed_password):
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect username or password",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     access_token = create_access_token(
#         data={"sub": user.email}, expires_delta=access_token_expires
#     )
#     return {"access_token": access_token, "token_type": "bearer"}

# # Mock function to get current user
# def get_current_user(token: str = Depends(oauth2_scheme)):
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         username: str = payload.get("sub")
#         if username is None:
#             raise credentials_exception
#     except JWTError:
#         raise credentials_exception
#     user = get_user(username)
#     if user is None:
#         raise credentials_exception
#     return user