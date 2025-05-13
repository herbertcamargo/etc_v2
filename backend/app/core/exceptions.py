"""
Custom exception classes for the application.

This module defines custom exceptions used throughout the application
to handle various error scenarios and provide appropriate responses.
"""

from fastapi import HTTPException, status


class NotFoundError(HTTPException):
    """
    Exception raised when a requested resource is not found.
    """
    def __init__(self, detail: str = "Resource not found"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


class AuthenticationError(HTTPException):
    """
    Exception raised when authentication fails.
    """
    def __init__(self, detail: str = "Could not validate credentials"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"},
        )


class AuthorizationError(HTTPException):
    """
    Exception raised when a user doesn't have permission for an operation.
    """
    def __init__(self, detail: str = "Not enough permissions"):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail
        )


class BadRequestError(HTTPException):
    """
    Exception raised when request data is invalid.
    """
    def __init__(self, detail: str = "Invalid request"):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail
        )


class PaymentRequiredError(HTTPException):
    """
    Exception raised when a premium feature is accessed without subscription.
    """
    def __init__(self, detail: str = "Payment required for this feature"):
        super().__init__(
            status_code=status.HTTP_402_PAYMENT_REQUIRED,
            detail=detail
        ) 