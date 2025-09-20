"""
Utility functions for handling file exports from BIM Portal API.
Includes content type detection and file management capabilities.
"""

import os
import zipfile
from pathlib import Path
from typing import Optional
from uuid import UUID
import logging

from client.config import BIMPortalConfig

logger = logging.getLogger(__name__)


class ExportUtils:
    """Utility class for export file handling and content type detection."""
    
    @staticmethod
    def detect_file_extension(content: bytes, default_extension: str) -> str:
        """
        Detect content type from byte array and return appropriate file extension.
        
        Args:
            content: The byte array content
            default_extension: Default extension if detection fails
            
        Returns:
            Detected file extension
        """
        if content is None or len(content) < 4:
            logger.debug(f"Content too small for detection, using default: {default_extension}")
            return default_extension
        
        # Check for PDF signature (%PDF)
        if (len(content) >= 4 and 
            content[0] == 0x25 and content[1] == 0x50 and 
            content[2] == 0x44 and content[3] == 0x46):
            logger.debug("Detected PDF file signature")
            return "pdf"
        
        # Check for ZIP file signature (PK)
        if len(content) >= 2 and content[0] == 0x50 and content[1] == 0x4B:
            # Additional check for OpenDocument format - but be more careful
            try:
                # First check if it's a valid ZIP
                import io
                with zipfile.ZipFile(io.BytesIO(content), 'r') as zip_ref:
                    file_list = zip_ref.namelist()
                    # OpenDocument files have specific structure
                    if 'META-INF/manifest.xml' in file_list and 'content.xml' in file_list:
                        # Double-check by reading the manifest
                        try:
                            manifest_content = zip_ref.read('META-INF/manifest.xml').decode('utf-8')
                            if 'application/vnd.oasis.opendocument' in manifest_content:
                                logger.debug("Detected valid OpenDocument format")
                                return "odt"
                        except:
                            logger.debug("OpenDocument structure present but manifest check failed")
            except zipfile.BadZipFile:
                logger.warning("Content has ZIP signature but is corrupted")
            except Exception as e:
                logger.debug(f"ZIP analysis failed: {e}")

            logger.debug("Detected ZIP file signature")
            return "zip"

        # Check for XML content (IDS files, LOIN-XML are typically XML)
        if len(content) >= 5:
            try:
                start = content[:100].decode('utf-8', errors='ignore').strip()
                if (start.startswith("<?xml") or
                    "<ids" in start or
                    "<loin" in start):
                    logger.debug("Detected XML format")
                    return "xml"
            except UnicodeDecodeError:
                pass

        logger.debug(f"Could not detect file type, using default: {default_extension}")
        return default_extension

    @staticmethod
    def analyze_zip_content(content: bytes) -> Optional[str]:
        """
        Analyze ZIP content to determine the most appropriate extension.

        Args:
            content: ZIP file content as bytes

        Returns:
            Suggested file extension based on ZIP contents
        """
        try:
            # Use BytesIO to avoid permission issues with temporary files
            import io
            with zipfile.ZipFile(io.BytesIO(content), 'r') as zip_ref:
                file_list = zip_ref.namelist()

                # Check for OpenDocument structure
                if any(f in file_list for f in ['META-INF/manifest.xml', 'content.xml', 'styles.xml']):
                    logger.debug("ZIP contains OpenDocument structure")
                    return "odt"

                # Check for OKSTRA content
                if any('.okstra' in f.lower() or 'okstra' in f.lower() for f in file_list):
                    logger.debug("ZIP contains OKSTRA files")
                    return "zip"  # Keep as zip for OKSTRA

                # Check for LOIN-XML content
                if any('.xml' in f.lower() and ('loin' in f.lower() or 'aia' in f.lower()) for f in file_list):
                    logger.debug("ZIP contains LOIN-XML files")
                    return "zip"  # Keep as zip for LOIN-XML

                # Check for PDF files inside ZIP (common case you're experiencing)
                pdf_files = [f for f in file_list if f.lower().endswith('.pdf')]
                if pdf_files:
                    logger.debug(f"ZIP contains {len(pdf_files)} PDF files")
                    return "zip"  # Keep as zip since it contains PDFs

                # Check for ODT files inside ZIP
                odt_files = [f for f in file_list if f.lower().endswith('.odt')]
                if odt_files:
                    logger.debug(f"ZIP contains {len(odt_files)} ODT files")
                    return "zip"  # Keep as zip since it contains ODTs

                # Generic XML content
                xml_files = [f for f in file_list if f.endswith('.xml')]
                if xml_files:
                    logger.debug(f"ZIP contains {len(xml_files)} XML files")
                    return "zip"

                logger.debug("ZIP content analysis inconclusive - keeping as ZIP")
                return "zip"

        except zipfile.BadZipFile:
            logger.warning("Content appears to be ZIP but is corrupted or invalid")
            return "zip"
        except Exception as e:
            logger.warning(f"Error analyzing ZIP content: {e}")
            return "zip"

    @staticmethod
    def export_with_detection(content: bytes, base_filename: str, expected_extension: str) -> Optional[Path]:
        """
        Export content with automatic file type detection and validation.

        Args:
            content: The byte array content
            base_filename: Base filename without extension
            expected_extension: Expected file extension for logging

        Returns:
            Optional path to saved file
        """
        detected_extension = ExportUtils.detect_file_extension(content, expected_extension)

        # Special handling for ZIP files - analyze content for better extension
        if detected_extension == "zip" and expected_extension != "zip":
            analyzed_extension = ExportUtils.analyze_zip_content(content)
            if analyzed_extension and analyzed_extension != "zip":
                detected_extension = analyzed_extension

        filename = f"{base_filename}.{detected_extension}"

        if detected_extension != expected_extension:
            logger.info(
                f"Content type detection: expected '{expected_extension}' but detected '{detected_extension}' for {base_filename}"
            )

        # Validate file integrity before saving
        is_valid, validation_msg = ExportUtils.validate_file_integrity(content, detected_extension)
        if not is_valid:
            logger.warning(f"File validation failed for {base_filename}: {validation_msg}")
            # Still save the file but with a warning prefix
            filename = f"CORRUPTED_{filename}"
        else:
            logger.debug(f"File validation passed: {validation_msg}")

        return ExportUtils.save_export_file(content, filename)

    @staticmethod
    def get_export_summary(export_results: dict) -> tuple[int, int]:
        """
        Get summary statistics for export results.

        Args:
            export_results: Dictionary of format -> path mappings

        Returns:
            Tuple of (successful_exports, total_attempted)
        """
        successful = len([path for path in export_results.values() if path is not None])
        total = len(export_results)
        return successful, total

    @staticmethod
    def save_export_file(content: bytes, filename: str) -> Optional[Path]:
        """
        Save byte content to a file in the export directory.

        Args:
            content: Byte content to save
            filename: Filename for the export

        Returns:
            Path to saved file or None if save failed
        """
        if content is None or not filename or not filename.strip():
            logger.warning("Cannot save file: content or filename is null/empty")
            return None

        try:
            export_dir = Path(BIMPortalConfig.EXPORT_DIRECTORY)
            export_dir.mkdir(exist_ok=True)

            file_path = export_dir / filename
            file_path.write_bytes(content)

            logger.info(f"Exported file: {file_path} ({len(content)} bytes)")
            return file_path

        except Exception as e:
            logger.error(f"Error saving export file {filename}: {e}")
            return None

    @staticmethod
    def generate_export_filename(resource_type: str, guid: UUID, format_name: str) -> str:
        """
        Generate filename for export based on type and GUID.

        Args:
            resource_type: Type of resource (project, loin, etc.)
            guid: Resource GUID
            format_name: Export format (pdf, odt, etc.)

        Returns:
            Generated filename
        """
        extension = ExportUtils.get_file_extension(format_name)
        return f"{resource_type}_{format_name}_{guid}.{extension}"

    @staticmethod
    def get_file_extension(format_name: str) -> str:
        """
        Get file extension for export format.

        Args:
            format_name: Export format name

        Returns:
            File extension
        """
        format_map = {
            "pdf": "pdf",
            "openoffice": "odt",
            "odt": "odt",
            "okstra": "zip",
            "loinxml": "zip",
            "loin-xml": "zip",
            "ids": "ids",
            "xml": "xml"
        }
        return format_map.get(format_name.lower(), format_name.lower())

    @staticmethod
    def is_export_directory_writable() -> bool:
        """
        Check if export directory is writable.

        Returns:
            True if directory exists and is writable
        """
        try:
            export_dir = Path(BIMPortalConfig.EXPORT_DIRECTORY)
            export_dir.mkdir(exist_ok=True)
            return os.access(export_dir, os.W_OK)
        except Exception as e:
            logger.error(f"Error checking export directory: {e}")
            return False

    @staticmethod
    def cleanup_old_exports(days_old: int) -> int:
        """
        Clean up temporary files older than specified days.

        Args:
            days_old: Files older than this will be deleted

        Returns:
            Number of files cleaned up
        """
        try:
            export_dir = Path(BIMPortalConfig.EXPORT_DIRECTORY)
            if not export_dir.exists():
                return 0

            import time
            cutoff_time = time.time() - (days_old * 24 * 60 * 60)
            deleted_count = 0

            for file_path in export_dir.iterdir():
                if file_path.is_file() and file_path.stat().st_mtime < cutoff_time:
                    try:
                        file_path.unlink()
                        deleted_count += 1
                        logger.debug(f"Deleted old export file: {file_path.name}")
                    except Exception as e:
                        logger.warning(f"Could not delete {file_path.name}: {e}")

            logger.info(f"Cleaned up {deleted_count} old export files")
            return deleted_count

        except Exception as e:
            logger.error(f"Error during export cleanup: {e}")
            return 0

    @staticmethod
    def validate_file_integrity(content: bytes, expected_type: str) -> tuple[bool, str]:
        """
        Validate the integrity of exported content.

        Args:
            content: File content as bytes
            expected_type: Expected file type

        Returns:
            Tuple of (is_valid, validation_message)
        """
        if not content or len(content) == 0:
            return False, "Empty content"

        try:
            if expected_type in ['odt', 'zip']:
                # Validate ZIP-based files
                import io
                with zipfile.ZipFile(io.BytesIO(content), 'r') as zip_ref:
                    # Test the ZIP file integrity
                    bad_file = zip_ref.testzip()
                    if bad_file:
                        return False, f"Corrupted file in ZIP: {bad_file}"

                    file_list = zip_ref.namelist()
                    if not file_list:
                        return False, "ZIP file is empty"

                    # Additional validation for ODT files
                    if expected_type == 'odt':
                        required_files = ['META-INF/manifest.xml', 'content.xml']
                        missing_files = [f for f in required_files if f not in file_list]
                        if missing_files:
                            return False, f"ODT missing required files: {missing_files}"

                        # Validate manifest
                        try:
                            manifest = zip_ref.read('META-INF/manifest.xml').decode('utf-8')
                            if 'application/vnd.oasis.opendocument' not in manifest:
                                return False, "Invalid ODT manifest"
                        except Exception as e:
                            return False, f"Cannot read ODT manifest: {e}"

                    return True, f"Valid {expected_type.upper()} file with {len(file_list)} entries"

            elif expected_type == 'pdf':
                # Basic PDF validation
                if not (content.startswith(b'%PDF') and b'%%EOF' in content[-1024:]):
                    return False, "Invalid PDF structure"
                return True, "Valid PDF file"

            elif expected_type == 'xml':
                # Basic XML validation
                try:
                    content.decode('utf-8')
                    content_str = content.decode('utf-8').strip()
                    if not content_str.startswith('<?xml'):
                        return False, "XML file missing XML declaration"
                    return True, "Valid XML file"
                except UnicodeDecodeError:
                    return False, "XML file has encoding issues"

            else:
                return True, f"No validation available for {expected_type}"

        except zipfile.BadZipFile:
            return False, "Corrupted ZIP file"
        except Exception as e:
            return False, f"Validation error: {e}"