package com.pb40.bimportal.auth;

import com.bimportal.client.model.JWTTokenPublicDto;
import com.bimportal.client.model.UserLoginPublicDto;

/**
 * Authentication service interface for BIM Portal API.
 * 
 * This interface defines the contract for authentication operations
 * including login, token refresh, and logout functionality.
 */
public interface AuthService {
    
    /**
     * Login with username and password.
     * @param credentials User login credentials
     * @return JWT token response or null if login failed
     * @throws AuthenticationException if login fails
     */
    JWTTokenPublicDto login(UserLoginPublicDto credentials) throws AuthenticationException;
    
    /**
     * Login using configured credentials from environment.
     * @return JWT token response or null if login failed
     * @throws AuthenticationException if login fails or credentials not configured
     */
    JWTTokenPublicDto login() throws AuthenticationException;
    
    /**
     * Get a valid authentication token, refreshing if necessary.
     * @return Valid JWT token or null if authentication failed
     * @throws AuthenticationException if authentication fails
     */
    String getValidToken() throws AuthenticationException;
    
    /**
     * Refresh the current authentication token.
     * @return New JWT token response or null if refresh failed
     * @throws AuthenticationException if refresh fails
     */
    JWTTokenPublicDto refreshToken() throws AuthenticationException;
    
    /**
     * Logout and invalidate the current token.
     * @return True if logout successful
     */
    boolean logout();
    
    /**
     * Check if currently authenticated.
     * @return True if valid token is available
     */
    boolean isAuthenticated();
    
    /**
     * Clear all stored authentication tokens.
     */
    void clearTokens();
    
    /**
     * Check if credentials are configured.
     * @return True if username and password are available
     */
    boolean hasCredentials();
    
    /**
     * Get the current authentication context GUID.
     * @return Context GUID
     */
    String getContextGuid();
}