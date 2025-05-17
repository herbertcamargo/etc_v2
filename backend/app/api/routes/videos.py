# backend/app/api/routes/videos.py

# This file will contain the routes for handling video-related operations

"""
API routes for video-related operations.

This module provides endpoints for:
1. Searching YouTube videos
2. Retrieving video details
3. Fetching video transcripts
4. Comparing user transcriptions with reference transcripts

Requirements fulfilled:
- YouTube video search and metadata retrieval
- Transcript fetch and processing
- Transcription comparison functionality
"""

import logging
from typing import Any, Dict, List, Optional, Union

from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, validator

from app.api.deps import get_current_user
from app.core.config import settings
from app.models.user import User
from app.services.transcription_comparer import get_detailed_comparison
from app.services.youtube import YouTubeService, get_youtube_service

# Configure logging
logger = logging.getLogger(__name__)

# Create router
router = APIRouter()


# ----- Pydantic Models -----

class VideoSearchQuery(BaseModel):
    """Model for video search parameters."""
    query: str = Field(..., description="Search query term")
    max_results: int = Field(10, description="Maximum number of results to return", ge=1, le=50)
    language: Optional[str] = Field(None, description="Language preference (ISO 639-1 code)")


class TranscriptRequest(BaseModel):
    """Model for requesting video transcript."""
    video_id: str = Field(..., description="YouTube video ID")
    language: Optional[str] = Field(None, description="Preferred language for transcript (ISO 639-1 code)")


class TranscriptionCompareRequest(BaseModel):
    """Model for comparing user transcription with reference."""
    video_id: str = Field(..., description="YouTube video ID")
    user_transcription: str = Field(..., description="User's transcription text")
    segment_start: Optional[float] = Field(None, description="Start time of segment (seconds)")
    segment_end: Optional[float] = Field(None, description="End time of segment (seconds)")
    language: Optional[str] = Field(None, description="Language of the transcript (ISO 639-1 code)")
    
    @validator('user_transcription')
    def validate_transcription(cls, v):
        """Validate that user transcription is not empty."""
        if not v.strip():
            raise ValueError("User transcription cannot be empty")
        return v


# ----- Endpoints -----

@router.post("/search", response_model=Dict[str, Any], status_code=status.HTTP_200_OK)
async def search_videos(
    search_params: VideoSearchQuery,
    youtube_service: YouTubeService = Depends(get_youtube_service)
) -> Dict[str, Any]:
    """
    Search for YouTube videos based on the provided query.
    
    Args:
        search_params: Video search parameters
        youtube_service: YouTube service instance
        
    Returns:
        Dictionary containing search results
    """
    try:
        results = await youtube_service.search_videos(
            query=search_params.query,
            max_results=search_params.max_results,
            language=search_params.language
        )
        return {"results": results}
    except Exception as e:
        logger.error(f"Error searching videos: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to search videos"
        )


@router.get("/details/{video_id}", response_model=Dict[str, Any], status_code=status.HTTP_200_OK)
async def get_video_details(
    video_id: str,
    youtube_service: YouTubeService = Depends(get_youtube_service)
) -> Dict[str, Any]:
    """
    Get details for a specific YouTube video.
    
    Args:
        video_id: YouTube video ID
        youtube_service: YouTube service instance
        
    Returns:
        Dictionary containing video details
    """
    try:
        video_details = await youtube_service.get_video_details(video_id=video_id)
        if not video_details:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Video not found"
            )
        return video_details
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting video details: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve video details"
        )


@router.post("/transcript", response_model=Dict[str, Any], status_code=status.HTTP_200_OK)
async def get_video_transcript(
    transcript_request: TranscriptRequest,
    youtube_service: YouTubeService = Depends(get_youtube_service)
) -> Dict[str, Any]:
    """
    Get transcript for a YouTube video.
    
    Args:
        transcript_request: Transcript request parameters
        youtube_service: YouTube service instance
        
    Returns:
        Dictionary containing transcript data
    """
    try:
        transcript = await youtube_service.get_transcript(
            video_id=transcript_request.video_id,
            language=transcript_request.language
        )
        if not transcript:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Transcript not available for this video"
            )
        return {"transcript": transcript}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting transcript: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve transcript"
        )


@router.post("/compare-transcription", response_model=Dict[str, Any], status_code=status.HTTP_200_OK)
async def compare_transcription(
    compare_request: TranscriptionCompareRequest,
    youtube_service: YouTubeService = Depends(get_youtube_service),
    current_user: User = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Compare user transcription with reference transcript from YouTube video.
    
    Args:
        compare_request: Transcription comparison request
        youtube_service: YouTube service instance
        current_user: Authenticated user
        
    Returns:
        Dictionary containing comparison results
    """
    try:
        # Get the reference transcript
        transcript = await youtube_service.get_transcript(
            video_id=compare_request.video_id,
            language=compare_request.language
        )
        
        if not transcript:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Reference transcript not available for this video"
            )
        
        # Extract specific segment if requested
        reference_text = ""
        if compare_request.segment_start is not None and compare_request.segment_end is not None:
            # Filter transcript entries within the requested segment
            segment_entries = [
                entry for entry in transcript
                if (entry["start"] >= compare_request.segment_start and
                    entry["start"] < compare_request.segment_end)
            ]
            reference_text = " ".join([entry["text"] for entry in segment_entries])
        else:
            # Use entire transcript
            reference_text = " ".join([entry["text"] for entry in transcript])
        
        if not reference_text:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No reference text available for the specified segment"
            )
        
        # Compare transcriptions
        comparison, accuracy, stats = get_detailed_comparison(
            user_text=compare_request.user_transcription,
            reference_text=reference_text
        )
        
        # Return comparison results
        return {
            "comparison": comparison,
            "accuracy": accuracy,
            "statistics": stats,
            "reference_text": reference_text
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error comparing transcription: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to compare transcription"
        )


@router.get("/trending", response_model=Dict[str, Any], status_code=status.HTTP_200_OK)
async def get_trending_videos(
    category: Optional[str] = None,
    region_code: Optional[str] = None,
    max_results: int = Query(10, ge=1, le=50),
    youtube_service: YouTubeService = Depends(get_youtube_service)
) -> Dict[str, Any]:
    """
    Get trending YouTube videos, optionally filtered by category and region.
    
    Args:
        category: Optional video category
        region_code: Optional region code (ISO 3166-1 alpha-2)
        max_results: Maximum number of results to return
        youtube_service: YouTube service instance
        
    Returns:
        Dictionary containing trending videos
    """
    try:
        trending_videos = await youtube_service.get_trending_videos(
            category=category,
            region_code=region_code,
            max_results=max_results
        )
        return {"results": trending_videos}
    except Exception as e:
        logger.error(f"Error getting trending videos: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve trending videos"
        )


@router.get("/categories", response_model=Dict[str, Any], status_code=status.HTTP_200_OK)
async def get_video_categories(
    region_code: Optional[str] = None,
    youtube_service: YouTubeService = Depends(get_youtube_service)
) -> Dict[str, Any]:
    """
    Get available YouTube video categories.
    
    Args:
        region_code: Optional region code (ISO 3166-1 alpha-2)
        youtube_service: YouTube service instance
        
    Returns:
        Dictionary containing video categories
    """
    try:
        categories = await youtube_service.get_video_categories(region_code=region_code)
        return {"categories": categories}
    except Exception as e:
        logger.error(f"Error getting video categories: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve video categories"
        )