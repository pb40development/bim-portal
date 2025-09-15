package com.pb40.bimportal.examples;

import com.pb40.bimportal.client.BimPortalClientBuilder;
import com.pb40.bimportal.client.EnhancedBimPortalClient;
import com.pb40.bimportal.config.BimPortalConfig;

import com.bimportal.client.model.OrganisationForPublicDTO;
import com.bimportal.client.api.InfrastrukturApi;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.List;
import java.util.Optional;
import java.util.UUID;

/**
 * Organization examples for BIM Portal Java client.
 *
 * Demonstrates organization functionality according to the actual Swagger API:
 * - GET /infrastruktur/api/v1/public/organisation (public, no auth required)
 * - GET /infrastruktur/api/v1/public/organisation/my?userId={userId} (requires auth + userId)
 */
public class OrganizationExample {

    private static final Logger logger = LoggerFactory.getLogger(OrganizationExample.class);

    /**
     * Check if credentials are available for authentication.
     * @return True if credentials are configured
     */
    private static boolean checkCredentials() {
        if (!BimPortalConfig.hasCredentials()) {
            System.out.println("============================================================");
            System.out.println("WARNING: Credentials not found in environment variables.");
            System.out.println("Please set " + BimPortalConfig.USERNAME_ENV_VAR + " and " + BimPortalConfig.PASSWORD_ENV_VAR + " in .env file.");
            System.out.println("Some organization examples require authentication.");
            System.out.println("============================================================");
            return false;
        }
        return true;
    }

    /**
     * Demonstrate organization API usage with the correct API signatures.
     * @param client Enhanced BIM Portal client
     */
    public static void runOrganizationExamples(EnhancedBimPortalClient client) {
        System.out.println("\n============================================================");
        System.out.println("🏢 ORGANIZATION API EXAMPLES");
        System.out.println("============================================================");

        System.out.println("\n1️⃣ Fetching all available organizations (public endpoint)...");
        try {
            List<OrganisationForPublicDTO> allOrganizations = client.getAllOrganisations();
            System.out.println("✅ Found " + allOrganizations.size() + " available organizations:");

            for (int i = 0; i < Math.min(5, allOrganizations.size()); i++) {
                OrganisationForPublicDTO org = allOrganizations.get(i);
                System.out.println("   " + (i + 1) + ". " + org.getName() +
                        " (" + org.getGuid() + ")" +
                        (org.getDescription() != null ? " - " + org.getDescription() : ""));
            }

            if (allOrganizations.size() > 5) {
                System.out.println("   ... and " + (allOrganizations.size() - 5) + " more");
            }
        } catch (Exception e) {
            System.err.println("❌ Error fetching organizations: " + e.getMessage());
            logger.error("Error fetching organizations", e);
        }

        System.out.println("\n2️⃣ Testing organization search functionality...");
        try {
            List<OrganisationForPublicDTO> allOrgs = client.getAllOrganisations();
            if (!allOrgs.isEmpty()) {
                OrganisationForPublicDTO firstOrg = allOrgs.get(0);

                // Test GUID search
                Optional<OrganisationForPublicDTO> foundByGuid = client.findOrganisationByGuid(firstOrg.getGuid().toString());
                System.out.println("   🔍 Search by GUID: " + (foundByGuid.isPresent() ? "✅ Found" : "❌ Not found"));

                // Test name search
                if (firstOrg.getName() != null) {
                    Optional<OrganisationForPublicDTO> foundByName = client.findOrganisationByName(firstOrg.getName());
                    System.out.println("   🔍 Search by name: " + (foundByName.isPresent() ? "✅ Found" : "❌ Not found"));
                }

                // Test availability check
                boolean hasOrgs = client.hasAvailableOrganisations();
                System.out.println("   📊 Organizations available: " + (hasOrgs ? "✅ Yes" : "❌ No"));
            }
        } catch (Exception e) {
            System.err.println("❌ Error in organization search tests: " + e.getMessage());
            logger.error("Error in organization search tests", e);
        }

        System.out.println("\n3️⃣ Testing user organizations (requires authentication + user UUID)...");
        if (!client.isAuthenticated()) {
            System.out.println("   ⚠️  Authentication required for user organization endpoints");
            System.out.println("   💡 Client is not authenticated - skipping user organization examples");
        } else {
            System.out.println("   ✅ Client is authenticated");

            // Note: The API requires a specific user UUID parameter
            // In a real application, you would need to:
            // 1. Extract user UUID from JWT token
            // 2. Call a user profile endpoint to get the UUID
            // 3. Store it during login process

            System.out.println("   ⚠️  User UUID required for /organisation/my endpoint");
            System.out.println("   💡 Example implementation patterns:");
            System.out.println("      • Extract from JWT token payload");
            System.out.println("      • Add to AuthService during login");
            System.out.println("      • Call user profile API endpoint");

            // Example with placeholder UUID (replace with actual implementation)
            demonstrateUserOrganizationMethods(client);
        }

        System.out.println("\n4️⃣ Testing query parameters approach...");
        try {
            // Example of creating query parameters
            UUID exampleUserId = UUID.randomUUID(); // Replace with actual user UUID
            InfrastrukturApi.GetOrganisationsOfUserQueryParams queryParams =
                    client.createUserOrganisationQueryParams(exampleUserId);

            System.out.println("   ✅ Query parameters created for user: " + exampleUserId);
            System.out.println("   💡 To use: client.getUserOrganisationsWithParams(queryParams)");

        } catch (Exception e) {
            System.err.println("❌ Error in query parameters test: " + e.getMessage());
            logger.error("Error in query parameters test", e);
        }
    }

