"""
Batch XML export example for LOINs.

This demonstrates how to export multiple LOINs in XML format with timing.
"""

import time
import logging
from pathlib import Path
from uuid import UUID
from datetime import datetime
from examples.export_examples.utils.export_utils import ExportUtils
from client.config import BIMPortalConfig

logger = logging.getLogger(__name__)


def export_loins_xml_batch(client, guid_file: str = "guids_ohne_Doppelten.txt", count: int = 10) -> dict:
    """
    Export LOINs in XML format from a list of GUIDs.

    This function reads GUIDs from a file, exports each as XML, and measures performance.

    Args:
        client: Authenticated BIM Portal client
        guid_file: Path to file containing GUIDs (one per line)
        count: Number of GUIDs to export (default: 10)

    Returns:
        dict: Export statistics including timing and success rate
    """
    print("\n" + "=" * 60)
    print(f"🚀 BATCH XML EXPORT - Processing first {count} LOINs")
    print("=" * 60)

    results = {
        'total': 0,
        'successful': 0,
        'failed': 0,
        'total_time': 0,
        'files': [],
        'failed_guids': []
    }

    try:
        # Read GUIDs from file
        print(f"📂 Reading GUIDs from: {guid_file}")
        guid_path = Path(guid_file)

        if not guid_path.exists():
            print(f"❌ Error: File not found: {guid_file}")
            return results

        with open(guid_path, 'r') as f:
            guids = [line.strip() for line in f if line.strip()][:count]

        if not guids:
            print("❌ No GUIDs found in file")
            return results

        print(f"✅ Found {len(guids)} GUIDs to export")
        print("-" * 60)

        # Start timing
        start_time = time.time()

        # Export each LOIN
        for i, guid_str in enumerate(guids, 1):
            try:
                guid = UUID(guid_str)
                results['total'] += 1

                print(f"\n[{i}/{count}] Exporting LOIN: {guid}")

                # Export as XML
                export_start = time.time()
                xml_content = client.export_loin_xml(guid)
                export_time = time.time() - export_start

                if not xml_content:
                    print(f"  ❌ Export failed - no content returned")
                    results['failed'] += 1
                    results['failed_guids'].append(guid_str)
                    continue

                # Save the file
                filename = f"loin_xml_export_{guid}"
                file_path = ExportUtils.export_with_detection(xml_content, filename, "xml")

                if file_path:
                    print(f"  ✅ Success! Saved to: {file_path.name}")
                    print(f"  📊 Size: {len(xml_content):,} bytes | Time: {export_time:.2f}s")
                    results['successful'] += 1
                    results['files'].append(str(file_path))
                else:
                    print(f"  ❌ Failed to save file")
                    results['failed'] += 1
                    results['failed_guids'].append(guid_str)

            except ValueError as e:
                print(f"  ❌ Invalid GUID format: {guid_str}")
                results['failed'] += 1
                results['failed_guids'].append(guid_str)
            except Exception as e:
                print(f"  ❌ Error exporting GUID {guid_str}: {e}")
                results['failed'] += 1
                results['failed_guids'].append(guid_str)

        # Calculate total time
        results['total_time'] = time.time() - start_time

        # Print summary
        print("\n" + "=" * 60)
        print("📊 EXPORT SUMMARY")
        print("=" * 60)
        print(f"Total GUIDs processed: {results['total']}")
        print(f"✅ Successful exports: {results['successful']}")
        print(f"❌ Failed exports: {results['failed']}")
        print(f"⏱️  Total time: {results['total_time']:.2f} seconds")

        if results['successful'] > 0:
            avg_time = results['total_time'] / results['successful']
            print(f"📈 Average time per export: {avg_time:.2f} seconds")
            print(f"🚀 Throughput: {results['successful'] / results['total_time']:.2f} exports/second")

        print("=" * 60)

        # Write failed GUIDs to file if there are any
        if results['failed_guids']:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            failed_file = Path(BIMPortalConfig.EXPORT_DIRECTORY) / f"failed_exports_{timestamp}.txt"

            try:
                with open(failed_file, 'w') as f:
                    f.write("# Failed LOIN Export GUIDs\n")
                    f.write(f"# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                    f.write(f"# Total failed: {len(results['failed_guids'])}\n")
                    f.write("#" + "-" * 50 + "\n")
                    for guid in results['failed_guids']:
                        f.write(f"{guid}\n")

                print(f"\n📝 Failed GUIDs saved to: {failed_file}")
                print(f"   ({len(results['failed_guids'])} GUIDs)")
            except Exception as e:
                print(f"\n⚠️  Warning: Could not save failed GUIDs file: {e}")
                logger.error(f"Failed to write failed GUIDs file: {e}")

        return results

    except Exception as e:
        print(f"❌ Fatal error during batch export: {e}")
        logger.exception("Batch export failed")
        return results
