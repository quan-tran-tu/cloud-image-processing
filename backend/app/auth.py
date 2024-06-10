from fastapi import APIRouter, HTTPException
from datetime import timedelta
from .schemas import UserCreate, User
from .crud import get_user_by_email, create_user
from .database import SessionLocal
from .utils import verify_password, create_access_token
from .config import ACCESS_TOKEN_EXPIRE_MINUTES

auth_router = APIRouter()

@auth_router.post("/register", response_model=User)
def register_user(user: UserCreate):
    db = SessionLocal()
    db_user = get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return create_user(db=db, user=user)

@auth_router.post("/login")
def login_for_access_token(form_data: UserCreate):
    db = SessionLocal()
    user = get_user_by_email(db, form_data.email)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.email}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}
