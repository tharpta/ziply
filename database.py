import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

# Use environment variable for database URL in production, fallback to local SQLite
# In production with volume mount, store database in persistent directory
if os.getenv("RAILWAY_ENVIRONMENT"):
    # Try to use persistent data directory, fallback to temp if needed
    try:
        data_dir = "./data"
        os.makedirs(data_dir, exist_ok=True)
        DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./data/ziply.db")
    except (OSError, PermissionError):
        # Fallback to /tmp if data directory can't be created
        DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:////tmp/ziply.db")
else:
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./ziply.db")

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)