"""
LOIN export examples for BIM Portal Python client.

This module demonstrates LOIN export workflows in multiple formats including 
PDF, OpenOffice, OKSTRA, LOIN-XML, and IDS with automatic content type detection.
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
from examples.utils.export_utils import ExportUtils

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


def run_loin_export_examples(client: EnhancedBimPortalClient):
    """
    Run LOIN export examples with comprehensive format support.
    
    Args:
        client: Enhanced BIM Portal client
    """
    print("\n" + "=" * 60)
    print("📋 LOIN EXPORT EXAMPLES")
    print("=" * 60)
    
    print("\n1️⃣ Searching for available LOINs...")
    try:
        loins = client.search_loins()
        if not loins:
            print("🔭 No LOINs found for export")
            return
        
        print(f"✅ Found {len(loins)} LOINs:")
        for i, loin in enumerate(loins[:3], 1):
            print(f"   {i}. {loin.name} ({loin.guid})")
        
        selected_loin = loins[0]
        print(f"\n🎯 Using LOIN: '{selected_loin.name}'")
        
        export_results: Dict[str, Optional[Path]] = {}
        
        print("\n2️⃣ Exporting LOIN in multiple formats...")
        
        # PDF Export with auto-detection
        print("   📄 Exporting as PDF...")
        pdf_content = client.export_loin_pdf(selected_loin.guid)
        if pdf_content:
            base_filename = f"loin_pdf_{selected_loin.guid}"
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
        odt_content = client.export_loin_openoffice(selected_loin.guid)
        if odt_content:
            base_filename = f"loin_odt_{selected_loin.guid}"
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
        
        # OKSTRA Export with auto-detection
        print("   🗂️ Exporting as OKSTRA...")
        okstra_content = client.export_loin_okstra(selected_loin.guid)
        if okstra_content:
            base_filename = f"loin_okstra_{selected_loin.guid}"
            okstra_path = ExportUtils.export_with_detection(okstra_content, base_filename, "zip")
            if okstra_path:
                export_results['OKSTRA'] = okstra_path
                print(f"   ✅ OKSTRA exported: {okstra_path}")
            else:
                print("   ❌ OKSTRA export failed: Could not save file")
                export_results['OKSTRA'] = None
        else:
            print("   ❌ OKSTRA export failed: No content received")
            export_results['OKSTRA'] = None
        
        # LOIN-XML Export with auto-detection
        print("   🔗 Exporting as LOIN-XML...")
        xml_content = client.export_loin_xml(selected_loin.guid)
        if xml_content:
            base_filename = f"loin_xml_{selected_loin.guid}"
            xml_path = ExportUtils.export_with_detection(xml_content, base_filename, "xml")
            if xml_path:
                export_results['LOIN-XML'] = xml_path
                print(f"   ✅ LOIN-XML exported: {xml_path}")
            else:
                print("   ❌ LOIN-XML export failed: Could not save file")
                export_results['LOIN-XML'] = None
        else:
            print("   ❌ LOIN-XML export failed: No content received")
            export_results['LOIN-XML'] = None
        
        # IDS Export with auto-detection
        print("   🆔 Exporting as IDS...")
        ids_content = client.export_loin_ids(selected_loin.guid)
        if ids_content:
            base_filename = f"loin_ids_{selected_loin.guid}"
            ids_path = ExportUtils.export_with_detection(ids_content, base_filename, "ids")
            if ids_path:
                export_results['IDS'] = ids_path
                print(f"   ✅ IDS exported: {ids_path}")
            else:
                print("   ❌ IDS export failed: Could not save file")
                export_results['IDS'] = None
        else:
            print("   ❌ IDS export failed: No content received")
            export_results['IDS'] = None
        
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
        
        if successful_exports < 3:
            print("💡 Note: Some export formats may require special permissions or project setup")
            print("💡 Content type detection helps ensure correct file extensions are used")
        
        # Additional LOIN details
        print(f"\n📋 LOIN Details:")
        try:
            detailed_loin = client.get_loin(selected_loin.guid)
            if detailed_loin:
                print(f"   Name: {detailed_loin.name}")
                print(f"   GUID: {detailed_loin.guid}")
                if hasattr(detailed_loin, 'description') and detailed_loin.description:
                    print(f"   Description: {detailed_loin.description}")
                if hasattr(detailed_loin, 'version') and detailed_loin.version:
                    print(f"   Version: {detailed_loin.version}")
            else:
                print("   Could not retrieve detailed information")
        except Exception as e:
            print(f"   Error retrieving details: {e}")
        
    except Exception as e:
        logger.error(f"Error in LOIN export examples: {e}")
        print(f"❌ Error in LOIN export examples: {e}")


def main():
    """Main method to run LOIN export examples."""
    print("=" * 70)
    print("🚀 BIM PORTAL LOIN EXPORT EXAMPLES")
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
        
        # Run LOIN export examples
        run_loin_export_examples(client)
        
        print("\n" + "=" * 70)
        print("✅ LOIN EXPORT EXAMPLES COMPLETE!")
        print("=" * 70)
        print(f"📂 Check the '{BIMPortalConfig.EXPORT_DIRECTORY}' directory for exported files")
        
    except Exception as e:
        logger.error(f"Error running LOIN export examples: {e}")
        print(f"❌ Error running examples: {e}")


if __name__ == "__main__":
    main()
