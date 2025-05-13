"""
Payment service module.

This module provides functionality for payment processing using Stripe API.
It handles subscriptions, payment checkouts, and customer management.
"""

import stripe
from typing import Any, Dict, Optional

from app.core.config import settings

# Initialize Stripe with API key
stripe.api_key = settings.STRIPE_SECRET_KEY


async def create_customer(email: str, name: Optional[str] = None) -> str:
    """
    Create a new customer in Stripe.
    
    Args:
        email: Customer's email address
        name: Customer's name (optional)
        
    Returns:
        Stripe customer ID
    """
    customer = stripe.Customer.create(
        email=email,
        name=name or email.split('@')[0],  # Use email username if name not provided
        metadata={
            "source": "videotranscribe_app"
        }
    )
    
    return customer.id


async def create_checkout_session(
    customer_id: str,
    price_id: str,
    success_url: str,
    cancel_url: str
) -> Any:
    """
    Create a Stripe checkout session for subscription payment.
    
    Args:
        customer_id: Stripe customer ID
        price_id: Stripe price ID
        success_url: URL to redirect after successful payment
        cancel_url: URL to redirect after canceled payment
        
    Returns:
        Stripe checkout session
    """
    # Get the actual price ID based on our internal price_id
    if price_id == "price_monthly":
        actual_price_id = settings.STRIPE_MONTHLY_PRICE_ID
    elif price_id == "price_yearly":
        actual_price_id = settings.STRIPE_YEARLY_PRICE_ID
    else:
        actual_price_id = price_id
        
    session = stripe.checkout.Session.create(
        customer=customer_id,
        payment_method_types=["card"],
        line_items=[
            {
                "price": actual_price_id,
                "quantity": 1,
            },
        ],
        mode="subscription",
        success_url=success_url,
        cancel_url=cancel_url,
        metadata={
            "source": "videotranscribe_app"
        }
    )
    
    return session


async def get_subscription_details(subscription_id: str) -> Any:
    """
    Get details of a Stripe subscription.
    
    Args:
        subscription_id: Stripe subscription ID
        
    Returns:
        Subscription details
    """
    return stripe.Subscription.retrieve(subscription_id)


async def cancel_subscription(subscription_id: str) -> Any:
    """
    Cancel a Stripe subscription.
    
    Args:
        subscription_id: Stripe subscription ID
        
    Returns:
        Canceled subscription
    """
    return stripe.Subscription.delete(subscription_id)


async def get_subscription_invoices(subscription_id: str, limit: int = 10) -> Any:
    """
    Get invoices for a specific subscription.
    
    Args:
        subscription_id: Stripe subscription ID
        limit: Maximum number of invoices to return
        
    Returns:
        List of invoices
    """
    return stripe.Invoice.list(
        subscription=subscription_id,
        limit=limit
    )


async def create_billing_portal_session(customer_id: str, return_url: str) -> Any:
    """
    Create a billing portal session for a customer.
    
    Args:
        customer_id: Stripe customer ID
        return_url: URL to return to after the session
        
    Returns:
        Billing portal session
    """
    return stripe.billing_portal.Session.create(
        customer=customer_id,
        return_url=return_url
    ) 