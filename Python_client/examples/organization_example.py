"""
Organization examples for BIM Portal Python client.

This module demonstrates organization functionality including:
- Getting all organizations (public endpoint)
- Getting user organizations (authenticated)
- Organization search and filtering capabilities
"""

import os
import sys
from pathlib import Path

# Ensure we can import from project root
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import logging
from typing import List, Optional
from uuid import UUID

from dotenv import load_dotenv

from client.auth.auth_config import BIM_PORTAL_PASSWORD_ENV_VAR, BIM_PORTAL_USERNAME_ENV_VAR
from client.auth.auth_service_impl import AuthService
from client.enhanced_bim_client import EnhancedBimPortalClient
from client.config import BIMPortalConfig

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()


def check_credentials() -> bool:
    """
    Check if credentials are available for authentication.
    
    Returns:
        True if credentials are configured
    """
    if not os.getenv(BIM_PORTAL_USERNAME_ENV_VAR) or not os.getenv(BIM_PORTAL_PASSWORD_ENV_VAR):
        print("=" * 60)
        print("WARNING: Credentials not found in environment variables.")
        print(f"Please set {BIM_PORTAL_USERNAME_ENV_VAR} and {BIM_PORTAL_PASSWORD_ENV_VAR} in .env file.")
        print("Some organization examples require authentication.")
        print("=" * 60)
        return False
    return True


def run_organization_examples(client: EnhancedBimPortalClient):
    """
    Demonstrate organization API usage.
    
    Args:
        client: Enhanced BIM Portal client
    """
    print("\n" + "=" * 60)
    print("🏢 ORGANIZATION API EXAMPLES")
    print("=" * 60)
    
    print("\n1️⃣ Fetching all available organizations (public endpoint)...")
    try:
        all_organizations = client.get_organisations()
        print(f"✅ Found {len(all_organizations)} available organizations:")
        
        for i, org in enumerate(all_organizations[:5], 1):
            description = f" - {org.description}" if hasattr(org, 'description') and org.description else ""
            print(f"   {i}. {org.name} ({org.guid}){description}")
        
        if len(all_organizations) > 5:
            print(f"   ... and {len(all_organizations) - 5} more")
            
    except Exception as e:
        print(f"❌ Error fetching organizations: {e}")
        logger.error("Error fetching organizations", exc_info=True)
    
    print("\n2️⃣ Testing organization search functionality...")
    try:
        all_orgs = client.get_organisations()
        if all_orgs:
            first_org = all_orgs[0]
            
            # Test GUID search
            found_by_guid = find_organization_by_guid(all_orgs, first_org.guid)
            print(f"   🔍 Search by GUID: {'✅ Found' if found_by_guid else '❌ Not found'}")
            
            # Test name search
            if hasattr(first_org, 'name') and first_org.name:
                found_by_name = find_organization_by_name(all_orgs, first_org.name)
                print(f"   🔍 Search by name: {'✅ Found' if found_by_name else '❌ Not found'}")
            
            # Test availability check
            has_orgs = len(all_orgs) > 0
            print(f"   📊 Organizations available: {'✅ Yes' if has_orgs else '❌ No'}")
            
    except Exception as e:
        print(f"❌ Error in organization search tests: {e}")
        logger.error("Error in organization search tests", exc_info=True)
    
    print("\n3️⃣ Testing user organizations (requires authentication)...")
    if not is_authenticated(client):
        print("   ⚠️  Authentication required for user organization endpoints")
        print("   💡 Client is not authenticated - skipping user organization examples")
    else:
        print("   ✅ Client is authenticated")
        demonstrate_user_organization_methods(client)


def find_organization_by_guid(organizations: List, guid: UUID) -> Optional[any]:
    """Find organization by GUID."""
    for org in organizations:
        if org.guid == guid:
            return org
    return None


def find_organization_by_name(organizations: List, name: str) -> Optional[any]:
    """Find organization by name."""
    for org in organizations:
        if hasattr(org, 'name') and org.name == name:
            return org
    return None


def is_authenticated(client: EnhancedBimPortalClient) -> bool:
    """Check if client is authenticated."""
    try:
        # Try to get a valid token to check authentication
        token = client.auth_service.get_valid_token()
        return token is not None
    except Exception:
        return False


