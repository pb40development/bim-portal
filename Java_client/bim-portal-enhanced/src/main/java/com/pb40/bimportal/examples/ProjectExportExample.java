package com.pb40.bimportal.examples;

import com.pb40.bimportal.client.BimPortalClientBuilder;
import com.pb40.bimportal.client.EnhancedBimPortalClient;
import com.pb40.bimportal.config.BimPortalConfig;
import com.pb40.bimportal.util.ExportUtils;

import com.bimportal.client.model.SimpleAiaProjectPublicDto;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.nio.file.Path;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;

/**
 * Project export examples for BIM Portal Java client.
 *
 * Demonstrates project export workflows in multiple formats including
 * PDF, OpenOffice, OKSTRA, LOIN-XML, and IDS.
 */
public class ProjectExportExample {

    private static final Logger logger = LoggerFactory.getLogger(ProjectExportExample.class);

    /**
     * Check if credentials are available for authentication.
     * @return True if credentials are configured
     */
    private static boolean checkCredentials() {
        if (!BimPortalConfig.hasCredentials()) {
            System.out.println("============================================================");
            System.out.println("WARNING: Credentials not found in environment variables.");
            System.out.println("Please set " + BimPortalConfig.USERNAME_ENV_VAR + " and " + BimPortalConfig.PASSWORD_ENV_VAR + " in .env file.");
            System.out.println("============================================================");
            return false;
        }
        return true;
    }

    /**
     * Run project export examples.
     * @param client Enhanced BIM Portal client
     */
    public static void runProjectExportExamples(EnhancedBimPortalClient client) {
        System.out.println("\n============================================================");
        System.out.println("📊 PROJECT EXPORT EXAMPLES");
        System.out.println("============================================================");

        System.out.println("\n1️⃣ Searching for available projects...");
        try {
            List<SimpleAiaProjectPublicDto> projects = client.searchProjects();
            if (projects.isEmpty()) {
                System.out.println("🔭 No projects found for export");
                return;
            }

            System.out.println("✅ Found " + projects.size() + " projects:");
            System.out.println("📋 First 3 available projects:");
            for (int i = 0; i < Math.min(3, projects.size()); i++) {
                SimpleAiaProjectPublicDto project = projects.get(i);
                System.out.println("   " + (i + 1) + ". " + project.getName() + " (" + project.getGuid() + ")");
            }

            System.out.println("\n2️⃣ Finding exportable project...");
            Optional<SimpleAiaProjectPublicDto> exportableProject = client.findExportableProject();

            if (exportableProject.isEmpty()) {
                System.out.println("❌ No exportable projects found. All projects may be restricted or incomplete.");
                return;
            }

            SimpleAiaProjectPublicDto selectedProject = exportableProject.get();
            System.out.println("🎯 Using project: '" + selectedProject.getName() + "'");

            // Test all available project export formats
            Map<String, Path> exportResults = new HashMap<>();

            System.out.println("\n3️⃣ Exporting project in multiple formats...");

            // PDF Export
            System.out.println("   📄 Exporting as PDF...");
            Optional<byte[]> pdfContent = client.exportProjectPdf(selectedProject.getGuid());
            if (pdfContent.isPresent()) {
                String filename = "project_" + selectedProject.getGuid() + ".pdf";
                Optional<Path> pdfPath = ExportUtils.saveExportFile(pdfContent.get(), filename);
                if (pdfPath.isPresent()) {
                    exportResults.put("PDF", pdfPath.get());
                    System.out.println("   ✅ PDF exported: " + pdfPath.get());
                }
            } else {
                System.out.println("   ❌ PDF export failed");
            }

            // OpenOffice Export
            System.out.println("   📝 Exporting as OpenOffice...");
            Optional<byte[]> odtContent = client.exportProjectOpenOffice(selectedProject.getGuid());
            if (odtContent.isPresent()) {
                String filename = "project_" + selectedProject.getGuid() + ".odt";
                Optional<Path> odtPath = ExportUtils.saveExportFile(odtContent.get(), filename);
                if (odtPath.isPresent()) {
                    exportResults.put("OpenOffice", odtPath.get());
                    System.out.println("   ✅ OpenOffice exported: " + odtPath.get());
                }
            } else {
                System.out.println("   ❌ OpenOffice export failed");
            }

            // OKSTRA Export
            System.out.println("   🗗️ Exporting as OKSTRA...");
            Optional<byte[]> okstraContent = client.exportProjectOkstra(selectedProject.getGuid());
            if (okstraContent.isPresent()) {
                String filename = "project_" + selectedProject.getGuid() + ".zip";
                Optional<Path> okstraPath = ExportUtils.saveExportFile(okstraContent.get(), filename);
                if (okstraPath.isPresent()) {
                    exportResults.put("OKSTRA", okstraPath.get());
                    System.out.println("   ✅ OKSTRA exported: " + okstraPath.get());
                }
            } else {
                System.out.println("   ❌ OKSTRA export failed");
            }

            // LOIN-XML Export
            System.out.println("   🔗 Exporting as LOIN-XML...");
            Optional<byte[]> loinXmlContent = client.exportProjectLoinXml(selectedProject.getGuid());
            if (loinXmlContent.isPresent()) {
                String filename = "project_" + selectedProject.getGuid() + "_loin.zip";
                Optional<Path> loinXmlPath = ExportUtils.saveExportFile(loinXmlContent.get(), filename);
                if (loinXmlPath.isPresent()) {
                    exportResults.put("LOIN-XML", loinXmlPath.get());
                    System.out.println("   ✅ LOIN-XML exported: " + loinXmlPath.get());
                }
            } else {
                System.out.println("   ⚠️ LOIN-XML export failed (may require special permissions)");
            }

            // IDS Export
            System.out.println("   🆔 Exporting as IDS...");
            Optional<byte[]> idsContent = client.exportProjectIds(selectedProject.getGuid());
            if (idsContent.isPresent()) {
                String filename = "project_" + selectedProject.getGuid() + ".ids";
                Optional<Path> idsPath = ExportUtils.saveExportFile(idsContent.get(), filename);
                if (idsPath.isPresent()) {
                    exportResults.put("IDS", idsPath.get());
                    System.out.println("   ✅ IDS exported: " + idsPath.get());
                }
            } else {
                System.out.println("   ⚠️ IDS export failed (may require special permissions)");
            }

            // Summary
            System.out.println("\n📈 Export Summary: " + exportResults.size() + "/5 formats successful");
            for (Map.Entry<String, Path> entry : exportResults.entrySet()) {
                System.out.println("   ✅ " + entry.getKey() + ": " + entry.getValue());
            }

            if (exportResults.size() < 3) {
                System.out.println("💡 Note: Some export formats may require special permissions or project setup");
            }

        } catch (Exception e) {
            logger.error("❌ Error in project export examples", e);
            System.err.println("❌ Error in project export examples: " + e.getMessage());
        }
    }

