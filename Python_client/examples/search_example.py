"""
Search and filter examples for BIM Portal Python client.

This module demonstrates search functionality for projects, properties, 
filters, and organizations according to the BIM Portal API.
"""

import os
import sys
from pathlib import Path

# Ensure we can import from project root
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
import logging

from dotenv import load_dotenv

from client.auth.auth_config import BIM_PORTAL_PASSWORD_ENV_VAR, BIM_PORTAL_USERNAME_ENV_VAR
from client.auth.auth_service_impl import AuthService
from client.enhanced_bim_client import EnhancedBimPortalClient
from client.config import BIMPortalConfig
from client.models import AiaProjectForPublicRequest, PropertyOrGroupForPublicRequest
from examples.export_examples.utils.common_utils import check_credentials

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()


def run_search_examples(client: EnhancedBimPortalClient):
    """
    Demonstrate search and filtering capabilities.
    
    Args:
        client: Enhanced BIM Portal client
    """
    print("\n" + "=" * 60)
    print("🔍 SEARCH AND FILTER EXAMPLES")
    print("=" * 60)
    
    print("\n1️⃣ Searching projects with criteria...")
    try:
        # Create search request with criteria
        search_request = AiaProjectForPublicRequest(searchString="AIA")
        projects = client.search_projects(search_request)
        
        print(f"✅ Found {len(projects)} projects matching 'AIA':")
        for project in projects[:5]:  # Show first 5 results
            print(f"   📂 {project.name}")
            
        if len(projects) > 5:
            print(f"   ... and {len(projects) - 5} more")
            
    except Exception as e:
        logger.error("Error in project search example", exc_info=True)
        print(f"❌ Error in project search: {e}")
    
    print("\n2️⃣ Searching properties with criteria...")
    try:
        # Create property search request
        property_request = PropertyOrGroupForPublicRequest(searchString="Abdeckung")
        properties = client.search_properties(property_request)
        
        print(f"✅ Found {len(properties)} properties matching 'Abdeckung':")
        for i, prop in enumerate(properties[:5], 1):
            data_type = getattr(prop, 'data_type', 'Unknown') if hasattr(prop, 'data_type') else 'Unknown'
            print(f"   🔑 {prop.name} ({data_type})")
            
        if len(properties) > 5:
            print(f"   ... and {len(properties) - 5} more")
            
    except Exception as e:
        logger.error("Error in property search example", exc_info=True)
        print(f"❌ Error in property search: {e}")
    
    print("\n3️⃣ Searching LOINs with criteria...")
    try:
        # Search for LOINs
        loins = client.search_loins()
        print(f"✅ Found {len(loins)} LOINs:")
        for loin in loins[:5]:
            print(f"   📋 {loin.name}")
            
        if len(loins) > 5:
            print(f"   ... and {len(loins) - 5} more")
            
    except Exception as e:
        logger.error("Error in LOIN search example", exc_info=True)
        print(f"❌ Error in LOIN search: {e}")
    
    print("\n4️⃣ Searching domain models...")
    try:
        domain_models = client.search_domain_models()
        print(f"✅ Found {len(domain_models)} domain models:")
        for model in domain_models[:5]:
            print(f"   🗂️ {model.name}")
            
        if len(domain_models) > 5:
            print(f"   ... and {len(domain_models) - 5} more")
            
    except Exception as e:
        logger.error("Error in domain model search example", exc_info=True)
        print(f"❌ Error in domain model search: {e}")


