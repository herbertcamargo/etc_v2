"""
Transcription API tests.

This module contains tests for the transcription API endpoints.
"""

import json
from datetime import datetime, timedelta
from unittest.mock import patch
import pytest
from fastapi import status
from uuid import uuid4, UUID

from app.db.crud import users as users_crud
from app.db.crud import videos as videos_crud
from app.db.crud import transcriptions as trans_crud
from app.db.models import TranscriptionSession, Video


@pytest.fixture
def user_token(client, db_session):
    """Create a test user and return authentication token."""
    # Register test user
    user_data = {
        "username": "transtest",
        "email": "transtest@example.com",
        "password": "Password123"
    }
    client.post("/api/auth/register", json=user_data)
    
    # Login and get token
    login_response = client.post(
        "/api/auth/login", 
        data={
            "username": "transtest",
            "password": "Password123"
        }
    )
    token = login_response.json()["access_token"]
    return token


@pytest.fixture
def auth_headers(user_token):
    """Create authentication headers with token."""
    return {"Authorization": f"Bearer {user_token}"}


@pytest.fixture
def test_video(db_session):
    """Create a test video in the database."""
    video = Video(
        youtube_id="testVideo123",
        title="Test Video",
        description="This is a test video",
        thumbnail_url="https://example.com/thumb.jpg",
        duration=120  # 2 minutes
    )
    db_session.add(video)
    db_session.commit()
    db_session.refresh(video)
    return video


def test_create_transcription(client, db_session, auth_headers, test_video):
    """Test creating a new transcription session."""
    # Get test user
    user = users_crud.get_user_by_username(db_session, "transtest")
    
    # Prepare transcription data
    trans_data = {
        "video_id": str(test_video.id),
        "user_transcription": "This is my test transcription",
        "correct_transcription": "This is the correct transcription",
        "accuracy_score": 0.85
    }
    
    # Create transcription
    response = client.post(
        "/api/transcriptions/", 
        json=trans_data, 
        headers=auth_headers
    )
    
    # Check response
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    
    # Verify data
    assert data["user_id"] == str(user.id)
    assert data["video_id"] == str(test_video.id)
    assert data["user_transcription"] == trans_data["user_transcription"]
    assert data["correct_transcription"] == trans_data["correct_transcription"]
    assert data["accuracy_score"] == trans_data["accuracy_score"]
    
    # Check database
    db_trans = db_session.query(TranscriptionSession).filter(
        TranscriptionSession.id == UUID(data["id"])
    ).first()
    
    assert db_trans is not None
    assert db_trans.user_id == user.id
    assert db_trans.video_id == test_video.id


def test_create_transcription_exceeds_free_limit(client, db_session, auth_headers, test_video):
    """Test creating a transcription when free limit is exceeded."""
    # Get test user
    user = users_crud.get_user_by_username(db_session, "transtest")
    
    # Create 3 transcriptions (free limit)
    for i in range(3):
        trans = TranscriptionSession(
            user_id=user.id,
            video_id=test_video.id,
            user_transcription=f"Test {i}",
            correct_transcription=f"Correct {i}",
            accuracy_score=0.8
        )
        db_session.add(trans)
    
    db_session.commit()
    
    # Try to create a 4th transcription
    trans_data = {
        "video_id": str(test_video.id),
        "user_transcription": "This should fail",
        "correct_transcription": "This is the limit test",
        "accuracy_score": 0.7
    }
    
    response = client.post(
        "/api/transcriptions/", 
        json=trans_data, 
        headers=auth_headers
    )
    
    # Check that it fails due to limit
    assert response.status_code == status.HTTP_403_FORBIDDEN
    data = response.json()
    assert "limit" in data["detail"].lower()


def test_get_transcription(client, db_session, auth_headers, test_video):
    """Test retrieving a specific transcription."""
    # Get test user
    user = users_crud.get_user_by_username(db_session, "transtest")
    
    # Create a transcription
    trans = TranscriptionSession(
        user_id=user.id,
        video_id=test_video.id,
        user_transcription="Get test",
        correct_transcription="Correct get test",
        accuracy_score=0.9
    )
    db_session.add(trans)
    db_session.commit()
    db_session.refresh(trans)
    
    # Get the transcription
    response = client.get(
        f"/api/transcriptions/{trans.id}", 
        headers=auth_headers
    )
    
    # Check response
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    
    # Verify data
    assert data["id"] == str(trans.id)
    assert data["user_transcription"] == "Get test"
    assert data["correct_transcription"] == "Correct get test"
    assert data["accuracy_score"] == 0.9


