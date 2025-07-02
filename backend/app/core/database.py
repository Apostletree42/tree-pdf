from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator
from .config import settings

# Create SQLAlchemy engine
if settings.database_url.startswith("sqlite"):
    # SQLite specific settings
    engine = create_engine(
        settings.database_url,
        connect_args={"check_same_thread": False},
        echo=settings.debug
    )
else:
    # PostgreSQL/other databases
    engine = create_engine(
        settings.database_url,
        echo=settings.debug
    )

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class for models
Base = declarative_base()

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        db.close()

# Initialize database tables
def init_db():
    """Create all database tables"""
    Base.metadata.create_all(bind=engine)