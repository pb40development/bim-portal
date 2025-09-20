"""
LOIN IDS export example for hackathon learning.

This shows participants a complete working example they can copy and modify.
"""

import logging
from examples.export_examples.utils.export_utils import ExportUtils

logger = logging.getLogger(__name__)


def loin_ids_export_example(client) -> bool:
    """
    Complete LOIN IDS export example.

    This demonstrates the full workflow that participants can copy:
    1. Search for data
    2. Select an item
    3. Export it
    4. Save the file

    Copy this pattern for your hackathon project!
    """
    print("\n🎯 EXAMPLE: LOIN IDS Export")
    print("📚 Adapted from: examples/export_examples/loin_export_example.py")
    print("-" * 30)

    try:
        # Step 1: Search for LOINs
        print("1. Searching for LOINs...")
        loins = client.search_loins()

        if not loins:
            print("   No LOINs found")
            return False

        print(f"   Found {len(loins)} LOINs")

        # Step 2: Select first LOIN
        selected_loin = loins[0]
        print(f"2. Selected: {selected_loin.name}")

        # Step 3: Export as IDS
        print("3. Exporting as IDS...")
        ids_content = client.export_loin_ids(selected_loin.guid)

        if not ids_content:
            print("   Export failed - no content")
            return False

        # Step 4: Save file
        print("4. Saving file...")
        filename = f"loin_ids_example_export_{selected_loin.guid}"
        file_path = ExportUtils.export_with_detection(ids_content, filename, "ids")

        if file_path:
            print(f"✅ Success! Saved to: {file_path}")
            print(f"   File size: {len(ids_content)} bytes")
            return True
        else:
            print("   Failed to save file")
            return False

    except Exception as e:
        print(f"❌ Example failed: {e}")
        return False
