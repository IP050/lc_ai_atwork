from pydantic import BaseModel
from typing import Optional
import datetime
from typing import List, Dict

# This schema will be used for user creation requests
class UserCreate(BaseModel):
    username: str
    email: str
    password: str

# This schema inherits from UserCreate and also includes
# the id and created_at fields. It will be used for responses.
class UserInDB(BaseModel):
    id: int
    created_at: datetime.datetime

    class Config:
        orm_mode = True

# This schema is similar to UserInDB but does not include sensitive information like password
# It can be used for reading user data without revealing the hashed_password
class User(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime.datetime

    class Config:
        orm_mode = True

# For authentication purposes, we can also define a schema for the token
class Token(BaseModel):
    access_token: str
    token_type: str

# Optionally, a schema for token data could also be defined
class TokenData(BaseModel):
    username: Optional[str] = None


# AI doc scheme

class DocRequest(BaseModel):
    filename: str 
    chat_history: List[str]
    question: str 
    
class DocRequestTwo(BaseModel):
    filename: List[str]
    chat_history: List[str]
    question: str 

class DocRequest(BaseModel):
    filename: str 
    chat_history: List[str]
    question: str 

# chatreq 
class ChatRequest(BaseModel):
    query: str 
    language: str
    persona: str
