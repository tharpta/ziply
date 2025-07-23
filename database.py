import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

# Use environment variable for database URL in production, fallback to local SQLite
# In production with volume mount, store database in persistent directory
if os.getenv("RAILWAY_ENVIRONMENT"):
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./data/ziply.db")
else:
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./ziply.db")

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)