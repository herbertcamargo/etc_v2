"""
Main API router for the application.

This module aggregates all API route modules and includes them
in the main API router with appropriate prefixes.

Requirements fulfilled:
- Central router for all API endpoints
- Route prefixing and organization
- API versioning
"""

from fastapi import APIRouter

from app.api.routes import auth, practice, videos

# Create main API router
api_router = APIRouter()

# Include route modules with appropriate prefixes
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(videos.router, prefix="/videos", tags=["Videos"])
api_router.include_router(practice.router, prefix="/practice", tags=["Practice"]) 