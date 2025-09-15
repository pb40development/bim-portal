package com.pb40.bimportal.examples;

import com.pb40.bimportal.client.BimPortalClientBuilder;
import com.pb40.bimportal.client.EnhancedBimPortalClient;
import com.pb40.bimportal.config.BimPortalConfig;
import com.bimportal.client.model.SimpleAiaProjectPublicDto;
import com.bimportal.client.model.PropertyOrGroupForPublicDto;
import com.bimportal.client.model.SimpleLoinPublicDto;
import com.pb40.bimportal.util.ExportUtils;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.nio.file.Path;
import java.util.List;
import java.util.Optional;

/**
 * Quick start example for BIM Portal Java client.
 * 
 * This class demonstrates basic usage of the BIM Portal API client
 * for hackathon participants and developers getting started.
 */
public class QuickStart {
    
    private static final Logger logger = LoggerFactory.getLogger(QuickStart.class);
    
    /**
     * Quick start function that sets up the BIM Portal client and shows basic usage.
     * @return Configured client or null if setup failed
     */
    public static EnhancedBimPortalClient quickStart() {
        System.out.println("Setting up BIM Portal connection...");
        
        try {
            // Create client using builder pattern
            EnhancedBimPortalClient client = BimPortalClientBuilder.buildDefault();
            
            // Perform health check
            EnhancedBimPortalClient.HealthCheckResult healthCheck = client.performHealthCheck();
            
            if (!healthCheck.isApiAccessible()) {
                System.err.println("API connection failed: " + healthCheck.getStatusMessage());
                return null;
            }
            
            // Get basic statistics
            EnhancedBimPortalClient.ApiStats stats = client.getApiStats();
            
            if (healthCheck.isAuthWorking()) {
                System.out.println("============================================================");
                System.out.println("CONNECTED TO BIM PORTAL WITH FULL AUTHENTICATION!");
                System.out.println("============================================================");
                System.out.println("Available projects: " + stats.getProjectCount());
                System.out.println("Available properties: " + stats.getPropertyCount());
                System.out.println("Available LOINs: " + stats.getLoinCount());
                System.out.println("Available domain models: " + stats.getDomainModelCount());
                System.out.println("Exports will be saved to: " + BimPortalConfig.getExportPath());
                System.out.println("\nREADY FOR DEVELOPMENT! Use the client to interact with the API.");
                System.out.println("============================================================");
            } else {
                System.out.println("============================================================");
                System.out.println("CONNECTED TO BIM PORTAL WITH LIMITED ACCESS");
                System.out.println("============================================================");
                System.out.println("Available projects: " + stats.getProjectCount() + " (public only)");
                System.out.println("Available properties: " + stats.getPropertyCount() + " (public only)");
                System.out.println("Available LOINs: " + stats.getLoinCount() + " (public only)");
                System.out.println("Available domain models: " + stats.getDomainModelCount() + " (public only)");
                System.out.println("Exports will be saved to: " + BimPortalConfig.getExportPath());
                System.out.println("\nStatus: " + healthCheck.getStatusMessage());
                System.out.println("\nAUTHENTICATION ISSUE DETECTED:");
                System.out.println("- Check that email address is verified in the BIM Portal");
                System.out.println("- Verify credentials in .env file");
                System.out.println("- Some features may not be available without authentication");
                System.out.println("\nProceeding with public access only...");
                System.out.println("============================================================");
            }
            
            return client;
            
        } catch (Exception e) {
            System.err.println("Error setting up BIM Portal client: " + e.getMessage());
            logger.error("Setup failed", e);
            return null;
        }
    }
    