def run_filter_examples(client: EnhancedBimPortalClient):
    """
    Demonstrate filter functionality.
    
    Args:
        client: Enhanced BIM Portal client
    """
    print("\n" + "=" * 60)
    print("🔧 FILTER EXAMPLES")
    print("=" * 60)
    
    print("\n1️⃣ Getting AIA filters...")
    try:
        aia_filters = client.get_aia_filters()
        if aia_filters:
            print(f"✅ Found {len(aia_filters)} AIA filter groups:")
            for i, filter_group in enumerate(aia_filters[:3], 1):
                print(f"   📂 {filter_group.name}")
                if hasattr(filter_group, 'filters') and filter_group.filters:
                    for j, filter_item in enumerate(filter_group.filters[:2], 1):
                        print(f"     - {filter_item.name}")
                elif hasattr(filter_group, 'filter') and filter_group.filter:
                    for j, filter_item in enumerate(filter_group.filter[:2], 1):
                        print(f"     - {filter_item.name}")
                        
            if len(aia_filters) > 3:
                print(f"   ... and {len(aia_filters) - 3} more filter groups")
        else:
            print("🔭 No AIA filters found")
            
    except Exception as e:
        logger.error("Error getting AIA filters", exc_info=True)
        print(f"❌ Error getting AIA filters: {e}")
    
    print("\n2️⃣ Getting property filters...")
    try:
        property_filters = client.get_merkmale_filters()
        if property_filters:
            print(f"✅ Found {len(property_filters)} property filter groups:")
            for i, filter_group in enumerate(property_filters[:3], 1):
                print(f"   📂 {filter_group.name}")
                if hasattr(filter_group, 'filters') and filter_group.filters:
                    for j, filter_item in enumerate(filter_group.filters[:2], 1):
                        print(f"     - {filter_item.name}")
                elif hasattr(filter_group, 'filter') and filter_group.filter:
                    for j, filter_item in enumerate(filter_group.filter[:2], 1):
                        print(f"     - {filter_item.name}")
                        
            if len(property_filters) > 3:
                print(f"   ... and {len(property_filters) - 3} more filter groups")
        else:
            print("🔭 No property filters found")
            
    except Exception as e:
        logger.error("Error getting property filters", exc_info=True)
        print(f"❌ Error getting property filters: {e}")


def run_advanced_search_examples(client: EnhancedBimPortalClient):
    """
    Demonstrate advanced search functionality with different parameters.
    
    Args:
        client: Enhanced BIM Portal client
    """
    print("\n" + "=" * 60)
    print("🔍 ADVANCED SEARCH EXAMPLES")
    print("=" * 60)
    
    print("\n1️⃣ Search with empty criteria (get all)...")
    try:
        # Search with no specific criteria to get all available items
        all_projects = client.search_projects()
        print(f"✅ Found {len(all_projects)} total projects")
        
        all_properties = client.search_properties()
        print(f"✅ Found {len(all_properties)} total properties")
        
        all_loins = client.search_loins()
        print(f"✅ Found {len(all_loins)} total LOINs")
        
    except Exception as e:
        logger.error("Error in advanced search examples", exc_info=True)
        print(f"❌ Error in advanced search: {e}")
    
    print("\n2️⃣ Search with specific filters...")
    try:
        # Example of more targeted searches
        common_search_terms = ["BIM", "IFC", "Projekt", "Modell"]
        
        for term in common_search_terms:
            print(f"   🔍 Searching for '{term}':")
            
            # Search projects
            project_request = AiaProjectForPublicRequest(searchString=term)
            projects = client.search_projects(project_request)
            print(f"      📂 Projects: {len(projects)} found")
            
            # Search properties  
            property_request = PropertyOrGroupForPublicRequest(searchString=term)
            properties = client.search_properties(property_request)
            print(f"      🔑 Properties: {len(properties)} found")
            
    except Exception as e:
        logger.error("Error in filtered search examples", exc_info=True)
        print(f"❌ Error in filtered search: {e}")


def main():
    """Main method to run search and filter examples."""
    print("=" * 70)
    print("🚀 BIM PORTAL SEARCH AND FILTER EXAMPLES")
    print("=" * 70)
    
    if not check_credentials():
        print("❌ Cannot run examples without credentials")
        return
    
    print("🔧 Setting up authenticated client...")
    
    try:
        auth_service = AuthService()
        client = EnhancedBimPortalClient(
            auth_service=auth_service,
            base_url=BIMPortalConfig.BASE_URL
        )
        
        # Run search examples
        run_search_examples(client)
        
        # Run filter examples  
        run_filter_examples(client)
        
        # Run advanced search examples
        run_advanced_search_examples(client)
        
        print("\n" + "=" * 70)
        print("✅ SEARCH AND FILTER EXAMPLES COMPLETE!")
        print("=" * 70)
        
    except Exception as e:
        logger.error("Error running search examples", exc_info=True)
        print(f"❌ Error running examples: {e}")


if __name__ == "__main__":
    main()