def test_get_nonexistent_transcription(client, auth_headers):
    """Test retrieving a non-existent transcription."""
    random_id = uuid4()
    response = client.get(
        f"/api/transcriptions/{random_id}", 
        headers=auth_headers
    )
    
    # Should return not found
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_get_other_user_transcription(client, db_session, auth_headers, test_video):
    """Test retrieving another user's transcription."""
    # Create another user
    other_user = users_crud.create_user(
        db_session, 
        "otheruser", 
        "other@example.com", 
        "Password123"
    )
    
    # Create a transcription for other user
    trans = TranscriptionSession(
        user_id=other_user.id,
        video_id=test_video.id,
        user_transcription="Other user's transcription",
        correct_transcription="Correct other test",
        accuracy_score=0.8
    )
    db_session.add(trans)
    db_session.commit()
    db_session.refresh(trans)
    
    # Try to get the transcription
    response = client.get(
        f"/api/transcriptions/{trans.id}", 
        headers=auth_headers
    )
    
    # Should be forbidden
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_get_user_transcriptions(client, db_session, auth_headers, test_video):
    """Test retrieving all transcriptions for the current user."""
    # Get test user
    user = users_crud.get_user_by_username(db_session, "transtest")
    
    # Create multiple transcriptions
    for i in range(5):
        trans = TranscriptionSession(
            user_id=user.id,
            video_id=test_video.id,
            user_transcription=f"Test {i}",
            correct_transcription=f"Correct {i}",
            accuracy_score=0.7 + (i / 10)
        )
        db_session.add(trans)
    
    db_session.commit()
    
    # Get all user transcriptions
    response = client.get(
        "/api/transcriptions/me", 
        headers=auth_headers
    )
    
    # Check response
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    
    # Verify data
    assert len(data) == 5
    for i, trans in enumerate(data):
        assert trans["user_id"] == str(user.id)
        assert "user_transcription" in trans
        assert "correct_transcription" in trans
        assert "accuracy_score" in trans


def test_analyze_transcription(client, auth_headers):
    """Test analyzing transcription accuracy without saving."""
    analysis_data = {
        "user_transcription": "This is a test transcription.",
        "correct_transcription": "This is a test transcription with some extra words."
    }
    
    response = client.post(
        "/api/transcriptions/analyze", 
        json=analysis_data, 
        headers=auth_headers
    )
    
    # Check response
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    
    # Verify analysis result
    assert "accuracy_score" in data
    assert "word_count" in data
    assert "matched_words" in data
    assert "comparison" in data
    assert 0 <= data["accuracy_score"] <= 1.0


def test_delete_transcription(client, db_session, auth_headers, test_video):
    """Test deleting a transcription."""
    # Get test user
    user = users_crud.get_user_by_username(db_session, "transtest")
    
    # Create a transcription
    trans = TranscriptionSession(
        user_id=user.id,
        video_id=test_video.id,
        user_transcription="Delete test",
        correct_transcription="Correct delete test",
        accuracy_score=0.85
    )
    db_session.add(trans)
    db_session.commit()
    db_session.refresh(trans)
    
    # Delete the transcription
    response = client.delete(
        f"/api/transcriptions/{trans.id}", 
        headers=auth_headers
    )
    
    # Check response
    assert response.status_code == status.HTTP_204_NO_CONTENT
    
    # Verify transcription is deleted
    db_trans = db_session.query(TranscriptionSession).filter(
        TranscriptionSession.id == trans.id
    ).first()
    
    assert db_trans is None


def test_delete_other_user_transcription(client, db_session, auth_headers, test_video):
    """Test deleting another user's transcription."""
    # Create another user
    other_user = users_crud.create_user(
        db_session, 
        "otheruser2", 
        "other2@example.com", 
        "Password123"
    )
    
    # Create a transcription for other user
    trans = TranscriptionSession(
        user_id=other_user.id,
        video_id=test_video.id,
        user_transcription="Other user's delete test",
        correct_transcription="Correct other delete test",
        accuracy_score=0.75
    )
    db_session.add(trans)
    db_session.commit()
    db_session.refresh(trans)
    
    # Try to delete the transcription
    response = client.delete(
        f"/api/transcriptions/{trans.id}", 
        headers=auth_headers
    )
    
    # Should be forbidden
    assert response.status_code == status.HTTP_403_FORBIDDEN
    
    # Verify transcription still exists
    db_trans = db_session.query(TranscriptionSession).filter(
        TranscriptionSession.id == trans.id
    ).first()
    
    assert db_trans is not None 