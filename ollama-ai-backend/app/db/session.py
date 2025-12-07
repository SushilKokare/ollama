from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

# Load .env variables
load_dotenv()

POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
POSTGRES_DB = os.getenv("POSTGRES_DB", "postgres")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "db")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", 5432)

DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

# Create engine
engine = create_engine(DATABASE_URL, echo=True)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

# Dependency for FastAPI endpoints
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
