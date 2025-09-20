"""
AIA template export examples for BIM Portal Python client.

This module demonstrates AIA template export workflows in multiple formats including 
PDF and OpenOffice with automatic file type detection.
"""

import os
import logging
from pathlib import Path
from typing import Dict, Optional

from dotenv import load_dotenv

from client.auth.auth_config import BIM_PORTAL_PASSWORD_ENV_VAR, BIM_PORTAL_USERNAME_ENV_VAR
from client.auth.auth_service_impl import AuthService
from client.enhanced_bim_client import EnhancedBimPortalClient
from client.config import BIMPortalConfig
from examples.export_examples.utils.export_utils import ExportUtils

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
        print("=" * 60)
        return False
    return True


def run_template_export_examples(client: EnhancedBimPortalClient):
    """
    Run AIA template export examples with comprehensive format support.
    
    Args:
        client: Enhanced BIM Portal client
    """
    print("\n" + "=" * 60)
    print("📋 AIA TEMPLATE EXPORT EXAMPLES")
    print("=" * 60)
    
    print("\n1️⃣ Searching for available templates...")
    try:
        templates = client.search_templates()
        if not templates:
            print("🔭 No templates found for export")
            return
        
        print(f"✅ Found {len(templates)} templates:")
        for i, template in enumerate(templates[:3], 1):
            print(f"   {i}. {template.name} ({template.guid})")
        
        selected_template = templates[0]
        print(f"\n🎯 Using template: '{selected_template.name}'")
        
        export_results: Dict[str, Optional[Path]] = {}
        
        print("\n2️⃣ Exporting template...")
        
        # PDF Export with auto-detection
        print("   📄 Exporting as PDF...")
        pdf_content = client.export_template_pdf(selected_template.guid)
        if pdf_content:
            base_filename = f"template_pdf_{selected_template.guid}"
            pdf_path = ExportUtils.export_with_detection(pdf_content, base_filename, "pdf")
            if pdf_path:
                export_results['PDF'] = pdf_path
                print(f"   ✅ PDF exported: {pdf_path}")
            else:
                print("   ❌ PDF export failed: Could not save file")
                export_results['PDF'] = None
        else:
            print("   ❌ PDF export failed: No content received")
            export_results['PDF'] = None
        
        # OpenOffice Export with auto-detection
        print("   📝 Exporting as OpenOffice...")
        odt_content = client.export_template_openoffice(selected_template.guid)
        if odt_content:
            base_filename = f"template_odt_{selected_template.guid}"
            odt_path = ExportUtils.export_with_detection(odt_content, base_filename, "odt")
            if odt_path:
                export_results['OpenOffice'] = odt_path
                print(f"   ✅ OpenOffice exported: {odt_path}")
            else:
                print("   ❌ OpenOffice export failed: Could not save file")
                export_results['OpenOffice'] = None
        else:
            print("   ❌ OpenOffice export failed: No content received")
            export_results['OpenOffice'] = None
        
        # Summary with file type information
        successful_exports = len([path for path in export_results.values() if path is not None])
        total_formats = len(export_results)
        
        print(f"\n📈 Export Summary: {successful_exports}/{total_formats} formats successful")
        
        for format_name, path in export_results.items():
            if path:
                extension = path.suffix[1:].upper() if path.suffix else "UNKNOWN"
                print(f"   ✅ {format_name} ({extension}): {path}")
            else:
                print(f"   ❌ {format_name}: Export failed")
        
        # Additional template details
        print(f"\n📋 Template Details:")
        try:
            detailed_template = client.get_template(selected_template.guid)
            if detailed_template:
                print(f"   Name: {detailed_template.name}")
                print(f"   GUID: {detailed_template.guid}")
                if hasattr(detailed_template, 'description') and detailed_template.description:
                    print(f"   Description: {detailed_template.description}")
                if hasattr(detailed_template, 'version') and detailed_template.version:
                    print(f"   Version: {detailed_template.version}")
                if hasattr(detailed_template, 'template_type') and detailed_template.template_type:
                    print(f"   Type: {detailed_template.template_type}")
            else:
                print("   Could not retrieve detailed information")
        except Exception as e:
            print(f"   Error retrieving details: {e}")
        
        if successful_exports == 0:
            print("💡 Note: Template exports may require special permissions")
        
    except Exception as e:
        logger.error("Error in template export examples", exc_info=True)
        print(f"❌ Error in template export examples: {e}")


def demonstrate_template_search_and_filtering(client: EnhancedBimPortalClient):
    """
    Demonstrate template search and filtering capabilities.
    
    Args:
        client: Enhanced BIM Portal client
    """
    print("\n3️⃣ Template search and filtering examples...")
    
    try:
        # Search all templates
        all_templates = client.search_templates()
        print(f"   📊 Total templates available: {len(all_templates)}")
        
        if all_templates:
            # Show template categories or types if available
            template_types = set()
            for template in all_templates:
                if hasattr(template, 'template_type') and template.template_type:
                    template_types.add(template.template_type)
                elif hasattr(template, 'type') and template.type:
                    template_types.add(template.type)
            
            if template_types:
                print(f"   📂 Template types found: {', '.join(template_types)}")
            
            # Show templates by name length (as an example filter)
            short_names = [t for t in all_templates if len(t.name) < 20]
            long_names = [t for t in all_templates if len(t.name) >= 20]
            
            print(f"   📝 Templates with short names (<20 chars): {len(short_names)}")
            print(f"   📜 Templates with long names (≥20 chars): {len(long_names)}")
            
            # Show newest templates (if timestamps available)
            print(f"   📅 Most recent templates:")
            for template in all_templates[:3]:
                print(f"      - {template.name}")
        
    except Exception as e:
        logger.error("Error in template search examples", exc_info=True)
        print(f"   ❌ Error in template search: {e}")


def main():
    """Main method to run AIA template export examples."""
    print("=" * 70)
    print("🚀 BIM PORTAL AIA TEMPLATE EXPORT EXAMPLES")
    print("=" * 70)
    
    if not check_credentials():
        print("❌ Cannot run export examples without credentials")
        return
    
    if not ExportUtils.is_export_directory_writable():
        print("❌ Export directory is not writable!")
        return
    
    print("🔧 Setting up authenticated client...")
    
    try:
        auth_service = AuthService()
        client = EnhancedBimPortalClient(
            auth_service=auth_service,
            base_url=BIMPortalConfig.BASE_URL
        )
        
        # Run template export examples
        run_template_export_examples(client)
        
        # Demonstrate template search and filtering
        demonstrate_template_search_and_filtering(client)
        
        print("\n" + "=" * 70)
        print("✅ AIA TEMPLATE EXPORT EXAMPLES COMPLETE!")
        print("=" * 70)
        print(f"📂 Check the '{BIMPortalConfig.EXPORT_DIRECTORY}' directory for exported files")
        
    except Exception as e:
        logger.error("Error running template export examples", exc_info=True)
        print(f"❌ Error running examples: {e}")


if __name__ == "__main__":
    main()
