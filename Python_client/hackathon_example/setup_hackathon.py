"""
BIM Portal setup utilities.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

from client.auth.auth_config import BIM_PORTAL_PASSWORD_ENV_VAR, BIM_PORTAL_USERNAME_ENV_VAR
from client.auth.auth_service_impl import AuthService
from client.enhanced_bim_client import EnhancedBimPortalClient
from client.config import BIMPortalConfig

load_dotenv()


def setup_bim_portal(credentials_file: str = "../.env"):
    """
    Setup BIM Portal client for hackathon use.

    Returns:
        Enhanced BIM Portal client or None if setup failed
    """
    print("🔧 Setting up BIM Portal connection...")

    # Check credentials
    if not _check_credentials():
        print("❌ Credentials missing - run: python demo/credentials_setup.py")
        return None

    try:
        # Setup client
        auth_service = AuthService()
        client = EnhancedBimPortalClient(
            auth_service=auth_service,
            base_url=BIMPortalConfig.BASE_URL
        )

        # Create exports directory
        exports_dir = Path(BIMPortalConfig.EXPORT_DIRECTORY)
        exports_dir.mkdir(exist_ok=True)

        # Test connection
        if _test_connection(client):
            print("✅ Connected to BIM Portal!")
            return client
        else:
            print("❌ Connection failed")
            return None

    except Exception as e:
        print(f"❌ Setup error: {e}")
        return None


def _check_credentials() -> bool:
    """Check if credentials are configured."""
    return (os.getenv(BIM_PORTAL_USERNAME_ENV_VAR) and
            os.getenv(BIM_PORTAL_PASSWORD_ENV_VAR))


def _test_connection(client) -> bool:
    """Test basic API connectivity."""
    try:
        projects = client.search_projects()
        return True
    except:
        return False
