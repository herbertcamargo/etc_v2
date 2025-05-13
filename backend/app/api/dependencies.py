"""
API dependency functions.

This module provides common dependencies used across API routes.
"""

from typing import Generator

from fastapi import Depends
from sqlalchemy.orm import Session

from app.api.routes.auth import get_current_user
from app.core.exceptions import PaymentRequiredError
from app.db.database import get_db
from app.db.models import User


def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    """
    Get the current active user.
    
    Args:
        current_user: The authenticated user from the token
        
    Returns:
        User: The current active user
    """
    return current_user


def get_current_premium_user(current_user: User = Depends(get_current_user)) -> User:
    """
    Get the current user and verify premium status.
    
    Args:
        current_user: The authenticated user from the token
        
    Returns:
        User: The current premium user
        
    Raises:
        PaymentRequiredError: If user doesn't have premium status
    """
    if not current_user.is_premium:
        raise PaymentRequiredError("This feature requires a premium subscription")
    return current_user 