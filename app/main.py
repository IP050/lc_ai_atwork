from fastapi import FastAPI, HTTPException, Depends, File, UploadFile, Response, Security
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from langcorn import create_service
from sqlalchemy.orm import Session
from . import models, schemas, crud
from .database import SessionLocal, engine
from fastapi.middleware.cors import CORSMiddleware
from jose import jwt
import shutil 
import os 
from .crud import SECRET_KEY, ALGORITHM
from .ai.docs import run_conversational_retrieval_chain, format_filename, load_and_process_document, load_azure_blob_container, load_and_process_pdf, load_dir
from .ai.custom import run_chain
from azure.storage.blob import BlobServiceClient
from fastapi.responses import RedirectResponse
import logging


import traceback
import nltk
nltk.download('punkt')
original_nltk_download = nltk.download

upload_directory = "/app/uploads"
# Ensure the upload_directory exists
os.makedirs(upload_directory, exist_ok=True)


def patched_nltk_download(*args, **kwargs):
    print("NLTK download called. Stack trace:")
    traceback.print_stack()
    # Call the original nltk.download function
    return original_nltk_download(*args, **kwargs)

# Patch the nltk.download function
nltk.download = patched_nltk_download

models.Base.metadata.create_all(bind=engine)


blob_service_client = BlobServiceClient(account_url=os.environ.get('AZURE_BLOB_URL'))
container_name = os.environ.get('AZURE_CONTAINER_NAME')
azure_con_str=os.environ.get('AZURE_CONN_STR')
app:FastAPI = create_service('app.ex2:conversation')

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

allowed_origins = [
    "https://gray-tree-0f5500b03.3.azurestaticapps.net",  # Your front-end application origin
    "http://localhost:5174",  # Local development origin if needed
    # You can add more origins as needed
]

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/register", response_model=schemas.User)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Check if user with same username or email already exists
    db_user = crud.get_user_by_email(db, email=user.email) or crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Email or username already registered")
    
    # Create new user
    return crud.create_user(db=db, user=user)

@app.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.get_user_by_username(db, username=form_data.username)
    if not user or not crud.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    access_token = crud.create_access_token(data={"sub": user.username})
    response = Response()
    response.set_cookie(key="jwt", value=f"Bearer {access_token}", httponly=True)
    return response

@app.get("/check")
async def check_logged_in(token: str = Security(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        user = crud.get_user_by_username(db, username=username)
        if user is None:
            raise HTTPException(status_code=401, detail="User not found")
        return {"username": user.username, "email": user.email}
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token or expired token")

@app.post("/logout")
async def logout(response: Response):
    response.delete_cookie(key="jwt")
    return {"detail": "Logged out"}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    # Retrieve the file's name
    file_name = file.filename

    # Create a blob client using the file name as the name for the blob
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=file_name)
    
    # Read file content
    file_content = await file.read()

    # Create the blob with the file content
    blob_client.upload_blob(file_content, blob_type="BlockBlob", overwrite=True)

    return {"filename": file_name}


@app.post("/api/uploadv2")
async def upload_file(file: UploadFile = File(...)):
    filename = format_filename(file.filename)
    file_path = os.path.join(upload_directory, filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"filename": filename}

@app.post("/api/docgpttwo")
async def docgpt(request: schemas.DocRequest):
    # Check if the file existsbl
    file_path = f"uploads/{request.filename}"
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    if "pdf" in request.filename:
        docsearch = load_and_process_pdf(file_path)
    else:
        docsearch = load_and_process_document(file_path)
    
    answer = run_conversational_retrieval_chain(docsearch, request.question, request.chat_history)
    return {"answer": answer}

@app.post("/api/docgpt3")
async def docgpt(request: schemas.DocRequest):
    file_path = f"uploads/{request.filename}"
    cwd = os.getcwd()
    print({file_path})
    print(f"cwd {cwd}")
    logging.info(f"Resolved file path: {file_path}")
    logging.info(f"Current working directory: {cwd}")
    if not os.path.exists(file_path):
        logging.error("File not found at the path")
        raise HTTPException(status_code=404, detail="File not found")
    if "pdf" in request.filename:
        docsearch = load_dir("./uploads")
    else:
        docsearch = load_dir("./uploads")
    
    answer = run_conversational_retrieval_chain(docsearch, request.question, request.chat_history)
    return {"answer": answer}


@app.post("/docgpt")
async def docgpt(request: schemas.DocRequest):
    # Use the loaer to load documents from the container bla
    docsearch = load_azure_blob_container(
                azure_con_str=os.environ.get('AZURE_CONN_STR'),
                containername = os.environ.get('AZURE_CONTAINER_NAME'),
                filename = request.filename 
)

    answer = run_conversational_retrieval_chain(docsearch, request.question, request.chat_history)
    
    return {"answer": answer}

@app.post("/api/runchain")
async def runner(request: schemas.ChatRequest):
    return run_chain({'query' : request.query, 'language' : request.language, 'persona' : request.persona})


    
@app.get("/")
async def root():
    return "root"
