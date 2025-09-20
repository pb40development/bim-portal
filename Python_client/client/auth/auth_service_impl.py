import os
import requests
import threading
from typing import Optional

from .auth_config import (
    LOGIN_URL,
    REFRESH_URL,
    BIM_PORTAL_USERNAME_ENV_VAR,
    BIM_PORTAL_PASSWORD_ENV_VAR,
    logger,
)
from .token_manager import TokenManager
from .exceptions import (
    AuthenticationError,
    InvalidCredentialsError,
    TokenExpiredError,
    NetworkError,
    handle_requests_exception,
    create_auth_error_from_response
)
# Import from your new Pydantic models
from client.models import (
    UserLoginPublicDto,
    RefreshTokenRequestDTO,
    JWTTokenPublicDto,
)


class AuthService:
    """
    Handles the authentication process, including login and token refreshing.
    Uses improved exception handling for better error management.
    """

    def __init__(self, username: Optional[str] = None, password: Optional[str] = None):
        """
        Initializes the AuthService.

        Args:
            username (str, optional): The user's email. Defaults to env var.
            password (str, optional): The user's password. Defaults to env var.
        """
        self.username = username or os.getenv(BIM_PORTAL_USERNAME_ENV_VAR)
        self.password = password or os.getenv(BIM_PORTAL_PASSWORD_ENV_VAR)

        self._token_manager = TokenManager()
        self._lock = threading.Lock()

    def get_valid_token(self) -> Optional[str]:
        """
        Ensures a valid token is available and returns it.
        It handles token expiration by refreshing or re-logging in.
        Returns None if authentication is not configured or fails.

        Raises:
            AuthenticationError: If authentication fails with valid credentials
            InvalidCredentialsError: If credentials are invalid
            TokenExpiredError: If token expired and refresh failed
            NetworkError: If network issues prevent authentication
        """
        with self._lock:
            if not self.username or not self.password:
                logger.debug("No credentials provided; cannot get token. Proceeding with public access.")
                return None

            if not self._token_manager.is_token_expiring():
                return self._token_manager.get_access_token()

            logger.info("Token is missing or expiring. Attempting to refresh.")
            try:
                if self._refresh_token():
                    return self._token_manager.get_access_token()
            except TokenExpiredError:
                logger.info("Token refresh failed. Attempting fresh login.")
            except NetworkError as e:
                logger.error(f"Network error during token refresh: {e}")
                raise

            logger.info("Attempting to log in with fresh credentials.")
            if self._login():
                return self._token_manager.get_access_token()

            # If we reach here, both refresh and login failed
            raise AuthenticationError(
                "Failed to authenticate. Please check credentials and network connection.",
                username=self.username
            )

    def _login(self) -> bool:
        """
        Performs a login to get new access and refresh tokens.

        Returns:
            bool: True if login successful, False otherwise

        Raises:
            InvalidCredentialsError: If credentials are invalid
            NetworkError: If network issues occur
            AuthenticationError: For other authentication failures
        """
        logger.debug(f"Attempting login for user '{self.username}'")
        headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
        }
        login_data = UserLoginPublicDto(mail=self.username, password=self.password)

        try:
            response = requests.post(
                LOGIN_URL,
                headers=headers,
                json=login_data.model_dump(),
                timeout=30
            )

            if response.status_code == 200:
                try:
                    token_dto = JWTTokenPublicDto.model_validate(response.json())
                    self._token_manager.set_token(token_dto)
                    logger.info("Login successful. Token received.")
                    return True
                except Exception as e:
                    logger.error(f"Failed to parse login response: {e}")
                    raise AuthenticationError(f"Invalid response format from server: {e}")
            else:
                # Create specific error based on status code
                auth_error = create_auth_error_from_response(response, self.username)
                logger.error(f"Login failed: {auth_error}")
                self._token_manager.clear_tokens()
                raise auth_error

        except requests.RequestException as e:
            logger.error(f"Network error during login: {e}")
            self._token_manager.clear_tokens()
            network_error = handle_requests_exception(e, "login")
            raise network_error

    def _refresh_token(self) -> bool:
        """
        Refreshes the access token using the stored refresh token.

        Returns:
            bool: True if refresh successful, False otherwise

        Raises:
            TokenExpiredError: If refresh token is invalid/expired
            NetworkError: If network issues occur
        """
        refresh_token = self._token_manager.get_refresh_token()
        if not refresh_token:
            logger.debug("No refresh token available. Cannot refresh.")
            raise TokenExpiredError("No refresh token available")

        logger.debug("Attempting to refresh token.")
        headers = {"accept": "application/json", "Content-Type": "application/json"}
        refresh_data = RefreshTokenRequestDTO(refreshToken=refresh_token)

        try:
            response = requests.post(
                REFRESH_URL,
                headers=headers,
                json=refresh_data.model_dump(),
                timeout=30
            )

            if response.status_code == 200:
                try:
                    token_dto = JWTTokenPublicDto.model_validate(response.json())
                    self._token_manager.set_token(token_dto)
                    logger.info("Token refreshed successfully.")
                    return True
                except Exception as e:
                    logger.error(f"Failed to parse refresh response: {e}")
                    raise TokenExpiredError(f"Invalid refresh response format: {e}")
            else:
                logger.warning(f"Refresh token failed with status {response.status_code}: {response.text}")
                self._token_manager.clear_tokens()

                if response.status_code in (401, 403):
                    raise TokenExpiredError("Refresh token expired or invalid")
                else:
                    raise AuthenticationError(
                        f"Token refresh failed with status {response.status_code}",
                        status_code=response.status_code,
                        response_text=response.text
                    )

        except requests.RequestException as e:
            logger.error(f"Network error during token refresh: {e}")
            network_error = handle_requests_exception(e, "token refresh")
            raise network_error