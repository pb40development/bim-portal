"""
Authentication and organization management mixin.
"""

from typing import List, Optional
from auth.auth_config import logger
from models import (
    OrganisationForPublicDTO, UserLoginPublicDto, 
    JWTTokenPublicDto, RefreshTokenRequestDTO
)


class AuthMixin:
    """
    Mixin providing authentication and organization management methods.
    Requires BaseClient functionality to be available.
    """
    
    def login(self, credentials: UserLoginPublicDto) -> Optional[JWTTokenPublicDto]:
        """Login to the system."""
        try:
            response = self._make_authenticated_request(
                "POST", "/infrastruktur/api/v1/public/auth/login", 
                credentials.model_dump()
            )
            data = self._parse_response_json(response)
            return self._parse_model(data, JWTTokenPublicDto)
        except Exception as e:
            logger.error(f"Error during login: {e}")
            return None
    
    def refresh_token(self, refresh_request: RefreshTokenRequestDTO) -> Optional[JWTTokenPublicDto]:
        """Refresh the authorization token."""
        try:
            response = self._make_authenticated_request(
                "POST", "/infrastruktur/api/v1/public/auth/refresh", 
                refresh_request.model_dump()
            )
            data = self._parse_response_json(response)
            return self._parse_model(data, JWTTokenPublicDto)
        except Exception as e:
            logger.error(f"Error refreshing token: {e}")
            return None
    
    def logout(self) -> bool:
        """Logout from the system."""
        try:
            response = self._make_authenticated_request("POST", "/infrastruktur/api/v1/public/auth/logout")
            return response.status_code == 200
        except Exception as e:
            logger.error(f"Error during logout: {e}")
            return False
    
    def get_organisations(self) -> List[OrganisationForPublicDTO]:
        """Get list of all organizations available via the REST API."""
        try:
            response = self._make_authenticated_request("GET", "/infrastruktur/api/v1/public/organisation")
            data = self._parse_response_json(response)
            organisations = self._parse_model(data, OrganisationForPublicDTO)
            return organisations if organisations else []
        except Exception as e:
            logger.error(f"Error getting organisations: {e}")
            return []
    
    def get_my_organisations(self) -> List[OrganisationForPublicDTO]:
        """Get list of organizations where the user is a member."""
        try:
            response = self._make_authenticated_request("GET", "/infrastruktur/api/v1/public/organisation/my")
            data = self._parse_response_json(response)
            organisations = self._parse_model(data, OrganisationForPublicDTO)
            return organisations if organisations else []
        except Exception as e:
            logger.error(f"Error getting user organisations: {e}")
            return []