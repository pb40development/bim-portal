package com.pb40.bimportal.auth;

import com.pb40.bimportal.config.BimPortalConfig;
import com.bimportal.client.model.JWTTokenPublicDto;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.time.*;
import java.time.format.DateTimeFormatter;
import java.util.Base64;
import java.util.concurrent.locks.ReentrantReadWriteLock;

/**
 * Thread-safe JWT token manager for BIM Portal authentication.
 *
 * Handles token storage, validation, and expiration checking.
 */
public class TokenManager {

    private static final Logger logger = LoggerFactory.getLogger(TokenManager.class);

    private volatile String accessToken;
    private volatile String refreshToken;
    private volatile Instant tokenExpiresAt;

    private final ReentrantReadWriteLock lock = new ReentrantReadWriteLock();
    private final ReentrantReadWriteLock.ReadLock readLock = lock.readLock();
    private final ReentrantReadWriteLock.WriteLock writeLock = lock.writeLock();

    /**
     * Store tokens from authentication response.
     * @param tokenResponse JWT token response from API
     */
    public void storeTokens(JWTTokenPublicDto tokenResponse) {
        if (tokenResponse == null) {
            logger.warn("Cannot store null token response");
            return;
        }

        writeLock.lock();
        try {
            this.accessToken = tokenResponse.getToken();
            this.refreshToken = tokenResponse.getRefreshToken();
            this.tokenExpiresAt = parseTokenExpiration(tokenResponse.getToken());

            //Instant etcExpiration = this.tokenExpiresAt.atZone(ZoneOffset.UTC)
             /////       .withZoneSameInstant(ZoneId.of("Europe/Paris")) // CET timezone
                 //   .toInstant();
            //logger.info("Tokens stored successfully. Expires at: {}", etcExpiration);
            ZonedDateTime cetTime = this.tokenExpiresAt.atZone(ZoneOffset.UTC)
                    .withZoneSameInstant(ZoneId.of("Europe/Paris"));

//            logger.info("Tokens stored successfully. Expires at: {}", cetTime);
// or format it nicely:
            logger.info("Tokens stored successfully. Expires at: {}", cetTime.format(DateTimeFormatter.ISO_LOCAL_DATE_TIME));
        } finally {
            writeLock.unlock();
        }
    }

    /**
     * Get the current access token if valid.
     * @return Access token or null if not available or expired
     */
    public String getAccessToken() {
        readLock.lock();
        try {
            if (accessToken == null) {
                return null;
            }

            if (isTokenExpiring()) {
                logger.debug("Access token is expiring soon");
                return null;
            }

            return accessToken;
        } finally {
            readLock.unlock();
        }
    }

    /**
     * Get the current refresh token.
     * @return Refresh token or null if not available
     */
    public String getRefreshToken() {
        readLock.lock();
        try {
            return refreshToken;
        } finally {
            readLock.unlock();
        }
    }

    /**
     * Check if the current token is expiring soon.
     * @return True if token will expire within the configured margin
     */
    public boolean isTokenExpiring() {
        readLock.lock();
        try {
            if (tokenExpiresAt == null) {
                return true;
            }

            Instant refreshThreshold = Instant.now().plus(BimPortalConfig.TOKEN_REFRESH_MARGIN);
            return tokenExpiresAt.isBefore(refreshThreshold);
        } finally {
            readLock.unlock();
        }
    }

    /**
     * Check if tokens are available.
     * @return True if access token exists
     */
    public boolean hasTokens() {
        readLock.lock();
        try {
            return accessToken != null;
        } finally {
            readLock.unlock();
        }
    }

    /**
     * Clear all stored tokens.
     */
    public void clearTokens() {
        writeLock.lock();
        try {
            this.accessToken = null;
            this.refreshToken = null;
            this.tokenExpiresAt = null;
            logger.info("All tokens cleared");
        } finally {
            writeLock.unlock();
        }
    }

    /**
     * Parse JWT token expiration from token payload.
     * @param token JWT token
     * @return Expiration instant or null if parsing fails
     */
    private Instant parseTokenExpiration(String token) {
        if (token == null || token.trim().isEmpty()) {
            return null;
        }

        try {
            String[] parts = token.split("\\.");
            if (parts.length < 2) {
                logger.warn("Invalid JWT token format");
                return null;
            }

            String payload = new String(Base64.getUrlDecoder().decode(parts[1]));

            // Simple JSON parsing for exp claim
            int expIndex = payload.indexOf("\"exp\":");
            if (expIndex == -1) {
                logger.warn("No exp claim found in JWT token");
                return null;
            }

            String expPart = payload.substring(expIndex + 6);
            int commaIndex = expPart.indexOf(",");
            int braceIndex = expPart.indexOf("}");

            int endIndex = -1;
            if (commaIndex != -1 && braceIndex != -1) {
                endIndex = Math.min(commaIndex, braceIndex);
            } else if (commaIndex != -1) {
                endIndex = commaIndex;
            } else if (braceIndex != -1) {
                endIndex = braceIndex;
            }

            if (endIndex == -1) {
                logger.warn("Could not parse exp claim");
                return null;
            }

            String expValue = expPart.substring(0, endIndex).trim();
            long expirationSeconds = Long.parseLong(expValue);

            return Instant.ofEpochSecond(expirationSeconds);

        } catch (Exception e) {
            logger.warn("Failed to parse token expiration: {}", e.getMessage());
            return null;
        }
    }

    /**
     * Get token status information for debugging.
     * @return Status string
     */
    public String getTokenStatus() {
        readLock.lock();
        try {
            if (accessToken == null) {
                return "No token";
            }

            if (tokenExpiresAt == null) {
                return "Token available (expiration unknown)";
            }

            if (isTokenExpiring()) {
                return "Token expiring soon (expires: " + tokenExpiresAt + ")";
            }

            return "Token valid (expires: " + tokenExpiresAt + ")";
        } finally {
            readLock.unlock();
        }
    }
}