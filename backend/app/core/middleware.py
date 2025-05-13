"""
Middleware module for the application.

This module provides middleware components for the FastAPI application.
"""

import time
from typing import Callable

from fastapi import FastAPI, Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.metrics import http_requests_total, http_request_duration_seconds


class PrometheusMiddleware(BaseHTTPMiddleware):
    """
    Middleware for collecting Prometheus metrics.
    
    Tracks HTTP request counts and duration.
    """
    def __init__(self, app: FastAPI):
        super().__init__(app)
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Start timer for request duration
        start_time = time.time()
        
        # Get request method and path
        method = request.method
        path = request.url.path
        
        # Handle request
        try:
            response = await call_next(request)
            status = response.status_code
            
            # Skip metrics endpoint itself to avoid recursion
            if path != "/api/metrics":
                # Record metrics
                http_requests_total.labels(
                    method=method,
                    endpoint=path,
                    status=status
                ).inc()
                
                http_request_duration_seconds.labels(
                    method=method,
                    endpoint=path
                ).observe(time.time() - start_time)
            
            return response
        except Exception as e:
            # Record error metrics
            status = 500
            http_requests_total.labels(
                method=method,
                endpoint=path,
                status=status
            ).inc()
            
            # Re-raise the exception
            raise e 