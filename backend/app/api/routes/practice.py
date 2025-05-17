"""
API routes for transcription practice-related operations.

This module provides endpoints for:
1. Managing practice sessions
2. Retrieving practice history and statistics
3. Saving transcription practice results
4. Creating and retrieving practice segments

Requirements fulfilled:
- Practice session management
- User progress tracking
- History and statistics retrieval
- Practice segment management
"""

import logging
from datetime import datetime
from typing import Any, Dict, List, Optional, Union

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, Field, validator

from app.api.deps import get_current_user, get_db
from app.core.config import settings
from app.models.practice import PracticeSession, PracticeSegment, PracticeResult
from app.models.user import User
from app.services.practice import PracticeService, get_practice_service
from app.services.youtube import YouTubeService, get_youtube_service

# Configure logging
logger = logging.getLogger(__name__)

# Create router
router = APIRouter()


# ----- Pydantic Models -----

class PracticeSegmentCreate(BaseModel):
    """Model for creating a practice segment."""
    video_id: str = Field(..., description="YouTube video ID")
    start_time: float = Field(..., description="Start time of segment (seconds)", ge=0)
    end_time: float = Field(..., description="End time of segment (seconds)", gt=0)
    title: str = Field(..., description="Title for the segment")
    description: Optional[str] = Field(None, description="Description of the segment")
    difficulty: Optional[str] = Field(None, description="Difficulty level (easy, medium, hard)")
    language: Optional[str] = Field(None, description="Language of the segment (ISO 639-1 code)")
    
    @validator('end_time')
    def validate_end_time(cls, v, values):
        """Validate that end_time is greater than start_time."""
        if 'start_time' in values and v <= values['start_time']:
            raise ValueError("End time must be greater than start time")
        return v


class PracticeSessionCreate(BaseModel):
    """Model for creating a practice session."""
    segment_id: str = Field(..., description="ID of the practice segment")
    notes: Optional[str] = Field(None, description="User notes for this session")


class PracticeResultCreate(BaseModel):
    """Model for creating a practice result."""
    session_id: str = Field(..., description="ID of the practice session")
    user_transcription: str = Field(..., description="User's transcription text")
    accuracy: Optional[float] = Field(None, description="Calculated accuracy score")
    comparison_data: Optional[List[Dict[str, Any]]] = Field(None, description="Detailed comparison data")
    
    @validator('user_transcription')
    def validate_transcription(cls, v):
        """Validate that user transcription is not empty."""
        if not v.strip():
            raise ValueError("User transcription cannot be empty")
        return v


# ----- Endpoints -----

