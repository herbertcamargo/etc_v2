"""
Database session handling with SQLAlchemy.

This module provides the SQLAlchemy session factory and engine configuration
for both synchronous and asynchronous database access.

Requirements fulfilled:
- Asynchronous database access
- Connection pooling
- Session management
"""

import logging
from typing import AsyncGenerator

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

# Configure logging
logger = logging.getLogger(__name__)

# Create async engine
async_engine = create_async_engine(
    settings.SQLALCHEMY_DATABASE_URI,
    pool_pre_ping=True,
    echo=settings.DEBUG,
    future=True
)

# Create session factory for async sessions
async_session = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)


# Dependency for getting an async database session
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Get a database session for use in FastAPI dependency injection.
    
    Yields:
        AsyncSession: SQLAlchemy async session
    """
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except Exception as e:
            logger.error(f"Database session error: {str(e)}")
            await session.rollback()
            raise
        finally:
            await session.close() 