"""
BIM Portal API - Hackathon Interface

Simple entry point for hackathon participants to learn BIM Portal API usage.
"""

try:
    # When run as part of package (python -m hackathon_example)
    from .setup_hackathon import setup_bim_portal
    from .loin_example import loin_ids_export_example
    from .xml_batch_export import export_loins_xml_batch
except ImportError:
    # When run directly (IDE, python main_example.py)
    from setup_hackathon import setup_bim_portal
    from loin_example import loin_ids_export_example
    from xml_batch_export import export_loins_xml_batch


def run_hackathon_code(client):
    """
    Dedicated function for hackathon participant code.

    Args:
        client: Authenticated BIM Portal client
    """
    print("\n" + "=" * 50)
    print("💡 HACKATHON CODE SECTION")
    print("=" * 50)

    try:
        # Batch XML export of first 10 LOINs from guids_ohne_Doppelten.txt
        export_loins_xml_batch(client, count=6193)

        print("\n✅ Hackathon code completed successfully!")

    except Exception as e:
        print(f"❌ Error in hackathon code: {e}")
        print("💡 Check your API calls and make sure you have proper permissions")


def main():
    """
    Main function for hackathon participants.

    This demonstrates:
    1. How to setup the BIM Portal client
    2. A complete working example (LOIN IDS export)
    3. Where to place your own code

    Returns:
        BIM Portal client for further use
    """
    print("🚀 BIM Portal Hackathon Interface")
    print("=" * 50)

    # Set up the client
    client = setup_bim_portal()
    if not client:
        print("❌ Setup failed - check credentials")
        return None

    # Run the example to show how it works
    print("\n📚 Running example to show you how it works...")
    #loin_ids_export_example(client)

    # Run hackathon code
    run_hackathon_code(client)

    # Provide guidance
    print("\n" + "=" * 50)
    print("🎯 HACKATHON GUIDANCE")
    print("=" * 50)
    print("Edit the 'run_hackathon_code()' function or add more functions above to build your project!")
    print("\nThese are some of the available client methods:")
    print("  • client.search_projects()")
    print("  • client.search_loins()")
    print("  • client.search_properties()")
    print("  • client.export_loin_ids(guid)")
    print("  • client.export_project_pdf(guid)")
    print("\n🚀 Happy hacking!")

    return client


if __name__ == "__main__":
    client = main()

    # Optional: Additional code can go here if needed
    # But main hackathon code should be in run_hackathon_code() function