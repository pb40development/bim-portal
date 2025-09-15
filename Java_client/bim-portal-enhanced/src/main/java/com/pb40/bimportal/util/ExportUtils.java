package com.pb40.bimportal.util;

import com.pb40.bimportal.config.BimPortalConfig;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Optional;
import java.util.UUID;

/**
 * Utility functions for handling file exports from BIM Portal API.
 */
public class ExportUtils {
    
    private static final Logger logger = LoggerFactory.getLogger(ExportUtils.class);
    
    /**
     * Read a file to byte array.
     * @param file File to read
     * @return Optional byte array content
     */
    public static Optional<byte[]> readFileToBytes(File file) {
        if (file == null || !file.exists()) {
            return Optional.empty();
        }
        
        try {
            byte[] content = Files.readAllBytes(file.toPath());
            logger.debug("Read {} bytes from file: {}", content.length, file.getName());
            return Optional.of(content);
        } catch (IOException e) {
            logger.error("Error reading file {}: {}", file.getName(), e.getMessage());
            return Optional.empty();
        }
    }
    
    /**
     * Save byte content to a file in the export directory.
     * @param content Byte content to save
     * @param filename Filename for the export
     * @return Path to saved file or empty if save failed
     */
    public static Optional<Path> saveExportFile(byte[] content, String filename) {
        if (content == null || filename == null || filename.trim().isEmpty()) {
            logger.warn("Cannot save file: content or filename is null/empty");
            return Optional.empty();
        }
        
        try {
            Path filePath = BimPortalConfig.getExportFilePath(filename);
            Files.write(filePath, content);
            logger.info("Exported file: {} ({} bytes)", filePath, content.length);
            return Optional.of(filePath);
        } catch (IOException e) {
            logger.error("Error saving export file {}: {}", filename, e.getMessage());
            return Optional.empty();
        }
    }
    
    /**
     * Save and export project as PDF.
     * @param client Enhanced BIM Portal client
     * @param projectGuid Project GUID
     * @param customFilename Optional custom filename (null for auto-generated)
     * @return Path to saved PDF or empty if export failed
     */
    public static Optional<Path> saveProjectPdf(Object client, UUID projectGuid, String customFilename) {
        // This method would use the client to export and save
        // Implementation depends on the client interface
        String filename = customFilename != null ? customFilename : "project_" + projectGuid + ".pdf";
        
        try {
            // Cast to enhanced client and export
            if (client instanceof com.pb40.bimportal.client.EnhancedBimPortalClient) {
                var enhancedClient = (com.pb40.bimportal.client.EnhancedBimPortalClient) client;
                Optional<byte[]> pdfContent = enhancedClient.exportProjectPdf(projectGuid);
                
                if (pdfContent.isPresent()) {
                    return saveExportFile(pdfContent.get(), filename);
                }
            }
        } catch (Exception e) {
            logger.error("Error saving project PDF: {}", e.getMessage());
        }
        
        return Optional.empty();
    }
    
    /**
     * Generate filename for export based on type and GUID.
     * @param resourceType Type of resource (project, loin, etc.)
     * @param guid Resource GUID
     * @param format Export format (pdf, odt, etc.)
     * @return Generated filename
     */
    public static String generateExportFilename(String resourceType, UUID guid, String format) {
        return String.format("%s_%s.%s", resourceType, guid, format);
    }
    
    /**
     * Get file extension for export format.
     * @param format Export format name
     * @return File extension
     */
    public static String getFileExtension(String format) {
        switch (format.toLowerCase()) {
            case "pdf":
                return "pdf";
            case "openoffice":
            case "odt":
                return "odt";
            case "okstra":
            case "loinxml":
            case "loin-xml":
                return "zip";
            case "ids":
                return "ids";
            case "xml":
                return "xml";
            default:
                return format.toLowerCase();
        }
    }
    
    /**
     * Check if export directory is writable.
     * @return True if directory exists and is writable
     */
    public static boolean isExportDirectoryWritable() {
        try {
            Path exportDir = BimPortalConfig.getExportPath();
            File dir = exportDir.toFile();
            
            if (!dir.exists()) {
                boolean created = dir.mkdirs();
                if (!created) {
                    logger.error("Cannot create export directory: {}", exportDir);
                    return false;
                }
            }
            
            return dir.canWrite();
        } catch (Exception e) {
            logger.error("Error checking export directory: {}", e.getMessage());
            return false;
        }
    }
    
    /**
     * Clean up temporary files older than specified days.
     * @param daysOld Files older than this will be deleted
     * @return Number of files cleaned up
     */
    public static int cleanupOldExports(int daysOld) {
        try {
            Path exportDir = BimPortalConfig.getExportPath();
            if (!Files.exists(exportDir)) {
                return 0;
            }
            
            long cutoffTime = System.currentTimeMillis() - (daysOld * 24L * 60 * 60 * 1000);
            int deletedCount = 0;
            
            File[] files = exportDir.toFile().listFiles();
            if (files != null) {
                for (File file : files) {
                    if (file.isFile() && file.lastModified() < cutoffTime) {
                        if (file.delete()) {
                            deletedCount++;
                            logger.debug("Deleted old export file: {}", file.getName());
                        }
                    }
                }
            }
            
            logger.info("Cleaned up {} old export files", deletedCount);
            return deletedCount;
        } catch (Exception e) {
            logger.error("Error during export cleanup: {}", e.getMessage());
            return 0;
        }
    }
}