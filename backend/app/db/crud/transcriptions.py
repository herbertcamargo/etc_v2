"""
CRUD operations for transcription sessions.

This module provides functions for creating, reading, updating, and deleting
transcription sessions in the database.
"""

from typing import List, Optional
from uuid import UUID

from sqlalchemy.orm import Session

from app.db.models import TranscriptionSession, Video
from app.schemas import transcriptions as schemas


def get_transcription(db: Session, transcription_id: UUID) -> Optional[TranscriptionSession]:
    """
    Get a transcription session by ID.
    
    Args:
        db: Database session
        transcription_id: UUID of the transcription session
        
    Returns:
        TranscriptionSession if found, None otherwise
    """
    return db.query(TranscriptionSession).filter(TranscriptionSession.id == transcription_id).first()


def get_user_transcriptions(
    db: Session, user_id: UUID, skip: int = 0, limit: int = 100
) -> List[TranscriptionSession]:
    """
    Get all transcription sessions for a specific user.
    
    Args:
        db: Database session
        user_id: UUID of the user
        skip: Number of records to skip (for pagination)
        limit: Maximum number of records to return
        
    Returns:
        List of TranscriptionSession objects
    """
    return (
        db.query(TranscriptionSession)
        .filter(TranscriptionSession.user_id == user_id)
        .order_by(TranscriptionSession.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


def create_transcription(
    db: Session, 
    transcription: schemas.TranscriptionCreate, 
    user_id: UUID,
    accuracy_score: Optional[float] = None
) -> TranscriptionSession:
    """
    Create a new transcription session.
    
    Args:
        db: Database session
        transcription: TranscriptionCreate schema with session data
        user_id: UUID of the user creating the session
        accuracy_score: Optional accuracy score (0-1)
        
    Returns:
        The created TranscriptionSession object
    """
    # Create the transcription session
    db_transcription = TranscriptionSession(
        user_id=user_id,
        video_id=transcription.video_id,
        user_transcription=transcription.user_transcription,
        correct_transcription=transcription.correct_transcription,
        accuracy_score=accuracy_score
    )
    
    db.add(db_transcription)
    db.commit()
    db.refresh(db_transcription)
    
    return db_transcription


def update_transcription(
    db: Session,
    transcription_id: UUID,
    update_data: schemas.TranscriptionUpdate,
    accuracy_score: Optional[float] = None
) -> Optional[TranscriptionSession]:
    """
    Update an existing transcription session.
    
    Args:
        db: Database session
        transcription_id: UUID of the transcription to update
        update_data: TranscriptionUpdate schema with fields to update
        accuracy_score: Optional accuracy score (0-1)
        
    Returns:
        The updated TranscriptionSession object or None if not found
    """
    db_transcription = get_transcription(db=db, transcription_id=transcription_id)
    if not db_transcription:
        return None
    
    # Update the fields if provided
    if update_data.user_transcription is not None:
        db_transcription.user_transcription = update_data.user_transcription
    
    if update_data.correct_transcription is not None:
        db_transcription.correct_transcription = update_data.correct_transcription
    
    if accuracy_score is not None:
        db_transcription.accuracy_score = accuracy_score
    
    db.commit()
    db.refresh(db_transcription)
    
    return db_transcription


def delete_transcription(db: Session, transcription_id: UUID) -> bool:
    """
    Delete a transcription session.
    
    Args:
        db: Database session
        transcription_id: UUID of the transcription to delete
        
    Returns:
        True if deleted, False if not found
    """
    db_transcription = get_transcription(db=db, transcription_id=transcription_id)
    if not db_transcription:
        return False
    
    db.delete(db_transcription)
    db.commit()
    
    return True 