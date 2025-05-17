"""
Database models for practice-related functionality.

This module defines the SQLAlchemy models for:
- Practice segments (portions of videos for transcription practice)
- Practice sessions (instances of practicing a segment)
- Practice results (outcomes of practice sessions)

Requirements fulfilled:
- Data models for practice-related entities
- Relationships between users, segments, sessions, and results
- Support for storing transcript data and comparison results
"""

import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional

from sqlalchemy import (
    Boolean, Column, DateTime, Float, ForeignKey, Integer, 
    String, Text, JSON, UniqueConstraint, func
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class PracticeSegment(Base):
    """
    Model for practice segments.
    
    A practice segment is a portion of a video that users can practice transcribing.
    """
    __tablename__ = "practice_segments"
    
    id = Column(String(36), primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Video information
    video_id = Column(String(20), nullable=False, index=True)  # YouTube video ID
    video_title = Column(String(255), nullable=True)
    video_thumbnail = Column(String(255), nullable=True)
    
    # Segment information
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    start_time = Column(Float, nullable=False)  # Start time in seconds
    end_time = Column(Float, nullable=False)    # End time in seconds
    difficulty = Column(String(10), nullable=True)  # easy, medium, hard
    language = Column(String(10), nullable=True)  # Language code (e.g., 'en', 'fr')
    
    # Transcript data
    transcript_data = Column(JSON, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="practice_segments")
    sessions = relationship("PracticeSession", back_populates="segment", cascade="all, delete-orphan")
    
    def as_dict(self) -> Dict[str, Any]:
        """Convert model to dictionary."""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "video_id": self.video_id,
            "video_title": self.video_title,
            "video_thumbnail": self.video_thumbnail,
            "title": self.title,
            "description": self.description,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "difficulty": self.difficulty,
            "language": self.language,
            "transcript_data": self.transcript_data,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }


class PracticeSession(Base):
    """
    Model for practice sessions.
    
    A practice session represents an instance of a user practicing a segment.
    """
    __tablename__ = "practice_sessions"
    
    id = Column(String(36), primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    segment_id = Column(String(36), ForeignKey("practice_segments.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Session information
    notes = Column(Text, nullable=True)
    status = Column(String(20), nullable=False, default="created")  # created, completed, abandoned
    
    # Timestamps
    started_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    completed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Result relationship (one-to-one)
    result_id = Column(String(36), ForeignKey("practice_results.id", ondelete="SET NULL"), nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="practice_sessions")
    segment = relationship("PracticeSegment", back_populates="sessions")
    result = relationship("PracticeResult", foreign_keys=[result_id], back_populates="session_result")
    results = relationship("PracticeResult", back_populates="session", 
                          primaryjoin="PracticeSession.id == PracticeResult.session_id",
                          cascade="all, delete-orphan")
    
    def as_dict(self) -> Dict[str, Any]:
        """Convert model to dictionary."""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "segment_id": self.segment_id,
            "notes": self.notes,
            "status": self.status,
            "started_at": self.started_at,
            "completed_at": self.completed_at,
            "result_id": self.result_id,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }


class PracticeResult(Base):
    """
    Model for practice results.
    
    A practice result records the outcome of a practice session, including
    the user's transcription, accuracy, and detailed comparison data.
    """
    __tablename__ = "practice_results"
    
    id = Column(String(36), primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    session_id = Column(String(36), ForeignKey("practice_sessions.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Result data
    user_transcription = Column(Text, nullable=False)
    reference_text = Column(Text, nullable=False)
    accuracy = Column(Float, nullable=False)
    comparison_data = Column(JSON, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="practice_results")
    session = relationship("PracticeSession", back_populates="results", 
                         foreign_keys=[session_id], 
                         primaryjoin="PracticeResult.session_id == PracticeSession.id")
    session_result = relationship("PracticeSession", back_populates="result", 
                                 foreign_keys="PracticeSession.result_id")
    
    def as_dict(self) -> Dict[str, Any]:
        """Convert model to dictionary."""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "session_id": self.session_id,
            "user_transcription": self.user_transcription,
            "reference_text": self.reference_text,
            "accuracy": self.accuracy,
            "comparison_data": self.comparison_data,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        } 