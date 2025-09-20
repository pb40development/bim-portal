"""
BIM Portal Client Package

Refactored client using mixins for better organization and maintainability.
"""

from .enhanced_bim_client import EnhancedBimPortalClient
from .base_client import BaseClient
from .auth_mixin import AuthMixin
from .properties_mixin import PropertiesMixin
from .aia_mixin import AiaMixin

__version__ = "0.1.0"

__all__ = [
    'EnhancedBimPortalClient',
    'BaseClient',
    'AuthMixin',
    'PropertiesMixin',
    'AiaMixin'
]
