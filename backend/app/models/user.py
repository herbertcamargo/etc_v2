"""
User model for authentication and user management.

This module defines the SQLAlchemy model for users and their relationships
to other entities in the system, including practice-related entities.

Requirements fulfilled:
- User authentication and profile storage
- Relationships to practice segments, sessions, and results
- Support for user settings and preferences
"""

import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional

from sqlalchemy import (
    Boolean, Column, DateTime, Float, ForeignKey, Integer, 
    String, Text, JSON
)
from sqlalchemy.orm import relationship

from app.core.security import get_password_hash, verify_password
from app.db.base_class import Base


class User(Base):
    """
    User model for authentication and profile data.
    """
    __tablename__ = "users"
    
    id = Column(String(36), primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(50), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=True)
    
    # Profile information
    bio = Column(Text, nullable=True)
    avatar_url = Column(String(255), nullable=True)
    
    # Account status
    is_active = Column(Boolean, default=True, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)
    is_superuser = Column(Boolean, default=False, nullable=False)
    
    # User preferences
    preferences = Column(JSON, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships with practice entities
    practice_segments = relationship("PracticeSegment", back_populates="user", cascade="all, delete-orphan")
    practice_sessions = relationship("PracticeSession", back_populates="user", cascade="all, delete-orphan")
    practice_results = relationship("PracticeResult", back_populates="user", cascade="all, delete-orphan")
    
    def set_password(self, password: str) -> None:
        """
        Set a hashed password for the user.
        
        Args:
            password: Plain text password
        """
        self.hashed_password = get_password_hash(password)
    
    def verify_password(self, password: str) -> bool:
        """
        Verify if the provided password matches the stored hash.
        
        Args:
            password: Plain text password to verify
            
        Returns:
            True if password matches, False otherwise
        """
        return verify_password(password, self.hashed_password)
    
    def as_dict(self, include_private: bool = False) -> Dict[str, Any]:
        """
        Convert model to dictionary.
        
        Args:
            include_private: Whether to include private fields
            
        Returns:
            Dictionary representation of the user
        """
        data = {
            "id": self.id,
            "username": self.username,
            "email": self.email if include_private else None,
            "full_name": self.full_name,
            "bio": self.bio,
            "avatar_url": self.avatar_url,
            "is_active": self.is_active,
            "is_verified": self.is_verified,
            "is_superuser": self.is_superuser,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
        
        # Remove private fields if not requested
        if not include_private:
            data = {k: v for k, v in data.items() if v is not None}
        
        return data 