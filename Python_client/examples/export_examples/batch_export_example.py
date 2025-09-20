"""
Batch export examples for BIM Portal Python client (Refactored).

This module demonstrates batch export workflows for multiple projects and LOINs
in PDF format for efficient bulk processing.
Refactored to use simple common utility functions.
"""
import os
import sys
from pathlib import Path

# Ensure we can import from project root
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

import logging
from examples.export_examples.utils.common_utils import (
    handle_main_example_setup,
    print_example_footer,
    print_section_header,
    export_single_item_batch,
    run_cleanup_operations
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def run_batch_export_examples(client):
    """
    Run batch export examples for projects and LOINs.

    Args:
        client: Enhanced BIM Portal client
    """
    print_section_header("BATCH EXPORT EXAMPLES")

    total_exported = 0

    print("\n1️⃣ Batch exporting projects as PDF...")
    try:
        projects = client.search_projects()
        if projects:
            project_count = min(3, len(projects))
            successful_projects = 0

            for i, project in enumerate(projects[:project_count]):
                success = export_single_item_batch(
                    client, project, "project",
                    client.export_project_pdf, i+1, project_count
                )
                if success:
                    successful_projects += 1

            total_exported += successful_projects
            print(f"   📊 Projects: {successful_projects}/{project_count} exported successfully")
        else:
            print("🔭 No projects available")

    except Exception as e:
        logger.error("Error in project batch export", exc_info=True)
        print(f"❌ Error in project batch export: {e}")

    print("\n2️⃣ Batch exporting LOINs as PDF...")
    try:
        loins = client.search_loins()
        if loins:
            loin_count = min(2, len(loins))
            successful_loins = 0

            for i, loin in enumerate(loins[:loin_count]):
                success = export_single_item_batch(
                    client, loin, "loin",
                    client.export_loin_pdf, i+1, loin_count
                )
                if success:
                    successful_loins += 1

            total_exported += successful_loins
            print(f"   📊 LOINs: {successful_loins}/{loin_count} exported successfully")
        else:
            print("🔭 No LOINs available")

    except Exception as e:
        logger.error("Error in LOIN batch export", exc_info=True)
        print(f"❌ Error in LOIN batch export: {e}")

    print(f"\n📊 BATCH EXPORT COMPLETE: {total_exported} files exported successfully")

    # Additional batch operations
    if total_exported > 0:
        print("\n3️⃣ Additional batch operations...")
        run_cleanup_operations()


def run_advanced_batch_operations(client):
    """
    Demonstrate advanced batch operations with error handling and progress tracking.

    Args:
        client: Enhanced BIM Portal client
    """
    print("\n4️⃣ Advanced batch operations with error handling...")

    successful_exports = 0
    failed_exports = 0

    try:
        # Get resources for batch processing
        projects = client.search_projects()
        loins = client.search_loins()

        # Process up to 2 projects
        project_count = min(2, len(projects))
        print(f"   📄 Processing {project_count} projects...")

        for i, project in enumerate(projects[:project_count]):
            success = export_single_item_batch(
                client, project, "project",
                client.export_project_pdf, i+1, project_count
            )
            if success:
                successful_exports += 1
            else:
                failed_exports += 1

        # Process up to 2 LOINs
        loin_count = min(2, len(loins))
        print(f"   📋 Processing {loin_count} LOINs...")

        for i, loin in enumerate(loins[:loin_count]):
            success = export_single_item_batch(
                client, loin, "loin",
                client.export_loin_pdf, i+1, loin_count
            )
            if success:
                successful_exports += 1
            else:
                failed_exports += 1

        # Print summary
        total_processed = successful_exports + failed_exports
        print(f"\n   📊 Advanced Batch Summary:")
        print(f"      ✅ Successful: {successful_exports}")
        print(f"      ❌ Failed: {failed_exports}")
        print(f"      📈 Total processed: {total_processed}")

    except Exception as e:
        logger.error("Error in advanced batch operations", exc_info=True)
        print(f"   ❌ Error in advanced batch operations: {e}")


def main():
    """Main method to run batch export examples."""
    client = handle_main_example_setup("BATCH")
    if not client:
        return

    try:
        # Run basic batch export examples
        run_batch_export_examples(client)

        # Run advanced batch operations
        run_advanced_batch_operations(client)

        print_example_footer("BATCH")

    except Exception as e:
        logger.error("Error running batch export examples", exc_info=True)
        print(f"❌ Error running examples: {e}")


if __name__ == "__main__":
    main()