@router.post("/segments", response_model=Dict[str, Any], status_code=status.HTTP_201_CREATED)
async def create_practice_segment(
    segment_data: PracticeSegmentCreate,
    practice_service: PracticeService = Depends(get_practice_service),
    youtube_service: YouTubeService = Depends(get_youtube_service),
    current_user: User = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Create a new practice segment.
    
    Args:
        segment_data: Practice segment data
        practice_service: Practice service instance
        youtube_service: YouTube service instance
        current_user: Authenticated user
        
    Returns:
        Dictionary containing created segment details
    """
    try:
        # Verify the video exists
        video_details = await youtube_service.get_video_details(video_id=segment_data.video_id)
        if not video_details:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Video not found"
            )
        
        # Verify transcript is available
        transcript = await youtube_service.get_transcript(
            video_id=segment_data.video_id,
            language=segment_data.language
        )
        if not transcript:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No transcript available for this video"
            )
        
        # Filter transcript for the segment
        segment_transcript = [
            entry for entry in transcript
            if entry["start"] >= segment_data.start_time and entry["start"] < segment_data.end_time
        ]
        
        if not segment_transcript:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No transcript available for the specified segment time range"
            )
        
        # Create segment
        segment = await practice_service.create_segment(
            user_id=current_user.id,
            video_id=segment_data.video_id,
            start_time=segment_data.start_time,
            end_time=segment_data.end_time,
            title=segment_data.title,
            description=segment_data.description,
            difficulty=segment_data.difficulty,
            language=segment_data.language,
            video_title=video_details.get("title", ""),
            video_thumbnail=video_details.get("thumbnail_url", ""),
            transcript_data=segment_transcript
        )
        
        return {
            "message": "Practice segment created successfully",
            "segment": segment
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating practice segment: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create practice segment"
        )


@router.get("/segments", response_model=Dict[str, Any], status_code=status.HTTP_200_OK)
async def get_practice_segments(
    skip: int = 0,
    limit: int = 100,
    difficulty: Optional[str] = None,
    language: Optional[str] = None,
    search: Optional[str] = None,
    practice_service: PracticeService = Depends(get_practice_service),
    current_user: User = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Get practice segments with optional filtering.
    
    Args:
        skip: Number of items to skip
        limit: Maximum number of items to return
        difficulty: Optional filter by difficulty level
        language: Optional filter by language
        search: Optional search term
        practice_service: Practice service instance
        current_user: Authenticated user
        
    Returns:
        Dictionary containing segment list and count
    """
    try:
        segments, total = await practice_service.get_segments(
            user_id=current_user.id,
            skip=skip,
            limit=limit,
            difficulty=difficulty,
            language=language,
            search=search
        )
        
        return {
            "segments": segments,
            "total": total
        }
        
    except Exception as e:
        logger.error(f"Error getting practice segments: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve practice segments"
        )


@router.get("/segments/{segment_id}", response_model=Dict[str, Any], status_code=status.HTTP_200_OK)
async def get_practice_segment(
    segment_id: str,
    practice_service: PracticeService = Depends(get_practice_service),
    current_user: User = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Get a specific practice segment by ID.
    
    Args:
        segment_id: ID of the practice segment
        practice_service: Practice service instance
        current_user: Authenticated user
        
    Returns:
        Dictionary containing segment details
    """
    try:
        segment = await practice_service.get_segment_by_id(
            segment_id=segment_id,
            user_id=current_user.id
        )
        
        if not segment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Practice segment not found"
            )
            
        return segment
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting practice segment: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve practice segment"
        )


@router.delete("/segments/{segment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_practice_segment(
    segment_id: str,
    practice_service: PracticeService = Depends(get_practice_service),
    current_user: User = Depends(get_current_user)
) -> None:
    """
    Delete a practice segment.
    
    Args:
        segment_id: ID of the practice segment
        practice_service: Practice service instance
        current_user: Authenticated user
    """
    try:
        # Check if segment exists and belongs to user
        segment = await practice_service.get_segment_by_id(
            segment_id=segment_id,
            user_id=current_user.id
        )
        
        if not segment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Practice segment not found"
            )
        
        # Delete segment
        await practice_service.delete_segment(segment_id=segment_id, user_id=current_user.id)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting practice segment: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete practice segment"
        )


@router.post("/sessions", response_model=Dict[str, Any], status_code=status.HTTP_201_CREATED)
async def create_practice_session(
    session_data: PracticeSessionCreate,
    practice_service: PracticeService = Depends(get_practice_service),
    current_user: User = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Create a new practice session.
    
    Args:
        session_data: Practice session data
        practice_service: Practice service instance
        current_user: Authenticated user
        
    Returns:
        Dictionary containing created session details
    """
    try:
        # Check if segment exists
        segment = await practice_service.get_segment_by_id(
            segment_id=session_data.segment_id,
            user_id=current_user.id
        )
        
        if not segment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Practice segment not found"
            )
        
        # Create session
        session = await practice_service.create_session(
            user_id=current_user.id,
            segment_id=session_data.segment_id,
            notes=session_data.notes
        )
        
        return {
            "message": "Practice session created successfully",
            "session": session
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating practice session: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create practice session"
        )


@router.get("/sessions", response_model=Dict[str, Any], status_code=status.HTTP_200_OK)
async def get_practice_sessions(
    skip: int = 0,
    limit: int = 100,
    segment_id: Optional[str] = None,
    practice_service: PracticeService = Depends(get_practice_service),
    current_user: User = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Get practice sessions for the current user.
    
    Args:
        skip: Number of items to skip
        limit: Maximum number of items to return
        segment_id: Optional filter by segment ID
        practice_service: Practice service instance
        current_user: Authenticated user
        
    Returns:
        Dictionary containing session list and count
    """
    try:
        sessions, total = await practice_service.get_sessions(
            user_id=current_user.id,
            skip=skip,
            limit=limit,
            segment_id=segment_id
        )
        
        return {
            "sessions": sessions,
            "total": total
        }
        
    except Exception as e:
        logger.error(f"Error getting practice sessions: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve practice sessions"
        )


@router.get("/sessions/{session_id}", response_model=Dict[str, Any], status_code=status.HTTP_200_OK)
async def get_practice_session(
    session_id: str,
    practice_service: PracticeService = Depends(get_practice_service),
    current_user: User = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Get a specific practice session by ID.
    
    Args:
        session_id: ID of the practice session
        practice_service: Practice service instance
        current_user: Authenticated user
        
    Returns:
        Dictionary containing session details
    """
    try:
        session = await practice_service.get_session_by_id(
            session_id=session_id,
            user_id=current_user.id
        )
        
        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Practice session not found"
            )
            
        return session
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting practice session: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve practice session"
        )


