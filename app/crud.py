# crud.py
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from . import models, schemas
from jose import jwt

# Assuming you have a secret key for JWT encoding/decoding
SECRET_KEY = "fbf83421a201f69bd32adcabbfec20a0303f52d14e6bab35"
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = pwd_context.hash(user.password)
    db_user = models.User(
        email=user.email, 
        username=user.username, 
        hashed_password=fake_hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, username: str, password: str):
    user = get_user_by_username(db, username=username)
    if not user:
        return False
    if not pwd_context.verify(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict):
    # Simple token creation, expiration time can be set as needed
    from datetime import datetime, timedelta
    expire = datetime.utcnow() + timedelta(hours=1)
    data.update({"exp": expire})
    encoded_jwt = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
