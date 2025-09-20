"""
Project export examples for BIM Portal Python client.

This module demonstrates project export workflows in multiple formats including 
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


def find_exportable_project(client: EnhancedBimPortalClient):
    """
    Find the first project that can actually be exported.
    
    Args:
        client: Enhanced BIM Portal client
        
    Returns:
        First exportable project or None if none found
    """
    try:
        projects = client.search_projects()
        if not projects:
            return None
        
        print(f"Checking {len(projects)} projects for export capability...")
        
        for i, project in enumerate(projects, 1):
            print(f"   Testing project {i}: {project.name[:30]}...")
            
            # First check if we can get project details
            detailed_project = client.get_project(project.guid)
            if detailed_project is None:
                print(f"      Skip: Cannot access project details")
                continue
            
            # Then test if PDF export works
            response = client.get(f"/aia/api/v1/public/aiaProject/{project.guid}/pdf")
            if response.status_code == 200:
                print(f"      Found exportable project: {project.name}")
                return project
            else:
                print(f"      Skip: Export not available (status: {response.status_code})")
        
        print("   No exportable projects found")
        return None
        
    except Exception as e:
        print(f"Error finding exportable project: {e}")
        return None


def run_project_export_examples(client: EnhancedBimPortalClient):
    """
    Run project export examples with comprehensive format support.
    
    Args:
        client: Enhanced BIM Portal client
    """
    print("\n" + "=" * 60)
    print("📊 PROJECT EXPORT EXAMPLES")
    print("=" * 60)
    
    print("\n1️⃣ Searching for available projects...")
    try:
        projects = client.search_projects()
        if not projects:
            print("🔭 No projects found for export")
            return
        
        print(f"✅ Found {len(projects)} projects:")
        print("📝 First 5 available projects:")
        for i, project in enumerate(projects[:5], 1):
            print(f"   {i}. {project.name} ({project.guid})")
        
        # Use the first project or implement smart selection
        selected_project = projects[0]
        print(f"\n🎯 Using project: '{selected_project.name}'")
        
        export_results: Dict[str, Optional[Path]] = {}
        
        print("\n2️⃣ Exporting project in multiple formats...")
        
        # PDF Export with auto-detection
        print("   📄 Exporting as PDF...")
        pdf_content = client.export_project_pdf(selected_project.guid)
        if pdf_content:
            base_filename = f"project_pdf_{selected_project.guid}"
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
        odt_content = client.export_project_openoffice(selected_project.guid)
        if odt_content:
            base_filename = f"project_odt_{selected_project.guid}"
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
        okstra_content = client.export_project_okstra(selected_project.guid)
        if okstra_content:
            base_filename = f"project_okstra_{selected_project.guid}"
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
        
        # LOIN-XML Export with auto-detection (may require special permissions)
        print("   🔗 Exporting as LOIN-XML...")
        try:
            loin_xml_content = client.export_project_loin_xml(selected_project.guid)
            if loin_xml_content:
                base_filename = f"project_loin_{selected_project.guid}"
                xml_path = ExportUtils.export_with_detection(loin_xml_content, base_filename, "zip")
                if xml_path:
                    export_results['LOIN-XML'] = xml_path
                    print(f"   ✅ LOIN-XML exported: {xml_path}")
                else:
                    print("   ❌ LOIN-XML export failed: Could not save file")
                    export_results['LOIN-XML'] = None
            else:
                print("   ⚠️ LOIN-XML export failed (may require special permissions)")
                export_results['LOIN-XML'] = None
        except Exception as e:
            print(f"   ⚠️ LOIN-XML export error: {e}")
            export_results['LOIN-XML'] = None
        
        # IDS Export with auto-detection (may require special permissions)
        print("   🆔 Exporting as IDS...")
        try:
            ids_content = client.export_project_ids(selected_project.guid)
            if ids_content:
                base_filename = f"project_ids_{selected_project.guid}"
                ids_path = ExportUtils.export_with_detection(ids_content, base_filename, "ids")
                if ids_path:
                    export_results['IDS'] = ids_path
                    print(f"   ✅ IDS exported: {ids_path}")
                else:
                    print("   ❌ IDS export failed: Could not save file")
                    export_results['IDS'] = None
            else:
                print("   ⚠️ IDS export failed (may require special permissions)")
                export_results['IDS'] = None
        except Exception as e:
            print(f"   ⚠️ IDS export error: {e}")
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
        
        # Additional project details
        print(f"\n📋 Project Details:")
        try:
            detailed_project = client.get_project(selected_project.guid)
            if detailed_project:
                print(f"   Name: {detailed_project.name}")
                print(f"   GUID: {detailed_project.guid}")
                if hasattr(detailed_project, 'description') and detailed_project.description:
                    print(f"   Description: {detailed_project.description}")
                if hasattr(detailed_project, 'status') and detailed_project.status:
                    print(f"   Status: {detailed_project.status}")
            else:
                print("   Could not retrieve detailed information")
        except Exception as e:
            print(f"   Error retrieving details: {e}")
        
    except Exception as e:
        logger.error(f"Error in project export examples: {e}")
        print(f"❌ Error in project export examples: {e}")


def main():
    """Main method to run project export examples."""
    print("=" * 70)
    print("🚀 BIM PORTAL PROJECT EXPORT EXAMPLES")
    print("=" * 70)
    
    if not check_credentials():
        print("❌ Cannot run export examples without credentials")
        return
    
    if not ExportUtils.is_export_directory_writable():
        print("❌ Export directory is not writable!")
        return
    
    print("🔧 Setting up authenticated client...")
    
    try:
        auth_service = AuthService(guid=BIMPortalConfig.PRIVATE_RESOURCE_GUID)
        client = EnhancedBimPortalClient(
            auth_service=auth_service, 
            base_url=BIMPortalConfig.BASE_URL
        )
        
        # Run project export examples
        run_project_export_examples(client)
        
        print("\n" + "=" * 70)
        print("✅ PROJECT EXPORT EXAMPLES COMPLETE!")
        print("=" * 70)
        print(f"📂 Check the '{BIMPortalConfig.EXPORT_DIRECTORY}' directory for exported files")
        
    except Exception as e:
        logger.error(f"Error running project export examples: {e}")
        print(f"❌ Error running examples: {e}")


if __name__ == "__main__":
    main()
