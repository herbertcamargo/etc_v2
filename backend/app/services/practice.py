"""
Practice Service Module

This module provides functionality for managing practice sessions,
segments, results, and related operations for the transcription
practice feature.

Requirements fulfilled:
- Practice segment creation and management
- Practice session tracking and history
- Result storage and statistics calculation
- User progress tracking
"""

import logging
import uuid
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Tuple, Union

from fastapi import Depends
from sqlalchemy import and_, desc, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.core.config import settings
from app.db.session import async_session
from app.models.practice import PracticeResult, PracticeSegment, PracticeSession

# Configure logging
logger = logging.getLogger(__name__)


class PracticeService:
    """Service for managing practice-related operations."""
    
    def __init__(self, db: AsyncSession):
        """
        Initialize the practice service.
        
        Args:
            db: Database session
        """
        self.db = db
    
    # ----- Segment Management -----
    
    async def create_segment(
        self,
        user_id: str,
        video_id: str,
        start_time: float,
        end_time: float,
        title: str,
        description: Optional[str] = None,
        difficulty: Optional[str] = None,
        language: Optional[str] = None,
        video_title: Optional[str] = None,
        video_thumbnail: Optional[str] = None,
        transcript_data: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """
        Create a new practice segment.
        
        Args:
            user_id: ID of the user creating the segment
            video_id: YouTube video ID
            start_time: Start time of segment (seconds)
            end_time: End time of segment (seconds)
            title: Title for the segment
            description: Optional description
            difficulty: Optional difficulty level
            language: Optional language code
            video_title: Optional video title
            video_thumbnail: Optional video thumbnail URL
            transcript_data: Optional transcript data for the segment
            
        Returns:
            Created segment details
        """
        # Create segment ID
        segment_id = str(uuid.uuid4())
        
        # Create current timestamp
        now = datetime.utcnow()
        
        # Prepare segment data
        segment_data = {
            "id": segment_id,
            "user_id": user_id,
            "video_id": video_id,
            "start_time": start_time,
            "end_time": end_time,
            "title": title,
            "description": description,
            "difficulty": difficulty,
            "language": language,
            "video_title": video_title,
            "video_thumbnail": video_thumbnail,
            "transcript_data": transcript_data,
            "created_at": now,
            "updated_at": now
        }
        
        # Insert segment into database
        query = PracticeSegment.__table__.insert().values(**segment_data)
        await self.db.execute(query)
        await self.db.commit()
        
        return segment_data
    
    async def get_segments(
        self,
        user_id: str,
        skip: int = 0,
        limit: int = 100,
        difficulty: Optional[str] = None,
        language: Optional[str] = None,
        search: Optional[str] = None
    ) -> Tuple[List[Dict[str, Any]], int]:
        """
        Get practice segments with optional filtering.
        
        Args:
            user_id: ID of the user
            skip: Number of items to skip
            limit: Maximum number of items to return
            difficulty: Optional filter by difficulty level
            language: Optional filter by language
            search: Optional search term
            
        Returns:
            Tuple of (segments list, total count)
        """
        # Build where conditions
        conditions = [PracticeSegment.user_id == user_id]
        
        if difficulty:
            conditions.append(PracticeSegment.difficulty == difficulty)
        
        if language:
            conditions.append(PracticeSegment.language == language)
        
        if search:
            search_term = f"%{search}%"
            conditions.append(
                (PracticeSegment.title.ilike(search_term)) | 
                (PracticeSegment.description.ilike(search_term)) |
                (PracticeSegment.video_title.ilike(search_term))
            )
        
        # Build query
        query = (
            select(PracticeSegment)
            .where(and_(*conditions))
            .order_by(desc(PracticeSegment.created_at))
            .offset(skip)
            .limit(limit)
        )
        
        # Execute query
        result = await self.db.execute(query)
        segments = result.scalars().all()
        
        # Get total count
        count_query = (
            select(func.count())
            .select_from(PracticeSegment)
            .where(and_(*conditions))
        )
        count_result = await self.db.execute(count_query)
        total = count_result.scalar()
        
        # Convert to dictionaries
        segment_dicts = [row.as_dict() for row in segments]
        
        return segment_dicts, total
    
    async def get_segment_by_id(
        self,
        segment_id: str,
        user_id: str
    ) -> Optional[Dict[str, Any]]:
        """
        Get a specific practice segment by ID.
        
        Args:
            segment_id: ID of the segment
            user_id: ID of the user
            
        Returns:
            Segment details or None if not found
        """
        query = (
            select(PracticeSegment)
            .where(
                and_(
                    PracticeSegment.id == segment_id,
                    PracticeSegment.user_id == user_id
                )
            )
        )
        
        result = await self.db.execute(query)
        segment = result.scalar_one_or_none()
        
        if segment:
            return segment.as_dict()
        return None
    
    async def update_segment(
        self,
        segment_id: str,
        user_id: str,
        **update_data
    ) -> Optional[Dict[str, Any]]:
        """
        Update a practice segment.
        
        Args:
            segment_id: ID of the segment
            user_id: ID of the user
            **update_data: Fields to update
            
        Returns:
            Updated segment details or None if not found
        """
        # Make sure the segment exists and belongs to the user
        segment = await self.get_segment_by_id(segment_id, user_id)
        if not segment:
            return None
        
        # Add updated timestamp
        update_data["updated_at"] = datetime.utcnow()
        
        # Update segment
        query = (
            PracticeSegment.__table__.update()
            .where(
                and_(
                    PracticeSegment.id == segment_id,
                    PracticeSegment.user_id == user_id
                )
            )
            .values(**update_data)
        )
        
        await self.db.execute(query)
        await self.db.commit()
        
        # Return updated segment
        return await self.get_segment_by_id(segment_id, user_id)
    
    async def delete_segment(
        self,
        segment_id: str,
        user_id: str
    ) -> bool:
        """
        Delete a practice segment.
        
        Args:
            segment_id: ID of the segment
            user_id: ID of the user
            
        Returns:
            True if deleted, False if not found
        """
        # Make sure the segment exists and belongs to the user
        segment = await self.get_segment_by_id(segment_id, user_id)
        if not segment:
            return False
        
        # Delete all related sessions and results first
        # Get all sessions for this segment
        sessions_query = (
            select(PracticeSession)
            .where(
                and_(
                    PracticeSession.segment_id == segment_id,
                    PracticeSession.user_id == user_id
                )
            )
        )
        sessions_result = await self.db.execute(sessions_query)
        sessions = sessions_result.scalars().all()
        
        # Delete all results for these sessions
        for session in sessions:
            results_delete_query = (
                PracticeResult.__table__.delete()
                .where(
                    and_(
                        PracticeResult.session_id == session.id,
                        PracticeResult.user_id == user_id
                    )
                )
            )
            await self.db.execute(results_delete_query)
        
        # Delete sessions
        sessions_delete_query = (
            PracticeSession.__table__.delete()
            .where(
                and_(
                    PracticeSession.segment_id == segment_id,
                    PracticeSession.user_id == user_id
                )
            )
        )
        await self.db.execute(sessions_delete_query)
        
        # Delete segment
        segment_delete_query = (
            PracticeSegment.__table__.delete()
            .where(
                and_(
                    PracticeSegment.id == segment_id,
                    PracticeSegment.user_id == user_id
                )
            )
        )
        await self.db.execute(segment_delete_query)
        await self.db.commit()
        
        return True
    
    # ----- Session Management -----
    
    async def create_session(
        self,
        user_id: str,
        segment_id: str,
        notes: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create a new practice session.
        
        Args:
            user_id: ID of the user creating the session
            segment_id: ID of the practice segment
            notes: Optional notes for the session
            
        Returns:
            Created session details
        """
        # Create session ID
        session_id = str(uuid.uuid4())
        
        # Create current timestamp
        now = datetime.utcnow()
        
        # Prepare session data
        session_data = {
            "id": session_id,
            "user_id": user_id,
            "segment_id": segment_id,
            "notes": notes,
            "status": "created",
            "started_at": now,
            "completed_at": None,
            "result_id": None,
            "created_at": now,
            "updated_at": now
        }
        
        # Insert session into database
        query = PracticeSession.__table__.insert().values(**session_data)
        await self.db.execute(query)
        await self.db.commit()
        
        return session_data
    
    async def get_sessions(
        self,
        user_id: str,
        skip: int = 0,
        limit: int = 100,
        segment_id: Optional[str] = None
    ) -> Tuple[List[Dict[str, Any]], int]:
        """
        Get practice sessions for a user.
        
        Args:
            user_id: ID of the user
            skip: Number of items to skip
            limit: Maximum number of items to return
            segment_id: Optional filter by segment ID
            
        Returns:
            Tuple of (sessions list, total count)
        """
        # Build where conditions
        conditions = [PracticeSession.user_id == user_id]
        
        if segment_id:
            conditions.append(PracticeSession.segment_id == segment_id)
        
        # Build query
        query = (
            select(PracticeSession)
            .where(and_(*conditions))
            .order_by(desc(PracticeSession.created_at))
            .offset(skip)
            .limit(limit)
        )
        
        # Execute query
        result = await self.db.execute(query)
        sessions = result.scalars().all()
        
        # Get total count
        count_query = (
            select(func.count())
            .select_from(PracticeSession)
            .where(and_(*conditions))
        )
        count_result = await self.db.execute(count_query)
        total = count_result.scalar()
        
        # Convert to dictionaries
        session_dicts = [row.as_dict() for row in sessions]
        
        # Enhance sessions with segment info
        enhanced_sessions = []
        for session in session_dicts:
            # Get segment info
            segment = await self.get_segment_by_id(session["segment_id"], user_id)
            if segment:
                session["segment"] = {
                    "id": segment["id"],
                    "title": segment["title"],
                    "video_id": segment["video_id"],
                    "video_title": segment["video_title"],
                    "video_thumbnail": segment["video_thumbnail"],
                    "start_time": segment["start_time"],
                    "end_time": segment["end_time"],
                    "difficulty": segment["difficulty"],
                    "language": segment["language"]
                }
            
            # Get result info if available
            if session["result_id"]:
                result = await self.get_result_by_id(session["result_id"], user_id)
                if result:
                    session["result"] = {
                        "id": result["id"],
                        "accuracy": result["accuracy"],
                        "created_at": result["created_at"]
                    }
            
            enhanced_sessions.append(session)
        
        return enhanced_sessions, total
    
    async def get_session_by_id(
        self,
        session_id: str,
        user_id: str
    ) -> Optional[Dict[str, Any]]:
        """
        Get a specific practice session by ID.
        
        Args:
            session_id: ID of the session
            user_id: ID of the user
            
        Returns:
            Session details or None if not found
        """
        query = (
            select(PracticeSession)
            .where(
                and_(
                    PracticeSession.id == session_id,
                    PracticeSession.user_id == user_id
                )
            )
        )
        
        result = await self.db.execute(query)
        session = result.scalar_one_or_none()
        
        if not session:
            return None
            
        session_dict = session.as_dict()
        
        # Enhance session with segment info
        segment = await self.get_segment_by_id(session_dict["segment_id"], user_id)
        if segment:
            session_dict["segment"] = {
                "id": segment["id"],
                "title": segment["title"],
                "video_id": segment["video_id"],
                "video_title": segment["video_title"],
                "video_thumbnail": segment["video_thumbnail"],
                "start_time": segment["start_time"],
                "end_time": segment["end_time"],
                "difficulty": segment["difficulty"],
                "language": segment["language"],
                "transcript_data": segment["transcript_data"]
            }
        
        # Get result info if available
        if session_dict["result_id"]:
            result = await self.get_result_by_id(session_dict["result_id"], user_id)
            if result:
                session_dict["result"] = result
        
        return session_dict
    
    async def update_session_with_result(
        self,
        session_id: str,
        result_id: str
    ) -> Optional[Dict[str, Any]]:
        """
        Update a practice session with a result.
        
        Args:
            session_id: ID of the session
            result_id: ID of the result
            
        Returns:
            Updated session details or None if not found
        """
        # Get the session first
        query = select(PracticeSession).where(PracticeSession.id == session_id)
        result = await self.db.execute(query)
        session = result.scalar_one_or_none()
        
        if not session:
            return None
        
        # Update session with result and mark as completed
        now = datetime.utcnow()
        update_data = {
            "status": "completed",
            "completed_at": now,
            "result_id": result_id,
            "updated_at": now
        }
        
        update_query = (
            PracticeSession.__table__.update()
            .where(PracticeSession.id == session_id)
            .values(**update_data)
        )
        
        await self.db.execute(update_query)
        await self.db.commit()
        
        # Get updated session
        return await self.get_session_by_id(session_id, session.user_id)
    
    # ----- Result Management -----
    
    async def create_result(
        self,
        user_id: str,
        session_id: str,
        user_transcription: str,
        reference_text: str,
        accuracy: float,
        comparison_data: List[Dict[str, str]]
    ) -> Dict[str, Any]:
        """
        Create a new practice result.
        
        Args:
            user_id: ID of the user
            session_id: ID of the practice session
            user_transcription: User's transcription text
            reference_text: Reference transcription text
            accuracy: Accuracy score
            comparison_data: Detailed comparison data
            
        Returns:
            Created result details
        """
        # Create result ID
        result_id = str(uuid.uuid4())
        
        # Create current timestamp
        now = datetime.utcnow()
        
        # Prepare result data
        result_data = {
            "id": result_id,
            "user_id": user_id,
            "session_id": session_id,
            "user_transcription": user_transcription,
            "reference_text": reference_text,
            "accuracy": accuracy,
            "comparison_data": comparison_data,
            "created_at": now,
            "updated_at": now
        }
        
        # Insert result into database
        query = PracticeResult.__table__.insert().values(**result_data)
        await self.db.execute(query)
        await self.db.commit()
        
        return result_data
    
    async def get_result_by_id(
        self,
        result_id: str,
        user_id: str
    ) -> Optional[Dict[str, Any]]:
        """
        Get a specific practice result by ID.
        
        Args:
            result_id: ID of the result
            user_id: ID of the user
            
        Returns:
            Result details or None if not found
        """
        query = (
            select(PracticeResult)
            .where(
                and_(
                    PracticeResult.id == result_id,
                    PracticeResult.user_id == user_id
                )
            )
        )
        
        result = await self.db.execute(query)
        result_obj = result.scalar_one_or_none()
        
        if result_obj:
            return result_obj.as_dict()
        return None
    
    async def get_user_results(
        self,
        user_id: str,
        skip: int = 0,
        limit: int = 100
    ) -> Tuple[List[Dict[str, Any]], int]:
        """
        Get all practice results for a user.
        
        Args:
            user_id: ID of the user
            skip: Number of items to skip
            limit: Maximum number of items to return
            
        Returns:
            Tuple of (results list, total count)
        """
        # Build query
        query = (
            select(PracticeResult)
            .where(PracticeResult.user_id == user_id)
            .order_by(desc(PracticeResult.created_at))
            .offset(skip)
            .limit(limit)
        )
        
        # Execute query
        result = await self.db.execute(query)
        results = result.scalars().all()
        
        # Get total count
        count_query = (
            select(func.count())
            .select_from(PracticeResult)
            .where(PracticeResult.user_id == user_id)
        )
        count_result = await self.db.execute(count_query)
        total = count_result.scalar()
        
        # Convert to dictionaries
        result_dicts = [row.as_dict() for row in results]
        
        return result_dicts, total
    
    # ----- Statistics -----
    
    async def get_user_statistics(
        self,
        user_id: str,
        time_range: str = "all"
    ) -> Dict[str, Any]:
        """
        Get practice statistics for a user.
        
        Args:
            user_id: ID of the user
            time_range: Time range (all, week, month, year)
            
        Returns:
            Dictionary containing practice statistics
        """
        # Define start date based on time range
        start_date = None
        now = datetime.utcnow()
        
        if time_range == "week":
            start_date = now - timedelta(days=7)
        elif time_range == "month":
            start_date = now - timedelta(days=30)
        elif time_range == "year":
            start_date = now - timedelta(days=365)
        
        # Build where conditions for sessions and results
        session_conditions = [PracticeSession.user_id == user_id]
        result_conditions = [PracticeResult.user_id == user_id]
        
        if start_date:
            session_conditions.append(PracticeSession.created_at >= start_date)
            result_conditions.append(PracticeResult.created_at >= start_date)
        
        # Get total sessions
        session_count_query = (
            select(func.count())
            .select_from(PracticeSession)
            .where(and_(*session_conditions))
        )
        session_count_result = await self.db.execute(session_count_query)
        total_sessions = session_count_result.scalar()
        
        # Get completed sessions
        completed_session_conditions = session_conditions.copy()
        completed_session_conditions.append(PracticeSession.status == "completed")
        
        completed_session_query = (
            select(func.count())
            .select_from(PracticeSession)
            .where(and_(*completed_session_conditions))
        )
        completed_session_result = await self.db.execute(completed_session_query)
        completed_sessions = completed_session_result.scalar()
        
        # Get total practice time
        if start_date:
            segments_query = (
                select(PracticeSegment)
                .join(
                    PracticeSession, 
                    PracticeSegment.id == PracticeSession.segment_id
                )
                .where(
                    and_(
                        PracticeSegment.user_id == user_id,
                        PracticeSession.created_at >= start_date
                    )
                )
            )
        else:
            segments_query = (
                select(PracticeSegment)
                .join(
                    PracticeSession, 
                    PracticeSegment.id == PracticeSession.segment_id
                )
                .where(PracticeSegment.user_id == user_id)
            )
        
        segments_result = await self.db.execute(segments_query)
        segments = segments_result.scalars().all()
        
        total_practice_time = sum(
            (segment.end_time - segment.start_time) for segment in segments
        )
        
        # Get average accuracy
        accuracy_query = (
            select(func.avg(PracticeResult.accuracy))
            .where(and_(*result_conditions))
        )
        accuracy_result = await self.db.execute(accuracy_query)
        avg_accuracy = accuracy_result.scalar() or 0
        
        # Get best accuracy
        best_accuracy_query = (
            select(func.max(PracticeResult.accuracy))
            .where(and_(*result_conditions))
        )
        best_accuracy_result = await self.db.execute(best_accuracy_query)
        best_accuracy = best_accuracy_result.scalar() or 0
        
        # Get recent results
        recent_results_query = (
            select(PracticeResult)
            .where(and_(*result_conditions))
            .order_by(desc(PracticeResult.created_at))
            .limit(5)
        )
        recent_results_result = await self.db.execute(recent_results_query)
        recent_results = recent_results_result.scalars().all()
        
        recent_results_list = []
        for result in recent_results:
            result_dict = result.as_dict()
            
            # Get session
            session_query = select(PracticeSession).where(PracticeSession.id == result.session_id)
            session_result = await self.db.execute(session_query)
            session = session_result.scalar_one_or_none()
            
            if session:
                # Get segment
                segment_query = select(PracticeSegment).where(PracticeSegment.id == session.segment_id)
                segment_result = await self.db.execute(segment_query)
                segment = segment_result.scalar_one_or_none()
                
                if segment:
                    result_dict["segment"] = {
                        "id": segment.id,
                        "title": segment.title,
                        "video_id": segment.video_id,
                        "video_title": segment.video_title,
                        "difficulty": segment.difficulty
                    }
            
            recent_results_list.append(result_dict)
        
        # Compile statistics
        stats = {
            "total_sessions": total_sessions,
            "completed_sessions": completed_sessions,
            "completion_rate": (completed_sessions / total_sessions if total_sessions > 0 else 0),
            "total_practice_time": total_practice_time,
            "average_accuracy": avg_accuracy,
            "best_accuracy": best_accuracy,
            "recent_results": recent_results_list,
            "time_range": time_range
        }
        
        return stats


# Dependency to get practice service
async def get_practice_service(db: AsyncSession = Depends(get_db)) -> PracticeService:
    """
    Get an instance of the practice service.
    
    Args:
        db: Database session
        
    Returns:
        Practice service instance
    """
    return PracticeService(db) 