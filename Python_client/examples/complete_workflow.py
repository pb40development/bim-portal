"""
Enhanced complete workflow example using the new Enhanced BIM Portal client.
This demonstrates a robust approach that handles API inconsistencies gracefully
and uses advanced export capabilities with content type detection.
"""

import os
import logging
from pathlib import Path
from dotenv import load_dotenv
from uuid import UUID

from auth.auth_service_impl import AuthService
from enhanced_bim_client import EnhancedBimPortalClient
from export_utils import ExportUtils
from models import (
    AiaProjectForPublicRequest,
    PropertyOrGroupForPublicRequest,
    LoinForPublicRequest
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- Configuration ---
load_dotenv()
from config import BIMPortalConfig
BASE_URL = BIMPortalConfig.BASE_URL
AUTH_GUID = BIMPortalConfig.DEFAULT_AUTH_GUID


def setup_client() -> EnhancedBimPortalClient:
    """Sets up the enhanced BIM Portal client with integrated authentication."""
    auth_service = AuthService(guid=AUTH_GUID)
    return EnhancedBimPortalClient(auth_service=auth_service, base_url=BASE_URL)


def run_enhanced_export_workflow(client: EnhancedBimPortalClient):
    """
    Demonstrates enhanced export workflow with content type detection.
    Tests multiple export formats and handles unexpected content types.
    """
    print("--- Enhanced Export Workflow with Content Detection ---")

    # Get available resources for export testing
    print("\nGathering resources for export testing...")

    try:
        projects = client.search_projects()
        loins = client.search_loins()

        export_results = {}

        if projects:
            selected_project = projects[0]
            print(f"Selected project for export testing: '{selected_project.name}'")

            # Test multiple export formats with detection
            export_formats = [
                ('PDF', 'pdf', client.export_project_pdf),
                ('OpenOffice', 'odt', client.export_project_openoffice),
                ('OKSTRA', 'zip', client.export_project_okstra),
                ('LOIN-XML', 'zip', client.export_project_loin_xml),
                ('IDS', 'xml', client.export_project_ids)
            ]

            print(f"\nTesting {len(export_formats)} export formats with content detection...")

            for format_name, expected_ext, export_func in export_formats:
                print(f"  Exporting as {format_name}...")
                try:
                    content = export_func(selected_project.guid)
                    if content:
                        base_filename = f"enhanced_workflow_{format_name.lower()}_{selected_project.guid}"
                        saved_path = ExportUtils.export_with_detection(content, base_filename, expected_ext)

                        if saved_path:
                            actual_ext = saved_path.suffix[1:].upper()
                            detection_note = f" (detected as {actual_ext})" if actual_ext != expected_ext.upper() else ""
                            print(f"    ✅ Success: {saved_path.name}{detection_note}")
                            export_results[format_name] = {
                                'path': saved_path,
                                'expected': expected_ext,
                                'actual': actual_ext.lower(),
                                'size': len(content)
                            }
                        else:
                            print(f"    ❌ Failed to save {format_name}")
                            export_results[format_name] = None
                    else:
                        print(f"    ⚠️ No content received for {format_name}")
                        export_results[format_name] = None

                except Exception as e:
                    print(f"    ❌ Export error for {format_name}: {e}")
                    export_results[format_name] = None

        # Test LOIN exports if available
        if loins:
            selected_loin = loins[0]
            print(f"\nTesting LOIN exports with '{selected_loin.name}'...")

            loin_formats = [
                ('LOIN PDF', 'pdf', client.export_loin_pdf),
                ('LOIN XML', 'xml', client.export_loin_xml),
                ('LOIN IDS', 'xml', client.export_loin_ids)
            ]

            for format_name, expected_ext, export_func in loin_formats:
                print(f"  Exporting {format_name}...")
                try:
                    content = export_func(selected_loin.guid)
                    if content:
                        base_filename = f"enhanced_workflow_{format_name.lower().replace(' ', '_')}_{selected_loin.guid}"
                        saved_path = ExportUtils.export_with_detection(content, base_filename, expected_ext)

                        if saved_path:
                            actual_ext = saved_path.suffix[1:].upper()
                            detection_note = f" (detected as {actual_ext})" if actual_ext != expected_ext.upper() else ""
                            print(f"    ✅ Success: {saved_path.name}{detection_note}")
                            export_results[format_name] = {
                                'path': saved_path,
                                'expected': expected_ext,
                                'actual': actual_ext.lower(),
                                'size': len(content)
                            }
                        else:
                            print(f"    ❌ Failed to save {format_name}")
                    else:
                        print(f"    ⚠️ No content received for {format_name}")

                except Exception as e:
                    print(f"    ❌ Export error for {format_name}: {e}")

        # Export analysis
        print(f"\n--- Export Analysis ---")
        successful_exports = [k for k, v in export_results.items() if v is not None]
        print(f"Successful exports: {len(successful_exports)}/{len(export_results)}")

        # Content type analysis
        type_mismatches = []
        for format_name, result in export_results.items():
            if result and result['expected'] != result['actual']:
                type_mismatches.append({
                    'format': format_name,
                    'expected': result['expected'],
                    'actual': result['actual']
                })

        if type_mismatches:
            print(f"\nContent type detection findings:")
            for mismatch in type_mismatches:
                print(f"  📋 {mismatch['format']}: Expected {mismatch['expected'].upper()}, got {mismatch['actual'].upper()}")
            print(f"  💡 Content detection prevented {len(type_mismatches)} incorrect file extensions")
        else:
            print(f"\n✅ All exports matched expected content types")

        # File size analysis
        if successful_exports:
            sizes = [export_results[fmt]['size'] for fmt in successful_exports if export_results[fmt]]
            if sizes:
                print(f"\nFile size analysis:")
                print(f"  Smallest export: {min(sizes):,} bytes")
                print(f"  Largest export: {max(sizes):,} bytes")
                print(f"  Average size: {sum(sizes)//len(sizes):,} bytes")

    except Exception as e:
        logger.error("Error in enhanced export workflow", exc_info=True)
        print(f"❌ Enhanced export workflow failed: {e}")


def run_complete_workflow(client: EnhancedBimPortalClient):
    """
    Demonstrates a complete, end-to-end workflow using Pydantic models.
    This workflow finds a project, inspects its properties, and exports it with detection.
    """
    print("--- Running Complete End-to-End Workflow with Pydantic Models ---")

    # --- Step 1: Find a project to work with ---
    print("\nStep 1: Searching for projects...")
    try:
        search_request = AiaProjectForPublicRequest()  # Empty request for all public projects
        projects = client.search_projects(search_request)

        if not projects:
            print("❌ Workflow failed: No projects found.")
            return

        project_to_process = projects[0]
        print(f"✅ Found {len(projects)} projects. Using: '{project_to_process.name}' ({project_to_process.guid})")
    except Exception as e:
        print(f"❌ Error in Step 1: {e}")
        return

    # --- Step 2: Get the full details of the project ---
    print(f"\nStep 2: Fetching full details for project '{project_to_process.name}'...")
    try:
        project_details = client.get_project(project_to_process.guid)

        if project_details:
            print("✅ Successfully fetched project details using Pydantic models.")
            print(f"  - Name: {project_details.name}")
            print(f"  - Description: {project_details.description}")
            print(f"  - Version: {project_details.versionNumber}")
            print(f"  - Organisation: {project_details.organisationName}")
            print(f"  - Template Type: {project_details.templateType}")

            # Show coordinate system if available
            if project_details.coordinateSystem:
                coord = project_details.coordinateSystem
                print(f"  - Coordinate System: {coord.name} (Zone: {coord.zone})")

            # Show models if available
            if project_details.models:
                print(f"  - Models: {len(project_details.models)} available")
                for model in project_details.models[:3]:  # Show first 3
                    print(f"    * {model.name} ({model.guid})")

            # Show data formats if available
            if project_details.dataFormats:
                print(f"  - Data Formats: {len(project_details.dataFormats)} available")
        else:
            print("❌ Could not fetch project details.")
    except Exception as e:
        print(f"❌ Error in Step 2: {e}")

    # --- Step 3: Find relevant properties ---
    print("\nStep 3: Searching for properties...")
    try:
        property_search = PropertyOrGroupForPublicRequest()
        properties = client.search_properties(property_search)

        if properties:
            print(f"✅ Found {len(properties)} properties using Pydantic models.")
            for prop in properties[:5]:  # Show first 5
                category_str = prop.category.value if prop.category else "None"
                print(f"  - Property: {prop.name} (Category: {category_str})")
                if prop.dataType:
                    print(f"    Data Type: {prop.dataType}")
                if prop.units:
                    print(f"    Units: {', '.join(prop.units[:3])}")  # First 3 units
        else:
            print("ℹ️ No properties found.")
    except Exception as e:
        print(f"❌ Error in Step 3: {e}")

    # --- Step 4: Get details of a specific property ---
    print("\nStep 4: Getting detailed property information...")
    try:
        if properties and len(properties) > 0:
            first_property = properties[0]
            if first_property.guid:
                property_details = client.get_property(first_property.guid)

                if property_details:
                    # PropertyDto stores names in namesInLanguage array, not direct name field
                    property_name = first_property.name  # Use name from search results
                    if property_details.namesInLanguage and len(property_details.namesInLanguage) > 0:
                        property_name = property_details.namesInLanguage[0].name

                    print(f"✅ Successfully fetched details for property: {property_name}")
                    print(f"  - GUID: {property_details.guid}")
                    print(f"  - Data Type: {property_details.dataType}")
                    print(f"  - Organisation: {property_details.organisationName}")

                    if property_details.dimension:
                        print(f"  - Dimension: {property_details.dimension}")

                    if property_details.namesInLanguage:
                        print(f"  - Available names: {len(property_details.namesInLanguage)}")
                        for name_info in property_details.namesInLanguage[:2]:  # Show first 2
                            print(f"    * {name_info.name} ({name_info.language})")

                    if property_details.units:
                        print(f"  - Units: {', '.join(property_details.units[:3])}")

                    if property_details.definitionsInLanguage:
                        print(f"  - Definitions available: {len(property_details.definitionsInLanguage)}")
                        for def_info in property_details.definitionsInLanguage[:1]:  # Show first definition
                            if def_info.definition:
                                print(f"    * {def_info.definition[:100]}..." if len(def_info.definition) > 100 else f"    * {def_info.definition}")
                else:
                    print("❌ Could not fetch property details.")
            else:
                print("ℹ️ Skipping property details - no GUID available.")
        else:
            print("ℹ️ Skipping property details - no properties to examine.")
    except Exception as e:
        print(f"❌ Error in Step 4: {e}")

    # --- Step 5: Enhanced export with content detection ---
    print(f"\nStep 5: Enhanced export of project '{project_to_process.name}' with content detection...")
    try:
        # Export project in multiple formats using content detection
        export_formats = [
            ('PDF', 'pdf', client.export_project_pdf),
            ('OpenOffice', 'odt', client.export_project_openoffice)
        ]

        successful_exports = []

        for format_name, expected_ext, export_func in export_formats:
            print(f"  Exporting as {format_name}...")
            try:
                content = export_func(project_to_process.guid)

                if content:
                    base_filename = f"complete_workflow_{format_name.lower()}_{project_to_process.guid}"
                    saved_path = ExportUtils.export_with_detection(content, base_filename, expected_ext)

                    if saved_path:
                        actual_ext = saved_path.suffix[1:].upper()
                        detection_note = f" (detected as {actual_ext})" if actual_ext != expected_ext.upper() else ""
                        print(f"    ✅ Successfully exported to {saved_path}{detection_note}")
                        successful_exports.append({
                            'format': format_name,
                            'path': saved_path,
                            'expected': expected_ext,
                            'actual': actual_ext.lower(),
                            'size': len(content)
                        })
                    else:
                        print(f"    ❌ Failed to save {format_name} export")
                else:
                    print(f"    ⚠️ Could not export project as {format_name}")

            except Exception as export_error:
                print(f"    ❌ Export error for {format_name}: {export_error}")

        # Export summary
        if successful_exports:
            print(f"\n📊 Export Summary:")
            print(f"  Successfully exported {len(successful_exports)} formats")
            for export in successful_exports:
                size_kb = export['size'] // 1024
                print(f"    • {export['format']}: {export['path'].name} ({size_kb} KB)")

                # Highlight content type detection
                if export['expected'] != export['actual']:
                    print(f"      🔍 Content detection: Expected {export['expected'].upper()}, detected {export['actual'].upper()}")
        else:
            print("❌ No exports were successful")

    except Exception as e:
        print(f"❌ Error in Step 5: {e}")

    print("\n--- Workflow completed ---")
    print("\n=== ENHANCED CLIENT BENEFITS DEMONSTRATED ===")
    print("- Integrated authentication handling with retry logic")
    print("- Graceful handling of null values in API responses")
    print("- Type-safe access to all fields")
    print("- Advanced export with automatic content type detection")
    print("- Robust error handling for unexpected content formats")
    print("- Clean, readable code with proper file management")


def demonstrate_advanced_content_detection(client: EnhancedBimPortalClient):
    """Demonstrate advanced content detection capabilities."""
    print("\n=== DEMONSTRATING ADVANCED CONTENT DETECTION ===")

    try:
        # Get a project for testing
        projects = client.search_projects()
        if not projects:
            print("No projects available for content detection demo")
            return

        test_project = projects[0]
        print(f"Testing content detection with project: {test_project.name}")

        # Test different export types to see content detection in action
        detection_tests = [
            ('OKSTRA', client.export_project_okstra, 'zip'),
            ('PDF', client.export_project_pdf, 'pdf'),
        ]

        for test_name, export_func, expected_type in detection_tests:
            try:
                print(f"\n  Testing {test_name} export content detection...")
                content = export_func(test_project.guid)

                if content:
                    # Use the detection utilities directly
                    detected_type = ExportUtils.detect_file_extension(content, expected_type)

                    print(f"    Expected type: {expected_type}")
                    print(f"    Detected type: {detected_type}")

                    if detected_type != expected_type:
                        print(f"    🔍 Content mismatch detected and handled!")

                        # If it's a ZIP, analyze contents
                        if detected_type == 'zip':
                            analyzed_type = ExportUtils.analyze_zip_content(content)
                            if analyzed_type:
                                print(f"    📦 ZIP analysis result: {analyzed_type}")
                    else:
                        print(f"    ✅ Content type matches expectation")

                    # Save with detection
                    base_filename = f"detection_test_{test_name.lower()}_{test_project.guid}"
                    saved_path = ExportUtils.export_with_detection(content, base_filename, expected_type)
                    if saved_path:
                        print(f"    💾 Saved as: {saved_path.name}")
                else:
                    print(f"    ⚠️ No content received for {test_name}")

            except Exception as e:
                print(f"    ❌ Error testing {test_name}: {e}")

    except Exception as e:
        logger.error("Error in content detection demo", exc_info=True)
        print(f"❌ Content detection demo failed: {e}")


def demonstrate_error_handling(client: EnhancedBimPortalClient):
    """Demonstrate how Pydantic handles malformed data gracefully."""
    print("\n=== DEMONSTRATING ERROR HANDLING ===")

    # Try to get a non-existent project
    fake_guid = UUID('00000000-0000-0000-0000-000000000000')
    result = client.get_project(fake_guid)
    print(f"Non-existent project result: {result}")


if __name__ == "__main__":
    if not os.getenv("BIM_PORTAL_USERNAME"):
        print("⚠️ Credentials not found. The workflow may fail if it encounters private resources.")

    client = setup_client()

    # Check export directory
    if not ExportUtils.is_export_directory_writable():
        print("❌ Export directory is not writable! Some features may not work.")

    # Run workflows
    run_complete_workflow(client)
    run_enhanced_export_workflow(client)
    demonstrate_advanced_content_detection(client)
    demonstrate_error_handling(client)

    print(f"\n📂 Check the '{BIMPortalConfig.EXPORT_DIRECTORY}' directory for all exported files")