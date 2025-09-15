package com.pb40.bimportal.examples;

import com.pb40.bimportal.client.BimPortalClientBuilder;
import com.pb40.bimportal.client.EnhancedBimPortalClient;
import com.pb40.bimportal.config.BimPortalConfig;
import com.pb40.bimportal.util.ExportUtils;

import com.bimportal.client.model.SimpleLoinPublicDto;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.nio.file.Path;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;

/**
 * LOIN export examples for BIM Portal Java client.
 *
 * Demonstrates LOIN export workflows in multiple formats including
 * PDF, OpenOffice, OKSTRA, LOIN-XML, and IDS.
 */
public class LoinExportExample {

    private static final Logger logger = LoggerFactory.getLogger(LoinExportExample.class);

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
     * Run LOIN export examples.
     * @param client Enhanced BIM Portal client
     */
    public static void runLoinExportExamples(EnhancedBimPortalClient client) {
        System.out.println("\n============================================================");
        System.out.println("📋 LOIN EXPORT EXAMPLES");
        System.out.println("============================================================");

        System.out.println("\n1️⃣ Searching for available LOINs...");
        try {
            List<SimpleLoinPublicDto> loins = client.searchLoins();
            if (loins.isEmpty()) {
                System.out.println("🔭 No LOINs found for export");
                return;
            }

            System.out.println("✅ Found " + loins.size() + " LOINs:");
            for (int i = 0; i < Math.min(3, loins.size()); i++) {
                SimpleLoinPublicDto loin = loins.get(i);
                System.out.println("   " + (i + 1) + ". " + loin.getName() + " (" + loin.getGuid() + ")");
            }

            SimpleLoinPublicDto selectedLoin = loins.get(0);
            System.out.println("\n🎯 Using LOIN: '" + selectedLoin.getName() + "'");

            Map<String, Path> exportResults = new HashMap<>();

            System.out.println("\n2️⃣ Exporting LOIN in multiple formats...");

            // PDF Export
            System.out.println("   📄 Exporting as PDF...");
            Optional<byte[]> pdfContent = client.exportLoinPdf(selectedLoin.getGuid());
            if (pdfContent.isPresent()) {
                String filename = "loin_" + selectedLoin.getGuid() + ".pdf";
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
            Optional<byte[]> odtContent = client.exportLoinOpenOffice(selectedLoin.getGuid());
            if (odtContent.isPresent()) {
                String filename = "loin_" + selectedLoin.getGuid() + ".odt";
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
            Optional<byte[]> okstraContent = client.exportLoinOkstra(selectedLoin.getGuid());
            if (okstraContent.isPresent()) {
                String filename = "loin_" + selectedLoin.getGuid() + ".zip";
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
            Optional<byte[]> xmlContent = client.exportLoinXml(selectedLoin.getGuid());
            if (xmlContent.isPresent()) {
                String filename = "loin_" + selectedLoin.getGuid() + ".xml";
                Optional<Path> xmlPath = ExportUtils.saveExportFile(xmlContent.get(), filename);
                if (xmlPath.isPresent()) {
                    exportResults.put("LOIN-XML", xmlPath.get());
                    System.out.println("   ✅ LOIN-XML exported: " + xmlPath.get());
                }
            } else {
                System.out.println("   ❌ LOIN-XML export failed");
            }

            // IDS Export
            System.out.println("   🆔 Exporting as IDS...");
            Optional<byte[]> idsContent = client.exportLoinIds(selectedLoin.getGuid());
            if (idsContent.isPresent()) {
                String filename = "loin_" + selectedLoin.getGuid() + ".ids";
                Optional<Path> idsPath = ExportUtils.saveExportFile(idsContent.get(), filename);
                if (idsPath.isPresent()) {
                    exportResults.put("IDS", idsPath.get());
                    System.out.println("   ✅ IDS exported: " + idsPath.get());
                }
            } else {
                System.out.println("   ❌ IDS export failed");
            }

            // Summary
            System.out.println("\n📈 Export Summary: " + exportResults.size() + "/5 formats successful");
            for (Map.Entry<String, Path> entry : exportResults.entrySet()) {
                System.out.println("   ✅ " + entry.getKey() + ": " + entry.getValue());
            }

        } catch (Exception e) {
            logger.error("❌ Error in LOIN export examples", e);
            System.err.println("❌ Error in LOIN export examples: " + e.getMessage());
        }
    }

    /**
     * Main method to run LOIN export examples.
     */
    public static void main(String[] args) {
        System.out.println("======================================================================");
        System.out.println("🚀 BIM PORTAL LOIN EXPORT EXAMPLES");
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

            runLoinExportExamples(client);

            System.out.println("\n======================================================================");
            System.out.println("✅ LOIN EXPORT EXAMPLES COMPLETE!");
            System.out.println("======================================================================");
            System.out.println("📂 Check the '" + BimPortalConfig.getExportPath() + "' directory for exported files");

            client.logout();
            System.out.println("👋 Logged out and session closed.");

        } catch (Exception e) {
            logger.error("❌ Error running LOIN export examples", e);
            System.err.println("❌ Error running examples: " + e.getMessage());
        }
    }
}