"""
Common utility functions for BIM Portal export examples.

This module centralizes common functionality used across all export examples
including credential validation, client setup, and shared operations.
Simple functions that can be easily copied and understood by beginners.
"""

import os
import logging
from pathlib import Path
from typing import Optional, Dict, List, Any

from dotenv import load_dotenv

from client.auth.auth_config import BIM_PORTAL_PASSWORD_ENV_VAR, BIM_PORTAL_USERNAME_ENV_VAR
from client.auth.auth_service_impl import AuthService
from client.enhanced_bim_client import EnhancedBimPortalClient
from client.config import BIMPortalConfig
from examples.export_examples.utils.export_utils import ExportUtils

# Configure logging
logger = logging.getLogger(__name__)

# Load environment variables once
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


def check_export_directory() -> bool:
    """
    Check if export directory is writable.

    Returns:
        True if directory is writable
    """
    if not ExportUtils.is_export_directory_writable():
        print("❌ Export directory is not writable!")
        return False
    return True


def setup_client() -> EnhancedBimPortalClient:
    """
    Setup and return authenticated BIM Portal client.

    Returns:
        Configured BIM Portal client
    """
    auth_service = AuthService()
    return EnhancedBimPortalClient(
        auth_service=auth_service,
        base_url=BIMPortalConfig.BASE_URL
    )


def print_example_header(example_name: str) -> None:
    """
    Print header for export examples.

    Args:
        example_name: Name of the example
    """
    print("=" * 70)
    print(f"🚀 BIM PORTAL {example_name.upper()} EXPORT EXAMPLES")
    print("=" * 70)


def print_example_footer(example_name: str) -> None:
    """
    Print footer for export examples.

    Args:
        example_name: Name of the example
    """
    print(f"\n{'=' * 70}")
    print(f"✅ {example_name.upper()} EXPORT EXAMPLES COMPLETE!")
    print("=" * 70)
    print(f"📂 Check the '{BIMPortalConfig.EXPORT_DIRECTORY}' directory for exported files")


def print_section_header(title: str) -> None:
    """
    Print a formatted section header.

    Args:
        title: Section title
    """
    print(f"\n{'=' * 60}")
    print(f"📋 {title}")
    print("=" * 60)


def print_search_results(items: List[Any], item_type: str, max_display: int = 5) -> Optional[Any]:
    """
    Print search results and return the first item for processing.

    Args:
        items: List of items found
        item_type: Type of items (for display)
        max_display: Maximum number of items to display

    Returns:
        First item if available, None otherwise
    """
    if not items:
        print(f"🔭 No {item_type} found for export")
        return None

    print(f"✅ Found {len(items)} {item_type}:")
    for i, item in enumerate(items[:max_display], 1):
        print(f"   {i}. {item.name} ({item.guid})")

    if len(items) > max_display:
        print(f"   ... and {len(items) - max_display} more")

    selected_item = items[0]
    print(f"\n🎯 Using {item_type.rstrip('s')}: '{selected_item.name}'")
    return selected_item


def export_pdf(client: EnhancedBimPortalClient, export_function, guid: str, base_filename: str) -> Optional[Path]:
    """
    Export PDF format with error handling.

    Args:
        client: BIM Portal client
        export_function: Function to call for PDF export
        guid: Resource GUID
        base_filename: Base filename for export

    Returns:
        Path to exported file or None if failed
    """
    print("   📄 Exporting as PDF...")
    try:
        pdf_content = export_function(guid)
        if pdf_content:
            filename = f"{base_filename}_{guid}"
            pdf_path = ExportUtils.export_with_detection(pdf_content, filename, "pdf")
            if pdf_path:
                print(f"   ✅ PDF exported: {pdf_path}")
                return pdf_path
            else:
                print("   ❌ PDF export failed: Could not save file")
                return None
        else:
            print("   ❌ PDF export failed: No content received")
            return None
    except Exception as e:
        print(f"   ❌ PDF export failed: {e}")
        return None


def export_openoffice(client: EnhancedBimPortalClient, export_function, guid: str, base_filename: str) -> Optional[
    Path]:
    """
    Export OpenOffice format with error handling.

    Args:
        client: BIM Portal client
        export_function: Function to call for OpenOffice export
        guid: Resource GUID
        base_filename: Base filename for export

    Returns:
        Path to exported file or None if failed
    """
    print("   📝 Exporting as OpenOffice...")
    try:
        odt_content = export_function(guid)
        if odt_content:
            filename = f"{base_filename}_{guid}"
            odt_path = ExportUtils.export_with_detection(odt_content, filename, "odt")
            if odt_path:
                print(f"   ✅ OpenOffice exported: {odt_path}")
                return odt_path
            else:
                print("   ❌ OpenOffice export failed: Could not save file")
                return None
        else:
            print("   ❌ OpenOffice export failed: No content received")
            return None
    except Exception as e:
        print(f"   ❌ OpenOffice export failed: {e}")
        return None


def export_okstra(client: EnhancedBimPortalClient, export_function, guid: str, base_filename: str) -> Optional[Path]:
    """
    Export OKSTRA format with error handling.

    Args:
        client: BIM Portal client
        export_function: Function to call for OKSTRA export
        guid: Resource GUID
        base_filename: Base filename for export

    Returns:
        Path to exported file or None if failed
    """
    print("   🗂️ Exporting as OKSTRA...")
    try:
        okstra_content = export_function(guid)
        if okstra_content:
            filename = f"{base_filename}_{guid}"
            okstra_path = ExportUtils.export_with_detection(okstra_content, filename, "zip")
            if okstra_path:
                print(f"   ✅ OKSTRA exported: {okstra_path}")
                return okstra_path
            else:
                print("   ❌ OKSTRA export failed: Could not save file")
                return None
        else:
            print("   ❌ OKSTRA export failed: No content received")
            return None
    except Exception as e:
        print(f"   ❌ OKSTRA export failed: {e}")
        return None