    /**
     * Main method to run project export examples.
     */
    public static void main(String[] args) {
        System.out.println("======================================================================");
        System.out.println("🚀 BIM PORTAL PROJECT EXPORT EXAMPLES");
        System.out.println("======================================================================");

        if (!checkCredentials()) {
            System.err.println("❌ Cannot run export examples without credentials");
            return;
        }

        if (!ExportUtils.isExportDirectoryWritable()) {
            System.err.println("❌ Export directory is not writable!");
            return;
        }

        System.out.println("🔧 Setting up authenticated client...");

        try {
            EnhancedBimPortalClient client = BimPortalClientBuilder.buildDefault();

            EnhancedBimPortalClient.HealthCheckResult healthCheck = client.performHealthCheck();
            System.out.println("🩺 Health check: " + healthCheck);

            if (!healthCheck.isApiAccessible()) {
                System.err.println("❌ API is not accessible. Please check configuration.");
                return;
            }

            runProjectExportExamples(client);

            System.out.println("\n======================================================================");
            System.out.println("✅ PROJECT EXPORT EXAMPLES COMPLETE!");
            System.out.println("======================================================================");
            System.out.println("📂 Check the '" + BimPortalConfig.getExportPath() + "' directory for exported files");

            client.logout();
            System.out.println("👋 Logged out and session closed.");

        } catch (Exception e) {
            logger.error("❌ Error running project export examples", e);
            System.err.println("❌ Error running examples: " + e.getMessage());
        }
    }
}