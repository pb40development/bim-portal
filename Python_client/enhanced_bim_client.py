"""
Enhanced BIM Portal HTTP Client using mixins for better organization.
"""

from auth.auth_service_impl import AuthService
from config import BIMPortalConfig
from base_client import BaseClient
from auth_mixin import AuthMixin
from properties_mixin import PropertiesMixin
from aia_mixin import AiaMixin


class EnhancedBimPortalClient(BaseClient, AuthMixin, PropertiesMixin, AiaMixin):
    """
    Comprehensive HTTP client for BIM Portal API covering all documented endpoints.

    This class combines functionality from multiple mixins:
    - BaseClient: Core HTTP functionality and authentication
    - AuthMixin: Login, logout, organizations
    - PropertiesMixin: Properties and property groups
    - AiaMixin: LOINs, projects, templates, domain models, context info

    Usage:
        client = EnhancedBimPortalClient(auth_service)

        # All methods are available directly on the client
        properties = client.search_properties()
        loins = client.search_loins()
        projects = client.search_projects()
        client.login(credentials)
    """

    def __init__(self, auth_service: AuthService, base_url: str = BIMPortalConfig.BASE_URL,
                 raise_on_unexpected_status: bool = False):
        """
        Initialize the enhanced BIM Portal client.

        Args:
            auth_service: Authentication service instance
            base_url: Base URL for the BIM Portal API
            raise_on_unexpected_status: Whether to raise exceptions on HTTP errors
        """
        super().__init__(auth_service, base_url, raise_on_unexpected_status)
