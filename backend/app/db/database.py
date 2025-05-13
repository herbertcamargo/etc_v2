"""
Database connection module.

This module sets up the SQLAlchemy engine, session, and base model for the application.
It provides the core database functionality used throughout the application.
"""

from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

# Create SQLAlchemy engine
engine = create_engine(str(settings.DATABASE_URL))

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base class for models
Base = declarative_base()


def get_db() -> Generator:
    """
    Get a database session.
    
    Yields:
        SQLAlchemy session that will be automatically closed after use
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 