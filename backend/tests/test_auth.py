"""
Authentication API tests.

This module contains tests for the authentication API endpoints.
"""

import pytest
from fastapi import status

from app.db.crud import users as users_crud


def test_register_user(client, db_session):
    """Test user registration."""
    # Prepare test data
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "Password123"
    }
    
    # Send registration request
    response = client.post("/api/auth/register", json=user_data)
    
    # Check response
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["username"] == user_data["username"]
    assert data["email"] == user_data["email"]
    assert "id" in data
    
    # Check that user was created in the database
    db_user = users_crud.get_user_by_username(db_session, user_data["username"])
    assert db_user is not None
    assert db_user.username == user_data["username"]
    assert db_user.email == user_data["email"]


def test_register_duplicate_username(client, db_session):
    """Test registration with duplicate username."""
    # Create a user first
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "Password123"
    }
    client.post("/api/auth/register", json=user_data)
    
    # Try to register with the same username but different email
    duplicate_data = {
        "username": "testuser",
        "email": "different@example.com",
        "password": "Password123"
    }
    
    response = client.post("/api/auth/register", json=duplicate_data)
    
    # Check response
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    data = response.json()
    assert "already registered" in data["detail"]


def test_login(client, db_session):
    """Test user login."""
    # Create a user first
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "Password123"
    }
    client.post("/api/auth/register", json=user_data)
    
    # Try to login
    login_data = {
        "username": "testuser",
        "password": "Password123"
    }
    
    response = client.post("/api/auth/login", data=login_data)
    
    # Check response
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_invalid_credentials(client, db_session):
    """Test login with invalid credentials."""
    # Create a user first
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "Password123"
    }
    client.post("/api/auth/register", json=user_data)
    
    # Try to login with wrong password
    login_data = {
        "username": "testuser",
        "password": "WrongPassword123"
    }
    
    response = client.post("/api/auth/login", data=login_data)
    
    # Check response
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_get_current_user(client, db_session):
    """Test getting current user information."""
    # Create a user and get token
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "Password123"
    }
    client.post("/api/auth/register", json=user_data)
    
    login_response = client.post(
        "/api/auth/login", 
        data={
            "username": "testuser",
            "password": "Password123"
        }
    )
    token = login_response.json()["access_token"]
    
    # Get current user with token
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/api/auth/me", headers=headers)
    
    # Check response
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["username"] == user_data["username"]
    assert data["email"] == user_data["email"]


def test_get_current_user_invalid_token(client):
    """Test getting current user with invalid token."""
    headers = {"Authorization": "Bearer invalidtoken"}
    response = client.get("/api/auth/me", headers=headers)
    
    # Check response
    assert response.status_code == status.HTTP_401_UNAUTHORIZED 