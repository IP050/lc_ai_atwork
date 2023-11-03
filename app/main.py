from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from . import models, schemas, crud
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/register", response_model=schemas.UserInDB)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Check if user with same username or email already exists
    db_user = crud.get_user_by_email(db, email=user.email) or crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Email or username already registered")
    
    # Create new user
    return crud.create_user(db=db, user=user)

@app.post("/login")
async def login(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Authenticate user
    db_user = crud.authenticate_user(db, username=user.username, password=user.password)
    if db_user is None:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    # Create token (this requires additional implementation)
    token = crud.create_access_token(data={"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}

@app.get("/")
async def home():
    return "hello world"