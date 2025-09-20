"""
Custom exception classes for the BIM Portal API client.

These exceptions provide specific error handling for different failure scenarios,
making it easier to handle errors appropriately in client code.
"""

from typing import Optional
import requests


class BIMPortalError(Exception):
    """Base exception for all BIM Portal API errors."""

    def __init__(self, message: str, status_code: Optional[int] = None, response_text: Optional[str] = None):
        """
        Initialize the base BIM Portal error.

        Args:
            message: Human-readable error message
            status_code: HTTP status code if applicable
            response_text: Raw response text if available
        """
        super().__init__(message)
        self.status_code = status_code
        self.response_text = response_text

    def __str__(self):
        if self.status_code:
            return f"{super().__str__()} (HTTP {self.status_code})"
        return super().__str__()


class AuthenticationError(BIMPortalError):
    """
    Exception raised when authentication fails.

    This includes login failures, token refresh failures, and invalid credentials.
    """

    def __init__(self, message: str = "Authentication failed",
                 status_code: Optional[int] = None,
                 response_text: Optional[str] = None,
                 username: Optional[str] = None):
        """
        Initialize authentication error.

        Args:
            message: Error message
            status_code: HTTP status code
            response_text: Raw response from server
            username: Username that failed authentication (for logging)
        """
        super().__init__(message, status_code, response_text)
        self.username = username


class TokenExpiredError(AuthenticationError):
    """Exception raised when token has expired and refresh failed."""

    def __init__(self, message: str = "Token expired and refresh failed"):
        super().__init__(message)


class InvalidCredentialsError(AuthenticationError):
    """Exception raised when credentials are invalid."""

    def __init__(self, message: str = "Invalid username or password",
                 username: Optional[str] = None):
        super().__init__(message, username=username)


class NetworkError(BIMPortalError):
    """Exception raised when network/connection issues occur."""

    def __init__(self, message: str = "Network error occurred",
                 original_exception: Optional[Exception] = None):
        super().__init__(message)
        self.original_exception = original_exception


class APIError(BIMPortalError):
    """Exception raised when the API returns an error response."""

    def __init__(self, message: str, status_code: int,
                 response_text: Optional[str] = None,
                 endpoint: Optional[str] = None):
        super().__init__(message, status_code, response_text)
        self.endpoint = endpoint


class ConfigurationError(BIMPortalError):
    """Exception raised when configuration is invalid or missing."""

    def __init__(self, message: str = "Configuration error"):
        super().__init__(message)


class ValidationError(BIMPortalError):
    """Exception raised when request data validation fails."""

    def __init__(self, message: str = "Request validation failed",
                 field: Optional[str] = None):
        super().__init__(message)
        self.field = field


# Utility functions for exception handling

def handle_requests_exception(e: requests.RequestException, context: str = "API request") -> BIMPortalError:
    """
    Convert requests exceptions to appropriate BIM Portal exceptions.

    Args:
        e: The original requests exception
        context: Context where the error occurred

    Returns:
        Appropriate BIMPortalError subclass
    """
    if isinstance(e, requests.ConnectionError):
        return NetworkError(f"Connection failed during {context}", e)
    elif isinstance(e, requests.Timeout):
        return NetworkError(f"Request timeout during {context}", e)
    elif isinstance(e, requests.HTTPError):
        response = e.response
        if response is not None:
            if response.status_code in (401, 403):
                return AuthenticationError(
                    f"Authentication failed during {context}",
                    response.status_code,
                    response.text
                )
            else:
                return APIError(
                    f"HTTP error during {context}",
                    response.status_code,
                    response.text
                )

    return NetworkError(f"Unexpected error during {context}: {str(e)}", e)


def create_auth_error_from_response(response: requests.Response, username: Optional[str] = None) -> AuthenticationError:
    """
    Create appropriate authentication error from HTTP response.

    Args:
        response: HTTP response object
        username: Username that failed authentication

    Returns:
        Specific authentication error
    """
    if response.status_code == 401:
        return InvalidCredentialsError(
            "Invalid username or password",
            username=username
        )
    elif response.status_code == 403:
        return AuthenticationError(
            "Access forbidden - check permissions",
            status_code=403,
            response_text=response.text,
            username=username
        )
    else:
        return AuthenticationError(
            f"Authentication failed with status {response.status_code}",
            status_code=response.status_code,
            response_text=response.text,
            username=username
        )