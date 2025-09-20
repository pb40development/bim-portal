"""
Properties and Property Groups management mixin.
"""

from typing import List, Optional
from uuid import UUID
from .auth.auth_config import logger
from .models import (
    PropertyOrGroupForPublicDto, PropertyOrGroupForPublicRequest,
    PropertyDto, PropertyGroupDto, FilterGroupForPublicDto
)


class PropertiesMixin:
    """
    Mixin providing property and property group management methods.
    Requires BaseClient functionality to be available.
    """
    
    # === PROPERTY GROUPS (MERKMALSGRUPPEN) ===
    
    def search_property_groups(self, request: Optional[PropertyOrGroupForPublicRequest] = None) -> List[PropertyOrGroupForPublicDto]:
        """Search for property groups matching the given criteria."""
        request_data = request.model_dump(exclude_none=True) if request else {}
        
        try:
            response = self._make_authenticated_request(
                "POST", "/merkmale/api/v1/public/propertygroup", request_data
            )
            data = self._parse_response_json(response)
            groups = self._parse_model(data, PropertyOrGroupForPublicDto)
            return groups if groups else []
        except Exception as e:
            logger.error(f"Error searching property groups: {e}")
            return []
    
    def get_property_group(self, guid: UUID) -> Optional[PropertyGroupDto]:
        """Get detailed information about a specific property group."""
        try:
            response = self._make_authenticated_request("GET", f"/merkmale/api/v1/public/propertygroup/{guid}")
            data = self._parse_response_json(response)
            return self._parse_model(data, PropertyGroupDto)
        except Exception as e:
            logger.error(f"Error getting property group {guid}: {e}")
            return None
    
    # === PROPERTIES (MERKMALE) ===
    
    def search_properties(self, request: Optional[PropertyOrGroupForPublicRequest] = None) -> List[PropertyOrGroupForPublicDto]:
        """Search for properties matching the given criteria."""
        request_data = request.model_dump(exclude_none=True) if request else {"searchString": "a"}
        
        try:
            response = self._make_authenticated_request("POST", "/merkmale/api/v1/public/property", request_data)
            data = self._parse_response_json(response)
            properties = self._parse_model(data, PropertyOrGroupForPublicDto)
            return properties if properties else []
        except Exception as e:
            logger.error(f"Error searching properties: {e}")
            return []
    
    def get_property(self, guid: UUID) -> Optional[PropertyDto]:
        """Get detailed information about a specific property."""
        try:
            response = self._make_authenticated_request("GET", f"/merkmale/api/v1/public/property/{guid}")
            data = self._parse_response_json(response)
            return self._parse_model(data, PropertyDto)
        except Exception as e:
            logger.error(f"Error getting property {guid}: {e}")
            return None

    def get_merkmale_filters(self) -> List[FilterGroupForPublicDto]:
        """Get all global filters for properties."""
        try:
            response = self._make_authenticated_request("GET", "/merkmale/api/v1/public/filter")
            data = self._parse_response_json(response)
            filters = self._parse_model(data, FilterGroupForPublicDto)
            return filters if filters else []
        except Exception as e:
            logger.error(f"Error getting property filters: {e}")
            return []