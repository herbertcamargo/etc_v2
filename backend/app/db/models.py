"""
Database models module.

This module defines the SQLAlchemy ORM models for the application's database tables.
These models represent the core data structures of the application.
"""

import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.database import Base


class User(Base):
    """
    User model representing application users.
    """
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password_hash = Column(String(128), nullable=False)
    is_premium = Column(Boolean, default=False)
    subscription_end_date = Column(DateTime, nullable=True)
    stripe_customer_id = Column(String(50), unique=True, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    transcription_sessions = relationship("TranscriptionSession", back_populates="user")
    subscriptions = relationship("Subscription", back_populates="user")

    def __str__(self) -> str:
        return f"User(id={self.id}, username={self.username}, email={self.email})"


class Video(Base):
    """
    Video model for storing YouTube video metadata.
    """
    __tablename__ = "videos"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    youtube_id = Column(String(20), unique=True, index=True, nullable=False)
    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    thumbnail_url = Column(String(255), nullable=True)
    duration = Column(Integer, nullable=True)  # Duration in seconds
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    transcription_sessions = relationship("TranscriptionSession", back_populates="video")

    def __str__(self) -> str:
        return f"Video(id={self.id}, youtube_id={self.youtube_id}, title={self.title})"


class TranscriptionSession(Base):
    """
    TranscriptionSession model for storing user transcription attempts.
    """
    __tablename__ = "transcription_sessions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    video_id = Column(UUID(as_uuid=True), ForeignKey("videos.id"), nullable=False)
    user_transcription = Column(Text, nullable=True)
    correct_transcription = Column(Text, nullable=True)
    accuracy_score = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="transcription_sessions")
    video = relationship("Video", back_populates="transcription_sessions")

    def __str__(self) -> str:
        return f"TranscriptionSession(id={self.id}, user_id={self.user_id}, video_id={self.video_id})"


class Subscription(Base):
    """
    Subscription model for storing user subscription data.
    """
    __tablename__ = "subscriptions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    stripe_subscription_id = Column(String(50), unique=True, nullable=True)
    status = Column(String(20), nullable=False)  # active, canceled, past_due
    plan_type = Column(String(20), nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="subscriptions")

    def __str__(self) -> str:
        return f"Subscription(id={self.id}, user_id={self.user_id}, status={self.status})" 