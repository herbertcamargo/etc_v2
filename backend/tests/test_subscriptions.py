"""
Subscription API tests.

This module contains tests for the subscription API endpoints.
"""

import json
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock
import pytest
from fastapi import status
from uuid import uuid4

from app.db.crud import users as users_crud
from app.db.crud import subscriptions as subs_crud


@pytest.fixture
def user_token(client, db_session):
    """Create a test user and return authentication token."""
    # Register test user
    user_data = {
        "username": "subtest",
        "email": "subtest@example.com",
        "password": "Password123"
    }
    client.post("/api/auth/register", json=user_data)
    
    # Login and get token
    login_response = client.post(
        "/api/auth/login", 
        data={
            "username": "subtest",
            "password": "Password123"
        }
    )
    token = login_response.json()["access_token"]
    return token


@pytest.fixture
def auth_headers(user_token):
    """Create authentication headers with token."""
    return {"Authorization": f"Bearer {user_token}"}


def test_get_subscription_plans(client):
    """Test retrieving subscription plans."""
    response = client.get("/api/subscriptions/plans")
    
    # Check response
    assert response.status_code == status.HTTP_200_OK
    plans = response.json()
    
    # Verify plans structure
    assert len(plans) >= 2  # Should have at least monthly and yearly plans
    
    # Check plan fields
    for plan in plans:
        assert "id" in plan
        assert "name" in plan
        assert "price" in plan
        assert "interval" in plan
        assert "features" in plan


@patch("backend.app.services.payment.create_checkout_session")
def test_create_checkout_session(mock_create_checkout, client, db_session, auth_headers):
    """Test creating a checkout session."""
    # Mock Stripe response
    mock_session = MagicMock()
    mock_session.url = "https://checkout.stripe.com/test-session"
    mock_session.id = "cs_test_123456"
    mock_create_checkout.return_value = mock_session
    
    # Prepare checkout data
    checkout_data = {
        "price_id": "price_monthly",
        "success_url": "https://example.com/success",
        "cancel_url": "https://example.com/cancel"
    }
    
    # Create checkout session
    response = client.post(
        "/api/subscriptions/checkout", 
        json=checkout_data, 
        headers=auth_headers
    )
    
    # Check response
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["checkout_url"] == "https://checkout.stripe.com/test-session"
    assert data["session_id"] == "cs_test_123456"
    
    # Verify the payment service was called correctly
    mock_create_checkout.assert_called_once()


def test_create_checkout_already_subscribed(client, db_session, auth_headers):
    """Test creating checkout when user already has an active subscription."""
    # Get the user
    user = users_crud.get_user_by_username(db_session, "subtest")
    
    # Create an active subscription for the user
    subscription_data = {
        "user_id": user.id,
        "stripe_subscription_id": "sub_test_123",
        "status": "active",
        "plan_type": "month",
        "start_date": datetime.utcnow(),
        "end_date": datetime.utcnow() + timedelta(days=30)
    }
    subs_crud.create_subscription(db_session, subscription_data)
    
    # Try to create a checkout session
    checkout_data = {
        "price_id": "price_monthly",
        "success_url": "https://example.com/success",
        "cancel_url": "https://example.com/cancel"
    }
    
    response = client.post(
        "/api/subscriptions/checkout", 
        json=checkout_data, 
        headers=auth_headers
    )
    
    # Should get an error response
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    data = response.json()
    assert "active subscription" in data["detail"]


def test_get_subscription_usage_free_user(client, db_session, auth_headers):
    """Test getting subscription usage for a free user."""
    response = client.get("/api/subscriptions/usage", headers=auth_headers)
    
    # Check response
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    
    # Verify free user data
    assert data["plan_type"] == "free"
    assert data["is_limited"] == True
    assert data["transcriptions_limit"] == 3
    assert data["transcriptions_used"] == 0
    assert data["transcriptions_remaining"] == 3
    assert data["renewal_date"] is None


