"""
Transcription schemas module.

This module contains Pydantic models for transcription data validation.
"""

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class TranscriptionBase(BaseModel):
    """
    Base schema for transcription data.
    """
    video_id: UUID
    user_transcription: Optional[str] = None
    correct_transcription: Optional[str] = None


class TranscriptionCreate(TranscriptionBase):
    """
    Schema for creating a new transcription session.
    """
    pass


class TranscriptionUpdate(BaseModel):
    """
    Schema for updating a transcription session.
    """
    user_transcription: Optional[str] = None
    correct_transcription: Optional[str] = None


class TranscriptionSession(TranscriptionBase):
    """
    Schema for a complete transcription session.
    """
    id: UUID
    user_id: UUID
    accuracy_score: Optional[float] = None
    created_at: datetime

    class Config:
        orm_mode = True


class TranscriptionAnalysis(BaseModel):
    """
    Schema for detailed transcription analysis.
    """
    overall_accuracy: float
    word_matches: list
    stats: dict 