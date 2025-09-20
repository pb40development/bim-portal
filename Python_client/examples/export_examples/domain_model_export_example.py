"""
Domain-specific model export examples for BIM Portal Python client.

This module demonstrates domain-specific model export workflows in multiple formats including
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
from examples.export_examples.utils.common_utils import check_credentials
from examples.export_examples.utils.export_utils import ExportUtils

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()



def run_domain_model_export_examples(client: EnhancedBimPortalClient):
    """
    Run domain-specific model export examples with comprehensive format support.

    Args:
        client: Enhanced BIM Portal client
    """
    print("\n" + "=" * 60)
    print("🗂️  DOMAIN MODEL EXPORT EXAMPLES")
    print("=" * 60)

    print("\n1️⃣ Searching for available domain models...")
    try:
        domain_models = client.search_domain_models()
        if not domain_models:
            print("🔭 No domain models found for export")
            return

        print(f"✅ Found {len(domain_models)} domain models:")
        for i, model in enumerate(domain_models[:3], 1):
            print(f"   {i}. {model.name} ({model.guid})")

        selected_model = domain_models[0]
        print(f"\n🎯 Using domain model: '{selected_model.name}'")

        export_results: Dict[str, Optional[Path]] = {}

        print("\n2️⃣ Exporting domain model in multiple formats...")

        # PDF Export with auto-detection
        print("   📄 Exporting as PDF...")
        pdf_content = client.export_domain_model_pdf(selected_model.guid)
        if pdf_content:
            base_filename = f"domain_model_pdf_{selected_model.guid}"
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
        odt_content = client.export_domain_model_openoffice(selected_model.guid)
        if odt_content:
            base_filename = f"domain_model_odt_{selected_model.guid}"
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
        okstra_content = client.export_domain_model_okstra(selected_model.guid)
        if okstra_content:
            base_filename = f"domain_model_okstra_{selected_model.guid}"
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
        loin_xml_content = client.export_domain_model_loin_xml(selected_model.guid)
        if loin_xml_content:
            base_filename = f"domain_model_loin_{selected_model.guid}"
            xml_path = ExportUtils.export_with_detection(loin_xml_content, base_filename, "zip")
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
        ids_content = client.export_domain_model_ids(selected_model.guid)
        if ids_content:
            base_filename = f"domain_model_ids_{selected_model.guid}"
            ids_path = ExportUtils.export_with_detection(ids_content, base_filename, "xml")
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

        # Additional domain model details
        print(f"\n📋 Domain Model Details:")
        try:
            detailed_model = client.get_domain_model(selected_model.guid)
            if detailed_model:
                print(f"   Name: {detailed_model.name}")
                print(f"   GUID: {detailed_model.guid}")
                if hasattr(detailed_model, 'description') and detailed_model.description:
                    print(f"   Description: {detailed_model.description}")
                if hasattr(detailed_model, 'version') and detailed_model.version:
                    print(f"   Version: {detailed_model.version}")
                if hasattr(detailed_model, 'discipline') and detailed_model.discipline:
                    print(f"   Discipline: {detailed_model.discipline}")
            else:
                print("   Could not retrieve detailed information")
        except Exception as e:
            print(f"   Error retrieving details: {e}")

    except Exception as e:
        logger.error(f"Error in domain model export examples: {e}")
        print(f"❌ Error in domain model export examples: {e}")


def main():
    """Main method to run domain model export examples."""
    print("=" * 70)
    print("🚀 BIM PORTAL DOMAIN MODEL EXPORT EXAMPLES")
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

        # Run domain model export examples
        run_domain_model_export_examples(client)

        print("\n" + "=" * 70)
        print("✅ DOMAIN MODEL EXPORT EXAMPLES COMPLETE!")
        print("=" * 70)
        print(f"📂 Check the '{BIMPortalConfig.EXPORT_DIRECTORY}' directory for exported files")
        
    except Exception as e:
        logger.error(f"Error running domain model export examples: {e}")
        print(f"❌ Error running examples: {e}")


if __name__ == "__main__":
    main()