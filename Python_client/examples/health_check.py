import os
import sys
from pathlib import Path

# Ensure we can import from project root
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from dotenv import load_dotenv

from client.auth.auth_service_impl import AuthService, AuthenticationError
from client.enhanced_bim_client import EnhancedBimPortalClient
from client.auth.auth_config import BIM_PORTAL_USERNAME_ENV_VAR

# --- Configuration ---
load_dotenv()
from client.config import BIMPortalConfig

BASE_URL = BIMPortalConfig.BASE_URL


def test_api_connectivity():
    """Test basic API connectivity without authentication."""
    print("Step 1: Testing basic API connectivity...")
    try:
        # Create client without credentials for public access
        auth_service = AuthService(username=None, password=None)
        client = EnhancedBimPortalClient(auth_service=auth_service, base_url=BASE_URL)

        # Simple connectivity test - try to get AIA filters (usually public)
        try:
            filters = client.get_aia_filters()
            print(f"   Success: API is reachable (found {len(filters)} filter groups)")
            return True
        except Exception:
            # Fallback: try searching for public projects
            projects = client.search_projects()
            print(f"   Success: API is reachable (found {len(projects)} public projects)")
            return True

    except Exception as e:
        print(f"   Error: API connectivity failed - {e}")
        return False


def test_authentication():
    """Test authentication with credentials."""
    print("\nStep 2: Testing authentication...")

    # Check if credentials are available
    username = os.getenv(BIM_PORTAL_USERNAME_ENV_VAR)
    if not username:
        print("   Info: No credentials found - skipping authentication test")
        print("   Note: Only public resources will be accessible")
        return None  # Not a failure, just no auth

    print(f"   Credentials found for user: {username}")

    try:
        auth_service = AuthService()
        client = EnhancedBimPortalClient(auth_service=auth_service, base_url=BASE_URL)

        # Test authentication by trying to get user's organizations
        try:
            my_orgs = client.get_my_organisations()
            print(f"   Success: Authenticated (user has access to {len(my_orgs)} organizations)")
            return True
        except Exception:
            # Fallback: try to get all organizations (may require auth)
            all_orgs = client.get_organisations()
            print(f"   Success: Authenticated (found {len(all_orgs)} total organizations)")
            return True

    except AuthenticationError as e:
        print(f"   Error: Authentication failed - {e}")
        print("   Check your username and password in the .env file")
        return False
    except Exception as e:
        print(f"   Error: Unexpected error during authentication test - {e}")
        return False


def test_basic_api_features(client: EnhancedBimPortalClient):
    """Test basic API features with minimal checks."""
    print("\nStep 3: Testing basic API features...")

    features_passed = 0
    total_features = 3

    # Test 1: Search functionality
    try:
        projects = client.search_projects()
        print(f"   Project search: SUCCESS ({len(projects)} projects found)")
        features_passed += 1
    except Exception as e:
        print(f"   Project search: FAILED - {e}")

    # Test 2: LOIN search
    try:
        loins = client.search_loins()
        print(f"   LOIN search: SUCCESS ({len(loins)} LOINs found)")
        features_passed += 1
    except Exception as e:
        print(f"   LOIN search: FAILED - {e}")

    # Test 3: Filter access
    try:
        filters = client.get_aia_filters()
        print(f"   Filter access: SUCCESS ({len(filters)} filter groups found)")
        features_passed += 1
    except Exception as e:
        print(f"   Filter access: FAILED - {e}")

    return features_passed, total_features


def test_detailed_access(client: EnhancedBimPortalClient):
    """Test detailed resource access if resources are available."""
    print("\nStep 4: Testing detailed resource access...")

    try:
        # Try to get details for first available project
        projects = client.search_projects()
        if projects:
            project_details = client.get_project(projects[0].guid)
            if project_details:
                print(f"   Project details: SUCCESS (retrieved '{project_details.name}')")
                return True
            else:
                print("   Project details: FAILED (could not retrieve details)")
                return False
        else:
            print("   Project details: SKIPPED (no projects available)")
            return None
    except Exception as e:
        print(f"   Project details: FAILED - {e}")
        return False


