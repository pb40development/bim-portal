"""
Base HTTP client functionality for BIM Portal API.
"""

import json
from typing import Dict, Any, Optional
from http import HTTPStatus

import httpx
from pydantic import ValidationError

from .auth.auth_service_impl import AuthService, AuthenticationError
from .auth.auth_config import AUTH_RETRY_LIMIT, logger
from .config import BIMPortalConfig


class BaseClient:
    """
    Base HTTP client with authentication and common functionality.
    No GUID required for authentication.
    """

    def __init__(self, auth_service: Optional[AuthService] = None, base_url: str = BIMPortalConfig.BASE_URL,
                 raise_on_unexpected_status: bool = False, username: Optional[str] = None,
                 password: Optional[str] = None):
        """
        Initialize the base client.

        Args:
            auth_service: Pre-configured AuthService instance (optional)
            base_url: API base URL
            raise_on_unexpected_status: Whether to raise exceptions on HTTP errors
            username: Username for authentication (if auth_service not provided)
            password: Password for authentication (if auth_service not provided)
        """
        if auth_service:
            self.auth_service = auth_service
        else:
            # Create auth service without GUID requirement
            self.auth_service = AuthService(username=username, password=password)

        self.base_url = base_url
        self.raise_on_unexpected_status = raise_on_unexpected_status
        
        self._httpx_client = httpx.Client(
            base_url=base_url,
            timeout=30.0,
            verify=True,
        )
    
    def _get_auth_headers(self) -> Dict[str, str]:
        """Get authentication headers if token is available."""
        headers = {
            "accept": "application/json",
            "Content-Type": "application/json"
        }
        
        try:
            token = self.auth_service.get_valid_token()
            if token:
                headers["Authorization"] = f"Bearer {token}"
        except AuthenticationError as e:
            logger.warning(f"Authentication failed: {e}. Proceeding with public access.")
        
        return headers
    
    def _make_authenticated_request(self, method: str, endpoint: str, 
                                   json_data: Optional[Dict] = None) -> httpx.Response:
        """Make an authenticated HTTP request with retry logic."""
        for attempt in range(AUTH_RETRY_LIMIT + 1):
            headers = self._get_auth_headers()
            
            try:
                response = self._httpx_client.request(
                    method=method.upper(), 
                    url=endpoint, 
                    headers=headers, 
                    json=json_data
                )
                
                if response.status_code in (HTTPStatus.UNAUTHORIZED, HTTPStatus.FORBIDDEN):
                    if attempt >= AUTH_RETRY_LIMIT:
                        if self.raise_on_unexpected_status:
                            response.raise_for_status()
                        return response
                    
                    self.auth_service._token_manager.clear_tokens()
                    continue
                
                if self.raise_on_unexpected_status and response.status_code >= 400:
                    response.raise_for_status()
                
                return response
                
            except httpx.HTTPError as e:
                if attempt >= AUTH_RETRY_LIMIT:
                    raise e
        
        raise RuntimeError("Exited retry loop unexpectedly.")
    
    def _parse_response_json(self, response: httpx.Response) -> Optional[Dict[str, Any]]:
        """Parse response JSON with error handling."""
        try:
            if response.status_code == 200:
                return response.json()
            return None
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON response: {e}")
            return None
    
    def _parse_model(self, data: Any, model_class) -> Optional[Any]:
        """Parse data into a Pydantic model with error handling."""
        if data is None:
            return None
            
        try:
            if isinstance(data, list):
                return [model_class.model_validate(item) for item in data if item is not None]
            else:
                return model_class.model_validate(data)
        except ValidationError as e:
            logger.warning(f"Failed to parse {model_class.__name__}: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error parsing {model_class.__name__}: {e}")
            return None
    
    # === COMPATIBILITY METHODS ===
    
    def get_httpx_client(self):
        """Return self to maintain compatibility with existing code."""
        return self
    
    def get(self, endpoint: str, **kwargs) -> httpx.Response:
        """GET request with authentication."""
        return self._make_authenticated_request("GET", endpoint)
    
    def post(self, endpoint: str, json: Optional[Dict] = None, **kwargs) -> httpx.Response:
        """POST request with authentication."""
        return self._make_authenticated_request("POST", endpoint, json)
    
    def request(self, method: str, endpoint: str, **kwargs) -> httpx.Response:
        """Generic request method."""
        json_data = kwargs.get('json')
        return self._make_authenticated_request(method, endpoint, json_data)
    
    # === CONTEXT MANAGER SUPPORT ===
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self._httpx_client.close()