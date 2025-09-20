"""
Context information export examples for BIM Portal Python client.

This module demonstrates context information export workflows in multiple formats including 
PDF and OpenOffice with automatic file type detection.
"""

import os
import sys
from pathlib import Path

# Ensure we can import from project root
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

import logging
from typing import Dict, Optional

from dotenv import load_dotenv

from client.auth.auth_config import BIM_PORTAL_PASSWORD_ENV_VAR, BIM_PORTAL_USERNAME_ENV_VAR
from client.auth.auth_service_impl import AuthService
from client.enhanced_bim_client import EnhancedBimPortalClient
from client.config import BIMPortalConfig
from examples.export_examples.utils.common_utils import check_credentials
from examples.export_examples.utils.export_utils import ExportUtils

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()



def run_context_info_export_examples(client: EnhancedBimPortalClient):
    """
    Run context information export examples with comprehensive format support.
    
    Args:
        client: Enhanced BIM Portal client
    """
    print("\n" + "=" * 60)
    print("📚 CONTEXT INFORMATION EXPORT EXAMPLES")
    print("=" * 60)
    
    print("\n1️⃣ Searching for available context information...")
    try:
        context_infos = client.search_context_info()
        if not context_infos:
            print("🔭 No context information found for export")
            return
        
        print(f"✅ Found {len(context_infos)} context information items:")
        for i, context in enumerate(context_infos[:5], 1):
            print(f"   {i}. {context.name} ({context.guid})")
        
        selected_context = context_infos[0]
        print(f"\n🎯 Using context info: '{selected_context.name}'")
        
        export_results: Dict[str, Optional[Path]] = {}
        
        print("\n2️⃣ Exporting context information...")
        
        # PDF Export with auto-detection
        print("   📄 Exporting as PDF...")
        pdf_content = client.export_context_info_pdf(selected_context.guid)
        if pdf_content:
            base_filename = f"context_pdf_{selected_context.guid}"
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
        odt_content = client.export_context_info_openoffice(selected_context.guid)
        if odt_content:
            base_filename = f"context_odt_{selected_context.guid}"
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
        
        # Additional context info details
        print(f"\n📋 Context Information Details:")
        try:
            detailed_context = client.get_context_info(selected_context.guid)
            if detailed_context:
                print(f"   Name: {detailed_context.name}")
                print(f"   GUID: {detailed_context.guid}")
                if hasattr(detailed_context, 'description') and detailed_context.description:
                    print(f"   Description: {detailed_context.description}")
                if hasattr(detailed_context, 'version') and detailed_context.version:
                    print(f"   Version: {detailed_context.version}")
                if hasattr(detailed_context, 'context_type') and detailed_context.context_type:
                    print(f"   Type: {detailed_context.context_type}")
            else:
                print("   Could not retrieve detailed information")
        except Exception as e:
            print(f"   Error retrieving details: {e}")
        
        if successful_exports == 0:
            print("💡 Note: Context information may require special permissions to export")
        
    except Exception as e:
        logger.error(f"Error in context info export examples: {e}")
        print(f"❌ Error in context info export examples: {e}")


def main():
    """Main method to run context information export examples."""
    print("=" * 70)
    print("🚀 BIM PORTAL CONTEXT INFORMATION EXPORT EXAMPLES")
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
        
        # Run context info export examples
        run_context_info_export_examples(client)
        
        print("\n" + "=" * 70)
        print("✅ CONTEXT INFORMATION EXPORT EXAMPLES COMPLETE!")
        print("=" * 70)
        print(f"📂 Check the '{BIMPortalConfig.EXPORT_DIRECTORY}' directory for exported files")
        
    except Exception as e:
        logger.error(f"Error running context information export examples: {e}")
        print(f"❌ Error running examples: {e}")


if __name__ == "__main__":
    main()
