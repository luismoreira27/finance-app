from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.auth_db import SessionLocal
from pydantic import BaseModel
from backend.auth_db import Credentials
from passlib.context import CryptContext
import hashlib, base64

router = APIRouter(prefix="/auth", tags=["Auth"])

pwd_context = CryptContext(schemes = ["bcrypt"], deprecated = "auto")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class RegisterRequest(BaseModel):
    username: str
    password: str
    name: str


class LoginRequest(BaseModel):
    username: str
    password: str


@router.post("/register")
def register(data: RegisterRequest, db: Session = Depends(get_db)):
    user = db.query(Credentials).filter(Credentials.username == data.username).first()
    if user:
        raise HTTPException(status_code = 400, detail = "User already exists!")

    new_user = Credentials(username = data.username, name = data.name, password = data.password)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User registered sucessfully!"}


@router.post("/login")
async def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(Credentials).filter(Credentials.username == data.username).first()
    if not user:
        raise HTTPException(status_code = 400, detail = "Invalid username or password")

    if not pwd_context.verify(data.password, user.password):
        raise HTTPException(status_code= 400, detail = "Inavalid username or password")
    
    return {"message": "Login Sucessful!", "username": user.username}