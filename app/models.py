from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel
from .database import Base 
import datetime


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserInDB(UserCreate):
    id: int
    created_at: datetime.datetime

    class Config:
        orm_mode = True