def demonstrate_user_organization_methods(client: EnhancedBimPortalClient):
    """Demonstrate user organization methods."""
    print("\n   🔍 User Organization Methods:")
    
    try:
        # Get user organizations
        print("   1️⃣ Getting user organizations...")
        user_orgs = client.get_my_organisations()
        print(f"   ✅ Found {len(user_orgs)} organizations for user")
        
        for i, org in enumerate(user_orgs[:3], 1):
            print(f"      👤 {org.name} ({org.guid})")
        
        if len(user_orgs) > 3:
            print(f"      ... and {len(user_orgs) - 3} more")
        
        # Organization count
        print(f"\n   2️⃣ Organization count: {len(user_orgs)} organizations")
        
        # Organization names
        print("\n   3️⃣ Getting organization names...")
        org_names = [org.name for org in user_orgs if hasattr(org, 'name')]
        print(f"   ✅ Organization names: {', '.join(org_names)}")
        
        # First organization (convenience method)
        print("\n   4️⃣ Getting first user organization...")
        if user_orgs:
            first_user_org = user_orgs[0]
            print(f"   ✅ First organization: {first_user_org.name}")
        else:
            print("   ⚠️  No organizations found for user")
            
    except Exception as e:
        print(f"   ❌ Error in user organization API calls: {e}")
        logger.error("Error in user organization API calls", exc_info=True)
        
        # Provide debugging info
        error_msg = str(e).lower()
        if "404" in error_msg or "not found" in error_msg:
            print("   💡 404 error suggests the user organization endpoint may not be available")
        elif "401" in error_msg or "unauthorized" in error_msg:
            print("   💡 401 error suggests authentication issues")
        elif "403" in error_msg or "forbidden" in error_msg:
            print("   💡 403 error suggests insufficient permissions for user organization access")


def demonstrate_jwt_token_analysis(client: EnhancedBimPortalClient):
    """Demonstrate JWT token analysis for debugging."""
    print("\n" + "=" * 60)
    print("🔍 JWT TOKEN ANALYSIS FOR DEBUGGING")
    print("=" * 60)
    
    if not is_authenticated(client):
        print("❌ Not authenticated - cannot analyze JWT token")
        return
    
    try:
        # Get current token for analysis
        current_token = client.auth_service.get_valid_token()
        if current_token:
            print("✅ Current token available for analysis")
            
            # Analyze token structure
            analyze_jwt_token_structure(current_token)
            
        else:
            print("❌ No valid token available for analysis")
            
    except Exception as e:
        print(f"❌ Error in JWT token analysis: {e}")
        logger.error("Error in JWT token analysis", exc_info=True)


def analyze_jwt_token_structure(token: str):
    """Analyze JWT token structure for debugging purposes."""
    try:
        import base64
        import json
        
        print("\n🔬 JWT Token Structure Analysis:")
        
        parts = token.split(".")
        print(f"   📋 Token parts: {len(parts)} (expected: 3 for JWT)")
        
        if len(parts) >= 2:
            # Decode and display payload
            # Add padding if needed for base64 decoding
            payload_b64 = parts[1]
            payload_b64 += "=" * (4 - len(payload_b64) % 4)
            
            try:
                payload_bytes = base64.urlsafe_b64decode(payload_b64)
                payload = payload_bytes.decode('utf-8')
                payload_json = json.loads(payload)
                
                print(f"   📄 JWT Payload preview: {str(payload_json)[:200]}...")
                
                # Look for common user ID claims
                print("   🔍 Checking for user ID claims:")
                check_for_claim(payload_json, "sub") # This is the user id
                check_for_claim(payload_json, "email") # This is the username

                
            except Exception as decode_error:
                print(f"   ❌ Failed to decode payload: {decode_error}")
                
    except Exception as e:
        print(f"   ❌ Failed to analyze token structure: {e}")


def check_for_claim(payload_json: dict, claim_name: str):
    """Check if a specific claim exists in the JWT payload."""
    if claim_name in payload_json:
        value = payload_json[claim_name]
        print(f"      ✅ {claim_name}: {value}")
    else:
        print(f"      ❌ {claim_name}: not found")


def main():
    """Main method to run organization examples."""
    print("=" * 70)
    print("🚀 BIM PORTAL ORGANIZATION API EXAMPLES")
    print("   📋 Features: Organization Management & JWT Analysis")
    print("=" * 70)
    
    has_credentials = check_credentials()
    
    print("🔧 Setting up client...")
    
    try:
        auth_service = AuthService()
        client = EnhancedBimPortalClient(
            auth_service=auth_service,
            base_url=BIMPortalConfig.BASE_URL
        )
        
        # Run organization examples
        run_organization_examples(client)
        
        # Run JWT token analysis for debugging (if authenticated)
        if has_credentials and is_authenticated(client):
            demonstrate_jwt_token_analysis(client)
        
        print("\n" + "=" * 70)
        print("✅ ORGANIZATION EXAMPLES COMPLETE!")
        print("=" * 70)
        
        if has_credentials and is_authenticated(client):
            print("🎯 Key achievements:")
            print("   ✅ Organization API endpoints demonstrated")
            print("   ✅ User organization access tested")
            print("   ✅ JWT token analysis performed")
        else:
            print("💡 Set up credentials to test authenticated organization endpoints")
            print("   and experience JWT token analysis")
        
    except Exception as e:
        logger.error("Error running organization examples", exc_info=True)
        print(f"❌ Error running examples: {e}")


if __name__ == "__main__":
    main()
