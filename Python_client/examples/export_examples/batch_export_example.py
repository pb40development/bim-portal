"""
Batch export examples for BIM Portal Python client.

This module demonstrates batch export workflows for multiple projects and LOINs 
in PDF format for efficient bulk processing.
"""

import os
import logging
from pathlib import Path

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


def run_batch_export_examples(client: EnhancedBimPortalClient):
    """
    Run batch export examples for projects and LOINs.
    
    Args:
        client: Enhanced BIM Portal client
    """
    print("\n" + "=" * 60)
    print("📦 BATCH EXPORT EXAMPLES")
    print("=" * 60)
    
    total_exported = 0
    
    print("\n1️⃣ Batch exporting projects as PDF...")
    try:
        projects = client.search_projects()
        if projects:
            project_count = min(3, len(projects))
            for i, project in enumerate(projects[:project_count]):
                print(f"   🚧 Exporting project {i+1}/{project_count}: {project.name}")
                
                pdf_content = client.export_project_pdf(project.guid)
                if pdf_content:
                    filename = f"batch_project_{i+1}_{project.guid}.zip"
                    saved_path = ExportUtils.save_export_file(pdf_content, filename)
                    if saved_path:
                        total_exported += 1
                        print(f"   ✅ Success: {saved_path}")
                    else:
                        print("   ❌ Failed: File save error")
                else:
                    print(f"   ❌ Failed: {project.name}")
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
            for i, loin in enumerate(loins[:loin_count]):
                print(f"   📊 Exporting LOIN {i+1}/{loin_count}: {loin.name}")
                
                pdf_content = client.export_loin_pdf(loin.guid)
                if pdf_content:
                    filename = f"batch_loin_{i+1}_{loin.guid}.zip"
                    saved_path = ExportUtils.save_export_file(pdf_content, filename)
                    if saved_path:
                        total_exported += 1
                        print(f"   ✅ Success: {saved_path}")
                    else:
                        print("   ❌ Failed: File save error")
                else:
                    print(f"   ❌ Failed: {loin.name}")
        else:
            print("🔭 No LOINs available")
            
    except Exception as e:
        logger.error("Error in LOIN batch export", exc_info=True)
        print(f"❌ Error in LOIN batch export: {e}")
    
    print(f"\n📊 BATCH EXPORT COMPLETE: {total_exported} files exported successfully")
    
    # Additional batch operations
    if total_exported > 0:
        print("\n3️⃣ Additional batch operations...")
        
        # Cleanup old exports (demonstration)
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


def run_advanced_batch_operations(client: EnhancedBimPortalClient):
    """
    Demonstrate advanced batch operations with error handling and progress tracking.
    
    Args:
        client: Enhanced BIM Portal client
    """
    print("\n4️⃣ Advanced batch operations with error handling...")
    
    successful_exports = []
    failed_exports = []
    
    try:
        # Get resources for batch processing
        projects = client.search_projects()
        loins = client.search_loins()
        
        # Combine resources for mixed batch processing
        resources = []
        
        # Add up to 2 projects
        for project in projects[:2]:
            resources.append({
                'type': 'project',
                'name': project.name,
                'guid': project.guid,
                'export_func': client.export_project_pdf
            })
        
        # Add up to 2 LOINs
        for loin in loins[:2]:
            resources.append({
                'type': 'loin',
                'name': loin.name,
                'guid': loin.guid,
                'export_func': client.export_loin_pdf
            })
        
        if not resources:
            print("   📭 No resources available for advanced batch processing")
            return
        
        print(f"   🔄 Processing {len(resources)} mixed resources...")
        
        for i, resource in enumerate(resources, 1):
            print(f"   📋 Processing {i}/{len(resources)}: {resource['type']} - {resource['name']}")
            
            try:
                # Export with error handling
                content = resource['export_func'](resource['guid'])
                if content:
                    filename = f"advanced_batch_{resource['type']}_{i}_{resource['guid']}.zip"
                    saved_path = ExportUtils.save_export_file(content, filename)
                    if saved_path:
                        successful_exports.append({
                            'resource': resource,
                            'path': saved_path
                        })
                        print(f"      ✅ Exported: {saved_path.name}")
                    else:
                        failed_exports.append({
                            'resource': resource,
                            'error': 'File save failed'
                        })
                        print("      ❌ File save failed")
                else:
                    failed_exports.append({
                        'resource': resource,
                        'error': 'No content received'
                    })
                    print("      ❌ No content received")
                    
            except Exception as e:
                failed_exports.append({
                    'resource': resource,
                    'error': str(e)
                })
                print(f"      ❌ Export error: {e}")
        
        # Summary report
        print(f"\n   📊 Advanced Batch Summary:")
        print(f"      ✅ Successful: {len(successful_exports)}")
        print(f"      ❌ Failed: {len(failed_exports)}")
        
        if successful_exports:
            print(f"      📁 Successful exports:")
            for export in successful_exports:
                print(f"         - {export['path'].name}")
        
        if failed_exports:
            print(f"      ⚠️ Failed exports:")
            for export in failed_exports:
                print(f"         - {export['resource']['name']}: {export['error']}")
        
    except Exception as e:
        logger.error("Error in advanced batch operations", exc_info=True)
        print(f"   ❌ Error in advanced batch operations: {e}")


def main():
    """Main method to run batch export examples."""
    print("=" * 70)
    print("🚀 BIM PORTAL BATCH EXPORT EXAMPLES")
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
        
        # Run basic batch export examples
        run_batch_export_examples(client)
        
        # Run advanced batch operations
        run_advanced_batch_operations(client)
        
        print("\n" + "=" * 70)
        print("✅ BATCH EXPORT EXAMPLES COMPLETE!")
        print("=" * 70)
        print(f"📂 Check the '{BIMPortalConfig.EXPORT_DIRECTORY}' directory for exported files")
        
    except Exception as e:
        logger.error("Error running batch export examples", exc_info=True)
        print(f"❌ Error running examples: {e}")


if __name__ == "__main__":
    main()