def export_loin_xml(client: EnhancedBimPortalClient, export_function, guid: str, base_filename: str) -> Optional[Path]:
    """
    Export LOIN-XML format with error handling.

    Args:
        client: BIM Portal client
        export_function: Function to call for LOIN-XML export
        guid: Resource GUID
        base_filename: Base filename for export

    Returns:
        Path to exported file or None if failed
    """
    print("   🔗 Exporting as LOIN-XML...")
    try:
        loin_xml_content = export_function(guid)
        if loin_xml_content:
            filename = f"{base_filename}_{guid}"
            xml_path = ExportUtils.export_with_detection(loin_xml_content, filename, "zip")
            if xml_path:
                print(f"   ✅ LOIN-XML exported: {xml_path}")
                return xml_path
            else:
                print("   ❌ LOIN-XML export failed: Could not save file")
                return None
        else:
            print("   ❌ LOIN-XML export failed: No content received")
            return None
    except Exception as e:
        print(f"   ❌ LOIN-XML export failed: {e}")
        return None


def export_ids(client: EnhancedBimPortalClient, export_function, guid: str, base_filename: str) -> Optional[Path]:
    """
    Export IDS format with error handling.

    Args:
        client: BIM Portal client
        export_function: Function to call for IDS export
        guid: Resource GUID
        base_filename: Base filename for export

    Returns:
        Path to exported file or None if failed
    """
    print("   🆔 Exporting as IDS...")
    try:
        ids_content = export_function(guid)
        if ids_content:
            filename = f"{base_filename}_{guid}"
            ids_path = ExportUtils.export_with_detection(ids_content, filename, "xml")
            if ids_path:
                print(f"   ✅ IDS exported: {ids_path}")
                return ids_path
            else:
                print("   ❌ IDS export failed: Could not save file")
                return None
        else:
            print("   ❌ IDS export failed: No content received")
            return None
    except Exception as e:
        print(f"   ❌ IDS export failed: {e}")
        return None


def print_export_summary(export_results: Dict[str, Optional[Path]]) -> None:
    """
    Print a summary of export results.

    Args:
        export_results: Dictionary of format -> path mappings
    """
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


def print_resource_details(detailed_resource: Any, resource_type: str) -> None:
    """
    Print detailed information about a resource.

    Args:
        detailed_resource: The detailed resource object
        resource_type: Type of resource
    """
    print(f"\n📋 {resource_type} Details:")
    if detailed_resource:
        print(f"   Name: {detailed_resource.name}")
        print(f"   GUID: {detailed_resource.guid}")

        # Print optional attributes if they exist
        if hasattr(detailed_resource, 'description') and detailed_resource.description:
            print(f"   Description: {detailed_resource.description}")
        if hasattr(detailed_resource, 'version') and detailed_resource.version:
            print(f"   Version: {detailed_resource.version}")
        if hasattr(detailed_resource, 'discipline') and detailed_resource.discipline:
            print(f"   Discipline: {detailed_resource.discipline}")
        if hasattr(detailed_resource, 'status') and detailed_resource.status:
            print(f"   Status: {detailed_resource.status}")
        if hasattr(detailed_resource, 'context_type') and detailed_resource.context_type:
            print(f"   Type: {detailed_resource.context_type}")
    else:
        print("   Could not retrieve detailed information")


def export_single_item_batch(client: EnhancedBimPortalClient, item, item_type: str,
                             export_function, index: int, total: int) -> bool:
    """
    Export a single item in batch processing.

    Args:
        client: BIM Portal client
        item: Item to export
        item_type: Type of item
        export_function: Function to call for export
        index: Current item index
        total: Total number of items

    Returns:
        True if export was successful
    """
    print(f"   📋 Exporting {item_type} {index}/{total}: {item.name}")

    try:
        content = export_function(item.guid)
        if content:
            filename = f"batch_{item_type}_{index}_{item.guid}.zip"
            saved_path = ExportUtils.save_export_file(content, filename)
            if saved_path:
                print(f"   ✅ Success: {saved_path}")
                return True
            else:
                print("   ❌ Failed: File save error")
                return False
        else:
            print(f"   ❌ Failed: {item.name}")
            return False
    except Exception as e:
        logger.error(f"Error in batch export for {item.name}: {e}")
        print(f"   ❌ Failed: {item.name} - {e}")
        return False


def run_cleanup_operations() -> None:
    """Run cleanup operations on old export files."""
    print("   🧹 Cleaning up old exports (demo - files older than 30 days)...")
    try:
        cleaned_files = ExportUtils.cleanup_old_exports(30)
        print(f"   ✅ Cleaned up {cleaned_files} old export files")
    except Exception as e:
        print(f"   ⚠️ Cleanup warning: {e}")

    # Export summary
    export_dir = Path(BIMPortalConfig.EXPORT_DIRECTORY)
    if export_dir.exists():
        export_files = list(export_dir.glob("batch_*"))
        print(f"   📁 Total batch export files in directory: {len(export_files)}")


def handle_main_example_setup(example_name: str) -> Optional[EnhancedBimPortalClient]:
    """
    Handle the common setup for main example functions.

    Args:
        example_name: Name of the example

    Returns:
        Configured client or None if setup failed
    """
    print_example_header(example_name)

    if not check_credentials():
        print("❌ Cannot run export examples without credentials")
        return None

    if not check_export_directory():
        return None

    print("🔧 Setting up authenticated client...")

    try:
        return setup_client()
    except Exception as e:
        logger.error(f"Error setting up client: {e}")
        print(f"❌ Error setting up client: {e}")
        return None