def test_export_functionality(client: EnhancedBimPortalClient):
    """Test export functionality if resources are available."""
    print("\nStep 5: Testing export functionality...")

    try:
        # Try to export first available project
        projects = client.search_projects()
        if projects:
            pdf_content = client.export_project_pdf(projects[0].guid)
            if pdf_content and len(pdf_content) > 0:
                print(f"   PDF export: SUCCESS ({len(pdf_content)} bytes)")
                return True
            else:
                print("   PDF export: FAILED (no content returned)")
                return False
        else:
            print("   PDF export: SKIPPED (no projects available)")
            return None
    except Exception as e:
        print(f"   PDF export: FAILED - {e}")
        return False


def main():
    """
    Minimal health check for the BIM Portal API without GUID requirements.
    """
    print("--- BIM Portal API Health Check (No GUID Required) ---")
    print(f"Testing against: {BASE_URL}")
    print()

    # Test 1: Basic connectivity (required)
    connectivity_ok = test_api_connectivity()
    if not connectivity_ok:
        print("\nHealth check stopped - API is not reachable")
        print("Please check your network connection and BASE_URL configuration")
        return

    # Test 2: Authentication (optional)
    auth_result = test_authentication()

    # Set up client based on authentication result
    if auth_result is True:
        # Authenticated client
        auth_service = AuthService()
        client = EnhancedBimPortalClient(auth_service=auth_service, base_url=BASE_URL)
        print("   Using authenticated client for remaining tests")
    else:
        # Public client
        auth_service = AuthService(username=None, password=None)
        client = EnhancedBimPortalClient(auth_service=auth_service, base_url=BASE_URL)
        print("   Using public client for remaining tests")

    # Test 3: Basic API features (required)
    features_passed, total_features = test_basic_api_features(client)

    # Test 4: Detailed access (optional)
    details_ok = test_detailed_access(client)

    # Test 5: Export functionality (optional)
    export_ok = test_export_functionality(client)

    # Summary
    print("\n" + "=" * 60)
    print("HEALTH CHECK SUMMARY")
    print("=" * 60)
    print(f"API Connectivity:      {'PASS' if connectivity_ok else 'FAIL'}")

    if auth_result is True:
        print(f"Authentication:        PASS")
    elif auth_result is False:
        print(f"Authentication:        FAIL")
    else:
        print(f"Authentication:        SKIPPED (no credentials)")

    print(f"Basic API Features:    {features_passed}/{total_features} PASS")

    if details_ok is True:
        print(f"Detailed Access:       PASS")
    elif details_ok is False:
        print(f"Detailed Access:       FAIL")
    else:
        print(f"Detailed Access:       SKIPPED")

    if export_ok is True:
        print(f"Export Functions:      PASS")
    elif export_ok is False:
        print(f"Export Functions:      FAIL")
    else:
        print(f"Export Functions:      SKIPPED")

    # Overall assessment
    print()
    if connectivity_ok and features_passed >= 2:
        if auth_result is True and details_ok is True:
            print("OVERALL STATUS: FULLY HEALTHY")
            print("✓ All systems operational with full authentication")
        elif features_passed == total_features:
            print("OVERALL STATUS: HEALTHY")
            print("✓ Core functionality working (public access)")
        else:
            print("OVERALL STATUS: MOSTLY HEALTHY")
            print("✓ Basic functionality works, some features may be limited")
    else:
        print("OVERALL STATUS: UNHEALTHY")
        print("✗ Significant issues detected")

        # Provide specific guidance
        if not connectivity_ok:
            print("  → Check network connection and API URL")
        elif features_passed < 2:
            print("  → API may be down or configuration is incorrect")
        if auth_result is False:
            print("  → Verify credentials in .env file")

    print("=" * 60)

    # Additional info
    print("\nNOTE: This health check no longer requires any GUIDs")
    print("It uses dynamic discovery to test available resources")
    if auth_result is None:
        print("For full functionality testing, add credentials to .env file")


if __name__ == "__main__":
    main()