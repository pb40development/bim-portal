package com.pb40.bimportal.auth;

import com.pb40.bimportal.client.ApiClientFactory;
import com.bimportal.client.api.InfrastrukturApi;
import com.pb40.bimportal.config.BimPortalConfig;
import com.bimportal.client.model.JWTTokenPublicDto;
import com.bimportal.client.model.RefreshTokenRequestDTO;
import com.bimportal.client.model.UserLoginPublicDto;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * Implementation of AuthService for BIM Portal API authentication.
 *
 * This class handles the complete authentication lifecycle including
 * login, token management, refresh, and logout operations.
 */
public class AuthServiceImpl implements AuthService {

    private static final Logger logger = LoggerFactory.getLogger(AuthServiceImpl.class);

    private final TokenManager tokenManager;
    private final InfrastrukturApi infraApi;
    private final String contextGuid;
    private final String username;
    private final String password;

    /**
     * Constructor with explicit credentials.
     * @param infraApi Infrastructure API client
     * @param contextGuid Context GUID for authentication
     * @param username Username for authentication
     * @param password Password for authentication
     */
    public AuthServiceImpl(InfrastrukturApi infraApi, String contextGuid, String username, String password) {
//        this.infraApi = infraApi;
        this.infraApi = ApiClientFactory.createInfrastrukturApi();
        this.contextGuid = contextGuid != null ? contextGuid : BimPortalConfig.DEFAULT_AUTH_GUID;
        this.username = username;
        this.password = password;
        this.tokenManager = new TokenManager();

        logger.debug("AuthService initialized with context GUID: {}", this.contextGuid);
    }

    /**
     * Constructor using configuration from environment.
     * @param infraApi Infrastructure API client
     * @param contextGuid Context GUID for authentication
     */
    public AuthServiceImpl(InfrastrukturApi infraApi, String contextGuid) {
        this(infraApi, contextGuid, BimPortalConfig.getUsername(), BimPortalConfig.getPassword());
    }

    /**
     * Constructor with default context GUID from configuration.
     * @param infraApi Infrastructure API client
     */
    public AuthServiceImpl(InfrastrukturApi infraApi) {
        this(infraApi, BimPortalConfig.DEFAULT_AUTH_GUID);
    }

    @Override
    public JWTTokenPublicDto login(UserLoginPublicDto credentials) throws AuthenticationException {
        if (credentials == null) {
            throw new AuthenticationException("Credentials cannot be null");
        }

        try {
            logger.debug("Attempting login for user: {}", credentials.getMail());

            JWTTokenPublicDto tokenResponse = infraApi.login(credentials);

            if (tokenResponse != null && tokenResponse.getToken() != null) {
                tokenManager.storeTokens(tokenResponse);
                logger.info("Login successful. Token received.");
                return tokenResponse;
            } else {
                logger.error("Login failed: No token in response");
                throw new AuthenticationException("Login failed: Invalid response from server");
            }

        } catch (Exception e) {
            logger.error("Login failed: {}", e.getMessage());
            throw new AuthenticationException("Login failed: " + e.getMessage(), e);
        }
    }




    @Override
    public JWTTokenPublicDto login() throws AuthenticationException {
        if (!hasCredentials()) {
            throw new AuthenticationException("No credentials configured. Please set " +
                    BimPortalConfig.USERNAME_ENV_VAR + " and " + BimPortalConfig.PASSWORD_ENV_VAR);
        }

        UserLoginPublicDto credentials = new UserLoginPublicDto();
        credentials.setMail(username);
        credentials.setPassword(password);

        return login(credentials);
    }

    @Override
    public String getValidToken() throws AuthenticationException {
        // Check if we have a valid token
        String token = tokenManager.getAccessToken();
        if (token != null) {
            logger.debug("Using cached token");
            return token;
        }

        logger.info("Token is missing or expiring. Attempting to refresh.");

        // Try to refresh token first
        if (tokenManager.getRefreshToken() != null) {
            try {
                JWTTokenPublicDto refreshResponse = refreshToken();
                if (refreshResponse != null) {
                    logger.info("Token refresh successful");
                    return refreshResponse.getToken();
                }
            } catch (AuthenticationException e) {
                logger.debug("Token refresh failed: {}", e.getMessage());
            }
        }

        // If refresh failed or no refresh token, try to login
        logger.info("Token refresh failed or not possible. Attempting to log in.");

        try {
            JWTTokenPublicDto loginResponse = login();
            if (loginResponse != null) {
                return loginResponse.getToken();
            }
        } catch (AuthenticationException e) {
            logger.error("Could not obtain a valid token after login attempt.");
            throw new AuthenticationException("Failed to authenticate. Please check credentials and GUID.", e);
        }

        throw new AuthenticationException("Authentication failed: Unable to obtain valid token");
    }

    @Override
    public JWTTokenPublicDto refreshToken() throws AuthenticationException {
        String currentRefreshToken = tokenManager.getRefreshToken();
        if (currentRefreshToken == null) {
            throw new AuthenticationException("No refresh token available");
        }

        try {
            logger.debug("Attempting to refresh token");

            RefreshTokenRequestDTO refreshRequest = new RefreshTokenRequestDTO();
            refreshRequest.setRefreshToken(currentRefreshToken);

            JWTTokenPublicDto tokenResponse = infraApi.refreshToken(refreshRequest);

            if (tokenResponse != null && tokenResponse.getToken() != null) {
                tokenManager.storeTokens(tokenResponse);
                logger.info("Token refresh successful");
                return tokenResponse;
            } else {
                logger.error("Token refresh failed: No token in response");
                throw new AuthenticationException("Token refresh failed: Invalid response from server");
            }

        } catch (Exception e) {
            logger.error("Token refresh failed: {}", e.getMessage());
            throw new AuthenticationException("Token refresh failed: " + e.getMessage(), e);
        }
    }

    @Override
    public boolean logout() {
        try {
            logger.debug("Attempting logout");

            // Call logout endpoint if token is available
            if (tokenManager.hasTokens()) {
                infraApi.logout();
            }

            // Clear tokens regardless of logout call success
            tokenManager.clearTokens();
            logger.info("Logout completed");
            return true;

        } catch (Exception e) {
            logger.warn("Logout request failed, but tokens cleared: {}", e.getMessage());
            tokenManager.clearTokens();
            return false;
        }
    }

    @Override
    public boolean isAuthenticated() {
        try {
            String token = tokenManager.getAccessToken();
            return token != null;
        } catch (Exception e) {
            return false;
        }
    }

    @Override
    public void clearTokens() {
        tokenManager.clearTokens();
    }

    @Override
    public boolean hasCredentials() {
        return username != null && password != null
                && !username.trim().isEmpty() && !password.trim().isEmpty();
    }

    @Override
    public String getContextGuid() {
        return contextGuid;
    }

    /**
     * Get token status for debugging.
     * @return Current token status
     */
    public String getTokenStatus() {
        return tokenManager.getTokenStatus();
    }

    /**
     * Force token refresh for testing purposes.
     * @throws AuthenticationException if refresh fails
     */
    public void forceTokenRefresh() throws AuthenticationException {
        tokenManager.clearTokens();
        getValidToken();
    }
}