"""
CRUD operations for subscriptions.

This module provides functions for creating, reading, updating, and deleting
subscription records in the database.
"""

from datetime import datetime
from typing import List, Optional
from uuid import UUID

from sqlalchemy import desc, func
from sqlalchemy.orm import Session

from app.db.models import Subscription, User, TranscriptionSession
from app.schemas import subscriptions as schemas


def get_subscription(db: Session, subscription_id: UUID) -> Optional[Subscription]:
    """
    Get a subscription by ID.
    
    Args:
        db: Database session
        subscription_id: UUID of the subscription
        
    Returns:
        Subscription if found, None otherwise
    """
    return db.query(Subscription).filter(Subscription.id == subscription_id).first()


def get_subscription_by_stripe_id(db: Session, stripe_subscription_id: str) -> Optional[Subscription]:
    """
    Get a subscription by Stripe subscription ID.
    
    Args:
        db: Database session
        stripe_subscription_id: Stripe subscription ID
        
    Returns:
        Subscription if found, None otherwise
    """
    return db.query(Subscription).filter(Subscription.stripe_subscription_id == stripe_subscription_id).first()


def get_active_subscription(db: Session, user_id: UUID) -> Optional[Subscription]:
    """
    Get the active subscription for a user.
    
    Args:
        db: Database session
        user_id: UUID of the user
        
    Returns:
        Subscription if found, None otherwise
    """
    return (
        db.query(Subscription)
        .filter(
            Subscription.user_id == user_id,
            Subscription.status == "active",
            Subscription.end_date > datetime.utcnow()
        )
        .order_by(desc(Subscription.end_date))
        .first()
    )


def get_user_subscriptions(
    db: Session, user_id: UUID, skip: int = 0, limit: int = 100
) -> List[Subscription]:
    """
    Get all subscriptions for a specific user.
    
    Args:
        db: Database session
        user_id: UUID of the user
        skip: Number of records to skip (for pagination)
        limit: Maximum number of records to return
        
    Returns:
        List of Subscription objects
    """
    return (
        db.query(Subscription)
        .filter(Subscription.user_id == user_id)
        .order_by(desc(Subscription.created_at))
        .offset(skip)
        .limit(limit)
        .all()
    )


def create_subscription(
    db: Session, subscription: schemas.SubscriptionCreate
) -> Subscription:
    """
    Create a new subscription.
    
    Args:
        db: Database session
        subscription: SubscriptionCreate schema with subscription data
        
    Returns:
        The created Subscription object
    """
    db_subscription = Subscription(
        user_id=subscription.user_id,
        stripe_subscription_id=subscription.stripe_subscription_id,
        status=subscription.status,
        plan_type=subscription.plan_type,
        start_date=subscription.start_date,
        end_date=subscription.end_date
    )
    
    db.add(db_subscription)
    db.commit()
    db.refresh(db_subscription)
    
    return db_subscription


def update_subscription_status(
    db: Session, subscription_id: UUID, status: str, end_date: Optional[datetime] = None
) -> Optional[Subscription]:
    """
    Update a subscription's status and optionally end date.
    
    Args:
        db: Database session
        subscription_id: UUID of the subscription to update
        status: New status (active, canceled, past_due)
        end_date: Optional new end date
        
    Returns:
        The updated Subscription object or None if not found
    """
    db_subscription = get_subscription(db=db, subscription_id=subscription_id)
    if not db_subscription:
        return None
    
    db_subscription.status = status
    
    if end_date:
        db_subscription.end_date = end_date
    
    db_subscription.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(db_subscription)
    
    return db_subscription


def update_stripe_customer_id(db: Session, user_id: UUID, stripe_customer_id: str) -> Optional[User]:
    """
    Update a user's Stripe customer ID.
    
    Args:
        db: Database session
        user_id: UUID of the user
        stripe_customer_id: Stripe customer ID
        
    Returns:
        The updated User object or None if not found
    """
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        return None
    
    db_user.stripe_customer_id = stripe_customer_id
    db_user.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(db_user)
    
    return db_user


def update_user_premium_status(
    db: Session, user_id: UUID, is_premium: bool, subscription_end_date: Optional[datetime]
) -> Optional[User]:
    """
    Update a user's premium status and subscription end date.
    
    Args:
        db: Database session
        user_id: UUID of the user
        is_premium: Whether the user has premium status
        subscription_end_date: End date of the subscription (or None)
        
    Returns:
        The updated User object or None if not found
    """
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        return None
    
    db_user.is_premium = is_premium
    db_user.subscription_end_date = subscription_end_date
    db_user.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(db_user)
    
    return db_user


def get_user_by_stripe_customer_id(db: Session, stripe_customer_id: str) -> Optional[User]:
    """
    Get a user by their Stripe customer ID.
    
    Args:
        db: Database session
        stripe_customer_id: Stripe customer ID
        
    Returns:
        User if found, None otherwise
    """
    return db.query(User).filter(User.stripe_customer_id == stripe_customer_id).first()


def count_user_transcriptions(db: Session, user_id: UUID) -> int:
    """
    Count the number of transcriptions created by a user.
    
    Args:
        db: Database session
        user_id: UUID of the user
        
    Returns:
        Number of transcriptions
    """
    return db.query(func.count(TranscriptionSession.id)).filter(
        TranscriptionSession.user_id == user_id
    ).scalar() or 0 