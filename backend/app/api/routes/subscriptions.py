"""
Subscription routes module.

This module contains the API endpoints for managing user subscriptions.
It handles subscription creation, updates, cancellation, and payment processing.
"""

from datetime import datetime, timedelta
from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user, get_db
from app.core.config import settings
from app.db.crud import subscriptions as crud
from app.schemas import subscriptions as schemas
from app.schemas.users import User
from app.services.payment import (
    create_checkout_session,
    create_customer,
    get_subscription_details,
    cancel_subscription
)

router = APIRouter(
    prefix="/subscriptions",
    tags=["subscriptions"],
)


@router.get("/plans", response_model=List[schemas.SubscriptionPlan])
async def get_subscription_plans():
    """
    Get available subscription plans.
    """
    # Return predefined subscription plans
    return [
        {
            "id": "price_monthly",
            "name": "Monthly Plan",
            "description": "Unlimited transcriptions with full features",
            "price": 4.99,
            "currency": "USD",
            "interval": "month",
            "features": [
                "Unlimited transcriptions",
                "Advanced analytics",
                "Priority support"
            ]
        },
        {
            "id": "price_yearly",
            "name": "Yearly Plan",
            "description": "20% discount for yearly commitment",
            "price": 47.88,
            "currency": "USD",
            "interval": "year",
            "features": [
                "Unlimited transcriptions",
                "Advanced analytics",
                "Priority support",
                "20% discount compared to monthly"
            ]
        }
    ]


@router.post("/checkout", response_model=schemas.CheckoutSession)
async def create_checkout(
    request: Request,
    checkout_data: schemas.CheckoutRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Create a Stripe checkout session for subscription payment.
    """
    # Make sure the user doesn't already have an active subscription
    active_subscription = crud.get_active_subscription(db, current_user.id)
    if active_subscription:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already has an active subscription"
        )
    
    # Create a customer in Stripe if not exists
    if not current_user.stripe_customer_id:
        customer_id = await create_customer(current_user.email, current_user.username)
        # Update the user with the Stripe customer ID
        crud.update_stripe_customer_id(db, current_user.id, customer_id)
    else:
        customer_id = current_user.stripe_customer_id
    
    # Create the checkout session
    success_url = f"{checkout_data.success_url}?session_id={{CHECKOUT_SESSION_ID}}"
    cancel_url = checkout_data.cancel_url
    
    checkout_session = await create_checkout_session(
        customer_id=customer_id,
        price_id=checkout_data.price_id,
        success_url=success_url,
        cancel_url=cancel_url
    )
    
    return {"checkout_url": checkout_session.url, "session_id": checkout_session.id}


@router.post("/webhook", status_code=status.HTTP_200_OK)
async def stripe_webhook(request: Request, db: Session = Depends(get_db)):
    """
    Handle Stripe webhook events for subscription lifecycle.
    """
    # Get the signature from the header
    signature = request.headers.get("stripe-signature")
    if not signature:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Missing Stripe signature"
        )
    
    # Get the event data
    try:
        payload = await request.body()
        event = stripe.Webhook.construct_event(
            payload, signature, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid payload"
        )
    except stripe.error.SignatureVerificationError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid signature"
        )
    
    # Handle relevant subscription events
    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        customer_id = session["customer"]
        subscription_id = session["subscription"]
        
        # Get the customer associated with this subscription
        user = crud.get_user_by_stripe_customer_id(db, customer_id)
        if not user:
            # This could be a webhook for a different environment or a test
            return {"success": True}
        
        # Get subscription details from Stripe
        subscription_details = await get_subscription_details(subscription_id)
        
        # Calculate subscription end date
        start_date = datetime.fromtimestamp(subscription_details.start_date)
        end_date = datetime.fromtimestamp(subscription_details.current_period_end)
        
        # Create a new subscription record
        subscription_data = schemas.SubscriptionCreate(
            user_id=user.id,
            stripe_subscription_id=subscription_id,
            status="active",
            plan_type=subscription_details.plan.interval,
            start_date=start_date,
            end_date=end_date
        )
        
        crud.create_subscription(db, subscription_data)
        
        # Update user premium status
        crud.update_user_premium_status(db, user.id, True, end_date)
    
    elif event["type"] == "customer.subscription.updated":
        subscription = event["data"]["object"]
        subscription_id = subscription["id"]
        status = subscription["status"]
        
        # Update subscription status
        db_subscription = crud.get_subscription_by_stripe_id(db, subscription_id)
        if db_subscription:
            # Update end date if renewed
            end_date = datetime.fromtimestamp(subscription["current_period_end"])
            crud.update_subscription_status(db, db_subscription.id, status, end_date)
            
            # Update user premium status if necessary
            if status == "active":
                crud.update_user_premium_status(db, db_subscription.user_id, True, end_date)
    
    elif event["type"] == "customer.subscription.deleted":
        subscription = event["data"]["object"]
        subscription_id = subscription["id"]
        
        # Mark subscription as canceled
        db_subscription = crud.get_subscription_by_stripe_id(db, subscription_id)
        if db_subscription:
            crud.update_subscription_status(db, db_subscription.id, "canceled")
            
            # Update user premium status
            crud.update_user_premium_status(db, db_subscription.user_id, False, None)
    
    return {"success": True}


@router.get("/me", response_model=schemas.Subscription)
async def get_current_subscription(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Get the current user's active subscription.
    """
    subscription = crud.get_active_subscription(db, current_user.id)
    if not subscription:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No active subscription found"
        )
    
    return subscription


@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
async def cancel_current_subscription(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Cancel the current user's subscription.
    """
    subscription = crud.get_active_subscription(db, current_user.id)
    if not subscription:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No active subscription found"
        )
    
    # Cancel the subscription in Stripe
    try:
        await cancel_subscription(subscription.stripe_subscription_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to cancel subscription: {str(e)}"
        )
    
    # Update subscription status in database
    crud.update_subscription_status(db, subscription.id, "canceled")
    
    # Update user premium status
    crud.update_user_premium_status(db, current_user.id, False, None)


@router.get("/usage", response_model=schemas.SubscriptionUsage)
async def get_subscription_usage(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Get the current user's subscription usage statistics.
    """
    # Check if user has premium status
    if not current_user.is_premium:
        # For free users, return usage against free tier limits
        free_transcriptions_used = crud.count_user_transcriptions(db, current_user.id)
        return {
            "plan_type": "free",
            "transcriptions_used": free_transcriptions_used,
            "transcriptions_limit": 3,
            "transcriptions_remaining": max(0, 3 - free_transcriptions_used),
            "is_limited": True,
            "renewal_date": None
        }
    else:
        # For premium users, return unlimited usage
        subscription = crud.get_active_subscription(db, current_user.id)
        return {
            "plan_type": subscription.plan_type if subscription else "unknown",
            "transcriptions_used": crud.count_user_transcriptions(db, current_user.id),
            "transcriptions_limit": float('inf'),
            "transcriptions_remaining": float('inf'),
            "is_limited": False,
            "renewal_date": subscription.end_date if subscription else None
        } 