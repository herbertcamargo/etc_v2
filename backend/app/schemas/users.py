"""
Pydantic schemas for user-related operations.

This module defines the request and response models for user-related API endpoints.
"""

import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, validator


class UserBase(BaseModel):
    """Base user schema with common attributes."""
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr


class UserCreate(UserBase):
    """Schema for user creation requests."""
    password: str = Field(..., min_length=8)
    
    @validator('password')
    def password_strength(cls, v):
        """Validate password strength."""
        if not any(char.isdigit() for char in v):
            raise ValueError('Password must contain at least one digit')
        if not any(char.isupper() for char in v):
            raise ValueError('Password must contain at least one uppercase letter')
        return v


class UserLogin(BaseModel):
    """Schema for user login requests."""
    username: str
    password: str


class UserUpdate(BaseModel):
    """Schema for user update requests."""
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    email: Optional[EmailStr] = None


class UserInDB(UserBase):
    """Schema for user data stored in the database."""
    id: uuid.UUID
    is_premium: bool
    subscription_end_date: Optional[datetime] = None
    stripe_customer_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True


class UserResponse(UserBase):
    """Schema for user data in responses."""
    id: uuid.UUID
    is_premium: bool
    subscription_end_date: Optional[datetime] = None
    
    class Config:
        orm_mode = True


class User(UserBase):
    """Schema for internal user representation."""
    id: uuid.UUID
    is_premium: bool
    subscription_end_date: Optional[datetime] = None
    stripe_customer_id: Optional[str] = None
    
    class Config:
        orm_mode = True


class Token(BaseModel):
    """Schema for authentication tokens."""
    access_token: str
    token_type: str


class TokenPayload(BaseModel):
    """Schema for token payload data."""
    sub: Optional[str] = None 