@router.post("/results", response_model=Dict[str, Any], status_code=status.HTTP_201_CREATED)
async def create_practice_result(
    result_data: PracticeResultCreate,
    practice_service: PracticeService = Depends(get_practice_service),
    youtube_service: YouTubeService = Depends(get_youtube_service),
    current_user: User = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Create a practice result for a session.
    
    Args:
        result_data: Practice result data
        practice_service: Practice service instance
        youtube_service: YouTube service instance
        current_user: Authenticated user
        
    Returns:
        Dictionary containing created result details
    """
    try:
        # Check if session exists and belongs to user
        session = await practice_service.get_session_by_id(
            session_id=result_data.session_id,
            user_id=current_user.id
        )
        
        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Practice session not found"
            )
        
        # Get the segment for this session
        segment = await practice_service.get_segment_by_id(
            segment_id=session["segment_id"],
            user_id=current_user.id
        )
        
        if not segment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Practice segment not found"
            )
        
        # Get transcript text from segment
        transcript_data = segment.get("transcript_data", [])
        reference_text = " ".join([entry["text"] for entry in transcript_data])
        
        if not reference_text:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No reference text available for comparison"
            )
        
        # We can use the pre-computed accuracy if provided, 
        # or calculate it here if not provided
        accuracy = result_data.accuracy
        comparison_data = result_data.comparison_data
        
        if accuracy is None or comparison_data is None:
            # Import and use transcription comparison module
            from app.services.transcription_comparer import get_detailed_comparison
            
            comparison, accuracy, stats = get_detailed_comparison(
                user_text=result_data.user_transcription,
                reference_text=reference_text
            )
            comparison_data = comparison
        
        # Create result
        result = await practice_service.create_result(
            user_id=current_user.id,
            session_id=result_data.session_id,
            user_transcription=result_data.user_transcription,
            reference_text=reference_text,
            accuracy=accuracy,
            comparison_data=comparison_data
        )
        
        # Update session with result
        await practice_service.update_session_with_result(
            session_id=result_data.session_id,
            result_id=result["id"]
        )
        
        return {
            "message": "Practice result created successfully",
            "result": result
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating practice result: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create practice result"
        )


@router.get("/results/{result_id}", response_model=Dict[str, Any], status_code=status.HTTP_200_OK)
async def get_practice_result(
    result_id: str,
    practice_service: PracticeService = Depends(get_practice_service),
    current_user: User = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Get a specific practice result by ID.
    
    Args:
        result_id: ID of the practice result
        practice_service: Practice service instance
        current_user: Authenticated user
        
    Returns:
        Dictionary containing result details
    """
    try:
        result = await practice_service.get_result_by_id(
            result_id=result_id,
            user_id=current_user.id
        )
        
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Practice result not found"
            )
            
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting practice result: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve practice result"
        )


@router.get("/statistics", response_model=Dict[str, Any], status_code=status.HTTP_200_OK)
async def get_practice_statistics(
    time_range: Optional[str] = "all",  # all, week, month, year
    practice_service: PracticeService = Depends(get_practice_service),
    current_user: User = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Get practice statistics for the current user.
    
    Args:
        time_range: Time range for statistics (all, week, month, year)
        practice_service: Practice service instance
        current_user: Authenticated user
        
    Returns:
        Dictionary containing practice statistics
    """
    try:
        stats = await practice_service.get_user_statistics(
            user_id=current_user.id,
            time_range=time_range
        )
        
        return stats
        
    except Exception as e:
        logger.error(f"Error getting practice statistics: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve practice statistics"
        ) 