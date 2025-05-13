"""
Transcription routes module.

This module contains the API endpoints for managing transcription sessions.
It provides endpoints for creating, retrieving, and analyzing transcriptions.
"""

from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user, get_db
from app.db.crud import transcriptions as crud
from app.schemas import transcriptions as schemas
from app.schemas.users import User
from app.services.transcription import compare_transcriptions, get_detailed_comparison

router = APIRouter(
    prefix="/transcriptions",
    tags=["transcriptions"],
)


@router.post("/", response_model=schemas.TranscriptionSession)
async def create_transcription(
    transcription: schemas.TranscriptionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Create a new transcription session.
    """
    # Calculate accuracy if both transcriptions are provided
    accuracy_score = None
    if transcription.user_transcription and transcription.correct_transcription:
        accuracy_score = compare_transcriptions(
            transcription.user_transcription,
            transcription.correct_transcription
        )
    
    return crud.create_transcription(
        db=db,
        transcription=transcription,
        user_id=current_user.id,
        accuracy_score=accuracy_score
    )


@router.get("/", response_model=List[schemas.TranscriptionSession])
async def read_transcriptions(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Retrieve all transcription sessions for the current user.
    """
    return crud.get_user_transcriptions(
        db=db,
        user_id=current_user.id,
        skip=skip,
        limit=limit
    )


@router.get("/{transcription_id}", response_model=schemas.TranscriptionSession)
async def read_transcription(
    transcription_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Retrieve a specific transcription session.
    """
    transcription = crud.get_transcription(db=db, transcription_id=transcription_id)
    if not transcription:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transcription not found"
        )
    
    if transcription.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this resource"
        )
    
    return transcription


@router.put("/{transcription_id}", response_model=schemas.TranscriptionSession)
async def update_transcription(
    transcription_id: UUID,
    update_data: schemas.TranscriptionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Update a transcription session.
    """
    transcription = crud.get_transcription(db=db, transcription_id=transcription_id)
    if not transcription:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transcription not found"
        )
    
    if transcription.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this resource"
        )
    
    # Calculate accuracy if both transcriptions are provided
    accuracy_score = None
    if update_data.user_transcription and update_data.correct_transcription:
        accuracy_score = compare_transcriptions(
            update_data.user_transcription,
            update_data.correct_transcription
        )
    
    return crud.update_transcription(
        db=db,
        transcription_id=transcription_id,
        update_data=update_data,
        accuracy_score=accuracy_score
    )


@router.delete("/{transcription_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_transcription(
    transcription_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Delete a transcription session.
    """
    transcription = crud.get_transcription(db=db, transcription_id=transcription_id)
    if not transcription:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transcription not found"
        )
    
    if transcription.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this resource"
        )
    
    crud.delete_transcription(db=db, transcription_id=transcription_id)


@router.post("/analyze", response_model=schemas.TranscriptionAnalysis)
async def analyze_transcription(
    user_text: str,
    reference_text: str,
    current_user: User = Depends(get_current_user),
):
    """
    Analyze and compare transcription texts without saving to the database.
    
    Returns detailed analysis with word-by-word comparison and statistics.
    """
    if not user_text or not reference_text:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Both user text and reference text are required"
        )
    
    analysis_result = get_detailed_comparison(user_text, reference_text)
    return analysis_result 