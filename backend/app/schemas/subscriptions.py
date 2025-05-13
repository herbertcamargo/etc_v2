"""
Subscription schemas module.

This module contains Pydantic models for subscription data validation.
"""

from datetime import datetime
from typing import List, Optional, Union
from uuid import UUID

from pydantic import BaseModel, Field, HttpUrl


class SubscriptionBase(BaseModel):
    """
    Base schema for subscription data.
    """
    user_id: UUID
    stripe_subscription_id: str
    status: str  # active, canceled, past_due
    plan_type: str  # month, year
    start_date: datetime
    end_date: datetime


class SubscriptionCreate(SubscriptionBase):
    """
    Schema for creating a new subscription.
    """
    pass


class Subscription(SubscriptionBase):
    """
    Schema for a complete subscription.
    """
    id: UUID
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True


class SubscriptionPlan(BaseModel):
    """
    Schema for a subscription plan.
    """
    id: str
    name: str
    description: str
    price: float
    currency: str = "USD"
    interval: str  # month, year
    features: List[str]


class CheckoutRequest(BaseModel):
    """
    Schema for creating a checkout session.
    """
    price_id: str
    success_url: HttpUrl
    cancel_url: HttpUrl


class CheckoutSession(BaseModel):
    """
    Schema for the created checkout session.
    """
    checkout_url: HttpUrl
    session_id: str


class SubscriptionUsage(BaseModel):
    """
    Schema for subscription usage statistics.
    """
    plan_type: str  # free, month, year
    transcriptions_used: int
    transcriptions_limit: Union[int, float]  # float('inf') for unlimited
    transcriptions_remaining: Union[int, float]
    is_limited: bool
    renewal_date: Optional[datetime] 