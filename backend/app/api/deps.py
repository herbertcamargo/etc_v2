"""
API dependencies for FastAPI application.

This module provides various dependency injection functions for use
in FastAPI route handlers, including authentication, database access,
and service instantiation.

Requirements fulfilled:
- Dependency injection for authentication
- Database access dependencies 
- Service instantiation
"""

import logging
from typing import AsyncGenerator, Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.security import verify_password
from app.db.session import get_db
from app.models.user import User
from app.services.youtube import YouTubeService, get_youtube_service

# Configure logging
logger = logging.getLogger(__name__)

# Create OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/auth/token"
)


# Database dependency
async def get_current_user(
    db: AsyncSession = Depends(get_db),
    token: str = Depends(oauth2_scheme)
) -> User:
    """
    Get the current authenticated user from JWT token.
    
    Args:
        db: Database session
        token: JWT token
        
    Returns:
        User: Authenticated user
        
    Raises:
        HTTPException: If authentication fails
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # Decode token
        payload = jwt.decode(
            token, 
            settings.SECRET_KEY, 
            algorithms=[settings.ALGORITHM]
        )
        user_id: str = payload.get("sub")
        
        if user_id is None:
            raise credentials_exception
            
    except (JWTError, ValidationError):
        logger.error("JWT token validation failed")
        raise credentials_exception
    
    # Get user from database
    from sqlalchemy import select
    
    stmt = select(User).where(User.id == user_id)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()
    
    if user is None:
        logger.error(f"User with ID {user_id} not found")
        raise credentials_exception
        
    if not user.is_active:
        logger.error(f"User with ID {user_id} is inactive")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
        
    return user


# Superuser dependency
async def get_current_superuser(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Get the current user and verify they are a superuser.
    
    Args:
        current_user: Current authenticated user
        
    Returns:
        User: Superuser
        
    Raises:
        HTTPException: If user is not a superuser
    """
    if not current_user.is_superuser:
        logger.error(f"User {current_user.id} attempted superuser action")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
        
    return current_user 