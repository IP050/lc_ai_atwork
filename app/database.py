from databases import Database
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
import os 
from urllib.parse import unquote

DATABASE_URL = os.environ.get('DATABASE_URL')
engine = create_engine(DATABASE_URL)
metadata = MetaData()

# Set up databases for async support
database = Database(DATABASE_URL)

# Set up SQLAlchemy for sync support (if needed)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for your ORM models
Base = declarative_base()