    /**
     * Demonstrate user organization methods (placeholder implementation).
     * In production, replace the example UUID with actual user identification.
     */
    private static void demonstrateUserOrganizationMethods(EnhancedBimPortalClient client) {
        System.out.println("\n   📝 User Organization Method Examples:");

        // Example UUID - in production, get this from:
        // - JWT token payload
        // - User profile endpoint
        // - AuthService/login process
        UUID exampleUserId = UUID.fromString("550e8400-e29b-41d4-a716-446655440000");

        System.out.println("   ⚠️  Using example UUID: " + exampleUserId);
        System.out.println("   🔄 Replace with actual user UUID in production");

        try {
            // Uncomment and test with real user UUID:
            /*
            List<OrganisationForPublicDTO> userOrgs = client.getUserOrganisations(exampleUserId);
            System.out.println("   ✅ User organizations: " + userOrgs.size());

            for (OrganisationForPublicDTO org : userOrgs) {
                System.out.println("     👤 " + org.getName() + " (" + org.getGuid() + ")");
            }

            // Test membership check
            if (!userOrgs.isEmpty()) {
                boolean isMember = client.isUserMemberOfOrganisation(exampleUserId, userOrgs.get(0).getGuid());
                System.out.println("   👥 Membership check: " + (isMember ? "✅ Confirmed" : "❌ Not confirmed"));
            }

            // Test organization count
            int orgCount = client.getUserOrganisationsCount(exampleUserId);
            System.out.println("   📊 Organization count: " + orgCount);

            // Test organization names
            List<String> orgNames = client.getUserOrganisationNames(exampleUserId);
            System.out.println("   📝 Organization names: " + orgNames);
            */

            System.out.println("   💡 Methods available once you have a real user UUID:");
            System.out.println("      • client.getUserOrganisations(userId)");
            System.out.println("      • client.isUserMemberOfOrganisation(userId, orgGuid)");
            System.out.println("      • client.getUserOrganisationsCount(userId)");
            System.out.println("      • client.getUserOrganisationNames(userId)");

        } catch (Exception e) {
            System.err.println("   ❌ Error in user organization methods: " + e.getMessage());
            logger.error("Error in user organization methods", e);
        }
    }

    /**
     * Helper method to demonstrate how you might extract user ID from token.
     * This is a placeholder - actual implementation depends on your JWT structure.
     */
    public static void demonstrateUserIdExtraction() {
        System.out.println("\n============================================================");
        System.out.println("💡 USER ID EXTRACTION IMPLEMENTATION GUIDE");
        System.out.println("============================================================");

        System.out.println("To use the /organisation/my endpoint, you need the user's UUID:");
        System.out.println("\n🔧 Option 1: Extract from JWT Token");
        System.out.println("   • Parse the JWT payload");
        System.out.println("   • Look for 'sub', 'userId', or similar claim");
        System.out.println("   • Add method to TokenManager or AuthService");

        System.out.println("\n🔧 Option 2: User Profile Endpoint");
        System.out.println("   • Call a separate user profile API");
        System.out.println("   • Cache the user UUID after login");

        System.out.println("\n🔧 Option 3: Store During Login");
        System.out.println("   • Modify login response handling");
        System.out.println("   • Store user UUID alongside tokens");

        System.out.println("\n📝 Example AuthService enhancement:");
        System.out.println("   public Optional<UUID> getCurrentUserId() {");
        System.out.println("       // Parse from stored JWT token");
        System.out.println("       // or call user profile endpoint");
        System.out.println("       // return the user UUID");
        System.out.println("   }");

        System.out.println("\n📝 Example EnhancedBimPortalClient method:");
        System.out.println("   public List<OrganisationForPublicDTO> getCurrentUserOrganisations() {");
        System.out.println("       UUID currentUserId = authService.getCurrentUserId()");
        System.out.println("           .orElseThrow(() -> new RuntimeException(\"User ID not available\"));");
        System.out.println("       return getUserOrganisations(currentUserId);");
        System.out.println("   }");
    }

    /**
     * Main method to run organization examples.
     */
    public static void main(String[] args) {
        System.out.println("======================================================================");
        System.out.println("🚀 BIM PORTAL ORGANIZATION API EXAMPLES");
        System.out.println("======================================================================");

        boolean hasCredentials = checkCredentials();

        System.out.println("🔧 Setting up client...");

        try {
            EnhancedBimPortalClient client = BimPortalClientBuilder.buildDefault();

            // Health check
            EnhancedBimPortalClient.HealthCheckResult healthCheck = client.performHealthCheck();
            System.out.println("🩺 Health check: " + healthCheck);

            if (!healthCheck.isApiAccessible()) {
                System.err.println("❌ API is not accessible. Please check configuration.");
                return;
            }

            // Run organization examples
            runOrganizationExamples(client);

            // Show implementation guide
            demonstrateUserIdExtraction();

            System.out.println("\n======================================================================");
            System.out.println("✅ ORGANIZATION EXAMPLES COMPLETE!");
            System.out.println("======================================================================");

            if (hasCredentials) {
                System.out.println("💡 Next steps: Implement user UUID extraction for full functionality");
            } else {
                System.out.println("💡 Set up credentials to test authenticated organization endpoints");
            }

            // Cleanup
            if (client.isAuthenticated()) {
                client.logout();
                System.out.println("👋 Logged out and session closed.");
            }

        } catch (Exception e) {
            logger.error("❌ Error running organization examples", e);
            System.err.println("❌ Error running examples: " + e.getMessage());
        }
    }
}