def test_get_subscription_usage_premium_user(client, db_session, auth_headers):
    """Test getting subscription usage for a premium user."""
    # Get the user
    user = users_crud.get_user_by_username(db_session, "subtest")
    
    # Set user as premium
    users_crud.update_user_premium_status(
        db_session, 
        user.id, 
        True, 
        datetime.utcnow() + timedelta(days=30)
    )
    
    # Create an active subscription
    subscription_data = {
        "user_id": user.id,
        "stripe_subscription_id": "sub_test_456",
        "status": "active",
        "plan_type": "month",
        "start_date": datetime.utcnow(),
        "end_date": datetime.utcnow() + timedelta(days=30)
    }
    subs_crud.create_subscription(db_session, subscription_data)
    
    # Get subscription usage
    response = client.get("/api/subscriptions/usage", headers=auth_headers)
    
    # Check response
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    
    # Verify premium user data
    assert data["plan_type"] == "month"
    assert data["is_limited"] == False
    assert isinstance(data["transcriptions_used"], int)
    assert data["renewal_date"] is not None


@patch("backend.app.services.payment.cancel_subscription")
def test_cancel_subscription(mock_cancel, client, db_session, auth_headers):
    """Test cancelling a subscription."""
    # Mock Stripe response
    mock_cancel.return_value = MagicMock()
    
    # Get the user
    user = users_crud.get_user_by_username(db_session, "subtest")
    
    # Create an active subscription
    subscription_data = {
        "user_id": user.id,
        "stripe_subscription_id": "sub_test_789",
        "status": "active",
        "plan_type": "month",
        "start_date": datetime.utcnow(),
        "end_date": datetime.utcnow() + timedelta(days=30)
    }
    subscription = subs_crud.create_subscription(db_session, subscription_data)
    
    # Cancel the subscription
    response = client.delete("/api/subscriptions/me", headers=auth_headers)
    
    # Check response
    assert response.status_code == status.HTTP_204_NO_CONTENT
    
    # Verify subscription was cancelled in the database
    updated_subscription = subs_crud.get_subscription(db_session, subscription.id)
    assert updated_subscription.status == "canceled"
    
    # Verify user premium status was updated
    updated_user = users_crud.get_user_by_username(db_session, "subtest")
    assert updated_user.is_premium == False
    assert updated_user.subscription_end_date is None


def test_cancel_subscription_no_active(client, db_session, auth_headers):
    """Test cancelling a subscription when user has no active subscription."""
    response = client.delete("/api/subscriptions/me", headers=auth_headers)
    
    # Should get an error response
    assert response.status_code == status.HTTP_404_NOT_FOUND
    data = response.json()
    assert "No active subscription" in data["detail"]


def test_get_current_subscription(client, db_session, auth_headers):
    """Test getting the current subscription."""
    # Get the user
    user = users_crud.get_user_by_username(db_session, "subtest")
    
    # Create an active subscription
    subscription_data = {
        "user_id": user.id,
        "stripe_subscription_id": "sub_test_999",
        "status": "active",
        "plan_type": "month",
        "start_date": datetime.utcnow(),
        "end_date": datetime.utcnow() + timedelta(days=30)
    }
    subs_crud.create_subscription(db_session, subscription_data)
    
    # Get current subscription
    response = client.get("/api/subscriptions/me", headers=auth_headers)
    
    # Check response
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    
    # Verify subscription data
    assert data["stripe_subscription_id"] == "sub_test_999"
    assert data["status"] == "active"
    assert data["plan_type"] == "month"


def test_get_current_subscription_none(client, db_session, auth_headers):
    """Test getting current subscription when user has none."""
    # Get the user and ensure no subscription
    user = users_crud.get_user_by_username(db_session, "subtest")
    
    # Delete any subscriptions the user might have
    db_session.query(subs_crud.Subscription).filter(
        subs_crud.Subscription.user_id == user.id
    ).delete()
    db_session.commit()
    
    # Get current subscription
    response = client.get("/api/subscriptions/me", headers=auth_headers)
    
    # Should get an error response
    assert response.status_code == status.HTTP_404_NOT_FOUND
    data = response.json()
    assert "No active subscription" in data["detail"] 