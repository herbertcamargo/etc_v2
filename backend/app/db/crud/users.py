"""
CRUD operations for User model.

This module provides functions for creating, reading, updating, and deleting User records.
"""

import uuid
from typing import Optional, List

from sqlalchemy.orm import Session

from app.core.security import get_password_hash, verify_password
from backend.app.db.models import User


def get_user_by_id(db: Session, user_id: uuid.UUID) -> Optional[User]:
    """
    Get a user by ID.
    
    Args:
        db: Database session
        user_id: User UUID
        
    Returns:
        User object if found, None otherwise
    """
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """
    Get a user by email.
    
    Args:
        db: Database session
        email: User email
        
    Returns:
        User object if found, None otherwise
    """
    return db.query(User).filter(User.email == email).first()


def get_user_by_username(db: Session, username: str) -> Optional[User]:
    """
    Get a user by username.
    
    Args:
        db: Database session
        username: Username
        
    Returns:
        User object if found, None otherwise
    """
    return db.query(User).filter(User.username == username).first()


def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
    """
    Get a list of users with pagination.
    
    Args:
        db: Database session
        skip: Number of records to skip
        limit: Maximum number of records to return
        
    Returns:
        List of User objects
    """
    return db.query(User).offset(skip).limit(limit).all()


def create_user(db: Session, username: str, email: str, password: str) -> User:
    """
    Create a new user.
    
    Args:
        db: Database session
        username: Username
        email: Email
        password: Plain text password to be hashed
        
    Returns:
        Created User object
    """
    hashed_password = get_password_hash(password)
    db_user = User(
        username=username,
        email=email,
        password_hash=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(
    db: Session, 
    user_id: uuid.UUID, 
    username: Optional[str] = None,
    email: Optional[str] = None,
    is_premium: Optional[bool] = None,
    subscription_end_date: Optional[str] = None
) -> Optional[User]:
    """
    Update a user.
    
    Args:
        db: Database session
        user_id: User UUID
        username: New username (optional)
        email: New email (optional)
        is_premium: Update premium status (optional)
        subscription_end_date: New subscription end date (optional)
        
    Returns:
        Updated User object if found, None otherwise
    """
    db_user = get_user_by_id(db, user_id)
    if not db_user:
        return None
    
    if username is not None:
        db_user.username = username
    if email is not None:
        db_user.email = email
    if is_premium is not None:
        db_user.is_premium = is_premium
    if subscription_end_date is not None:
        db_user.subscription_end_date = subscription_end_date
    
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: uuid.UUID) -> bool:
    """
    Delete a user.
    
    Args:
        db: Database session
        user_id: User UUID
        
    Returns:
        True if user was deleted, False otherwise
    """
    db_user = get_user_by_id(db, user_id)
    if not db_user:
        return False
    
    db.delete(db_user)
    db.commit()
    return True


def authenticate_user(db: Session, username: str, password: str) -> Optional[User]:
    """
    Authenticate a user.
    
    Args:
        db: Database session
        username: Username
        password: Plain text password
        
    Returns:
        User object if authentication successful, None otherwise
    """
    user = get_user_by_username(db, username)
    if not user:
        return None
    if not verify_password(password, user.password_hash):
        return None
    return user 