"""
Authentication API routes.

This module provides endpoints for user authentication and management.

Requirements fulfilled:
- User registration and login
- Token-based authentication
- User profile management
"""

import logging
from datetime import timedelta
from typing import Any, Dict

from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, get_db
from app.core.config import settings
from app.core.security import create_access_token, get_password_hash, verify_password
from app.models.user import User

# Configure logging
logger = logging.getLogger(__name__)

# Create router
router = APIRouter()


# ----- Pydantic Models -----

class UserCreate(BaseModel):
    """Model for user registration."""
    email: EmailStr = Field(..., description="User's email address")
    username: str = Field(..., description="User's username", min_length=3, max_length=50)
    password: str = Field(..., description="User's password", min_length=8)
    full_name: str = Field(None, description="User's full name")


class UserLogin(BaseModel):
    """Model for user login."""
    email: EmailStr = Field(..., description="User's email address")
    password: str = Field(..., description="User's password")


class Token(BaseModel):
    """Model for authentication token."""
    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field("bearer", description="Token type")


class UserOut(BaseModel):
    """Model for user data response."""
    id: str = Field(..., description="User ID")
    email: EmailStr = Field(..., description="User's email address")
    username: str = Field(..., description="User's username")
    full_name: str = Field(None, description="User's full name")
    is_active: bool = Field(..., description="Whether user is active")
    is_verified: bool = Field(..., description="Whether user is verified")
    is_superuser: bool = Field(..., description="Whether user is a superuser")


# ----- Endpoints -----

@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def register_user(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db)
) -> Any:
    """
    Register a new user.
    
    Args:
        user_data: User registration data
        db: Database session
        
    Returns:
        Newly created user data
    """
    # Check if email already exists
    email_query = select(User).where(User.email == user_data.email)
    email_result = await db.execute(email_query)
    if email_result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Check if username already exists
    username_query = select(User).where(User.username == user_data.username)
    username_result = await db.execute(username_query)
    if username_result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken"
        )
    
    # Create new user
    user = User(
        email=user_data.email,
        username=user_data.username,
        full_name=user_data.full_name,
        is_active=True,
        is_verified=False,
        is_superuser=False
    )
    
    # Set password hash
    user.set_password(user_data.password)
    
    # Add user to database
    db.add(user)
    await db.commit()
    await db.refresh(user)
    
    return user


@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
) -> Dict[str, str]:
    """
    OAuth2 compatible token login.
    
    Args:
        form_data: OAuth2 form data
        db: Database session
        
    Returns:
        Access token
    """
    # Authenticate user
    query = select(User).where(
        (User.email == form_data.username) | (User.username == form_data.username)
    )
    result = await db.execute(query)
    user = result.scalar_one_or_none()
    
    if not user or not user.verify_password(form_data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email/username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        subject=user.id,
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


@router.post("/login", response_model=Token)
async def login(
    login_data: UserLogin,
    db: AsyncSession = Depends(get_db)
) -> Dict[str, str]:
    """
    Login with email and password.
    
    Args:
        login_data: Login credentials
        db: Database session
        
    Returns:
        Access token
    """
    # Authenticate user
    query = select(User).where(User.email == login_data.email)
    result = await db.execute(query)
    user = result.scalar_one_or_none()
    
    if not user or not user.verify_password(login_data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        subject=user.id,
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


@router.get("/me", response_model=UserOut)
async def get_current_user_data(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Get current user data.
    
    Args:
        current_user: Current authenticated user
        
    Returns:
        User data
    """
    return current_user


@router.post("/change-password", response_model=Dict[str, str])
async def change_password(
    current_password: str = Body(...),
    new_password: str = Body(..., min_length=8),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> Dict[str, str]:
    """
    Change user password.
    
    Args:
        current_password: Current password
        new_password: New password
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        Success message
    """
    # Verify current password
    if not current_user.verify_password(current_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect password"
        )
    
    # Update password
    current_user.set_password(new_password)
    
    # Save changes
    db.add(current_user)
    await db.commit()
    
    return {"message": "Password changed successfully"} 