    /**
     * Demonstrate basic client usage.
     * @param client Configured BIM Portal client
     */
    public static void demonstrateBasicUsage(EnhancedBimPortalClient client) {
        System.out.println("\n--- Demo: Finding projects ---");
        
        // Search for projects
        List<SimpleAiaProjectPublicDto> projects = client.searchProjects();
        if (!projects.isEmpty()) {
            System.out.println("Found " + projects.size() + " projects:");
            for (int i = 0; i < Math.min(3, projects.size()); i++) {
                SimpleAiaProjectPublicDto project = projects.get(i);
                System.out.println("  " + (i + 1) + ". " + project.getName() + " (" + project.getGuid() + ")");
            }
        } else {
            System.out.println("No projects found in demo");
        }
        
        System.out.println("\n--- Demo: Finding properties ---");
        
        // Search for properties
        List<PropertyOrGroupForPublicDto> properties = client.searchProperties();
        if (!properties.isEmpty()) {
            System.out.println("Found " + properties.size() + " properties:");
            for (int i = 0; i < Math.min(3, properties.size()); i++) {
                PropertyOrGroupForPublicDto property = properties.get(i);
                System.out.println("  " + (i + 1) + ". " + property.getName() + " (" + property.getDataType() + ")");
            }
        } else {
            System.out.println("No properties found in demo");
        }
        
        System.out.println("\n--- Demo: Finding LOINs ---");
        
        // Search for LOINs
        List<SimpleLoinPublicDto> loins = client.searchLoins();
        if (!loins.isEmpty()) {
            System.out.println("Found " + loins.size() + " LOINs:");
            for (int i = 0; i < Math.min(3, loins.size()); i++) {
                SimpleLoinPublicDto loin = loins.get(i);
                System.out.println("  " + (i + 1) + ". " + loin.getName() + " (" + loin.getGuid() + ")");
            }
        } else {
            System.out.println("No LOINs found in demo");
        }
    }
    
    /**
     * Demonstrate export functionality.
     * @param client Configured BIM Portal client
     */
    public static void demonstrateExports(EnhancedBimPortalClient client) {
        System.out.println("\n--- Demo: Export functionality ---");
        
        // Find an exportable project
        Optional<SimpleAiaProjectPublicDto> exportableProject = client.findExportableProject();
        
        if (exportableProject.isPresent()) {
            SimpleAiaProjectPublicDto project = exportableProject.get();
            System.out.println("Testing export with project: " + project.getName());
            
            // Try to export as PDF
            Optional<byte[]> pdfContent = client.exportProjectPdf(project.getGuid());
            if (pdfContent.isPresent()) {
                String filename = "demo_" + project.getGuid() + ".pdf";
                Optional<Path> savedFile = ExportUtils.saveExportFile(pdfContent.get(), filename);
                
                if (savedFile.isPresent()) {
                    System.out.println("Successfully exported project to: " + savedFile.get());
                } else {
                    System.out.println("Export succeeded but file save failed");
                }
            } else {
                System.out.println("Project export failed");
            }
        } else {
            System.out.println("No exportable projects found for demo");
        }
    }
    
    /**
     * Main method for running the quick start demo.
     */
    public static void main(String[] args) {
        System.out.println("BIM Portal Java Client - Quick Start");
        System.out.println("=====================================");
        
        // Check configuration
        System.out.println("\nConfiguration check:");
        BimPortalConfig.displayConfig(true);
        
        // Check export directory
        if (!ExportUtils.isExportDirectoryWritable()) {
            System.err.println("Export directory is not writable!");
            return;
        }
        
        // Quick start
        EnhancedBimPortalClient client = quickStart();
        
        if (client != null) {
            EnhancedBimPortalClient.HealthCheckResult healthCheck = client.performHealthCheck();
            
            // Run demos
            demonstrateBasicUsage(client);
            demonstrateExports(client);
            
            // Final status
            if (healthCheck.isAuthWorking()) {
                System.out.println("\nREADY FOR DEVELOPMENT! Use the client to interact with the API.");
            } else {
                System.out.println("\nSetup complete with public access only.");
                System.out.println("For full functionality, resolve authentication issues first.");
            }
            
            // Clean up
            client.logout();
        } else {
            System.err.println("Client setup failed. Please check configuration and try again.");
        }
    }
}