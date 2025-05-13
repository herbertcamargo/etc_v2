"""
Routes initialization module.

This module initializes all API route modules and combines them into a single router.
"""

from fastapi import APIRouter

from app.api.routes import auth, videos, transcriptions, subscriptions

# Create the main API router
api_router = APIRouter()

# Include individual route modules
api_router.include_router(auth.router)
api_router.include_router(videos.router)
api_router.include_router(transcriptions.router)
api_router.include_router(subscriptions.router) 