"""
Main application module.

This is the entry point for the FastAPI application.
It sets up the API routes, middleware, and other application settings.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response

from app.api.routes import auth
from app.core.config import settings
from app.core.metrics import get_metrics
from app.core.middleware import PrometheusMiddleware

# Create FastAPI application
app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)

# Configure CORS
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Add Prometheus middleware
app.add_middleware(PrometheusMiddleware)

# Include API routes
app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["auth"])

@app.get("/")
async def root():
    """
    Root endpoint to verify the API is running.
    """
    return {"message": "Welcome to TranscriptV2 API"}

@app.get("/health")
async def health_check():
    """
    Health check endpoint for monitoring.
    """
    return {"status": "healthy"}

@app.get(f"{settings.API_V1_STR}/metrics")
async def metrics():
    """
    Expose metrics for Prometheus scraping.
    
    Returns:
        Response: Prometheus metrics in text format
    """
    return Response(
        content=get_metrics(),
        media_type="text/plain"
    ) 