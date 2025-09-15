package com.pb40.bimportal.config;

import io.github.cdimascio.dotenv.Dotenv;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.File;

/**
 * Configuration loader for environment variables and .env files.
 * 
 * This class handles loading configuration from multiple sources:
 * 1. Environment variables
 * 2. .env file in project root
 * 3. System properties
 * 4. Default values
 */
public class ConfigLoader {
    
    private static final Logger logger = LoggerFactory.getLogger(ConfigLoader.class);
    private static Dotenv dotenv;
    
    static {
        initializeDotenv();
    }
    
    /**
     * Initialize the dotenv loader.
     */
    private static void initializeDotenv() {
        try {
            // Try to load .env file from project root
            File envFile = new File(".env");
            if (envFile.exists()) {
                dotenv = Dotenv.configure()
                        .directory(".")
                        .filename(".env")
                        .ignoreIfMalformed()
                        .ignoreIfMissing()
                        .load();
                logger.info("Loaded configuration from .env file");
            } else {
                // Create empty dotenv if no file exists
                dotenv = Dotenv.configure()
                        .ignoreIfMissing()
                        .load();
                logger.debug("No .env file found, using environment variables only");
            }
        } catch (Exception e) {
            logger.warn("Failed to load .env file: " + e.getMessage());
            dotenv = null;
        }
    }
    
    /**
     * Get a property value from various sources (environment, .env file, system properties).
     * 
     * Priority order:
     * 1. Environment variables
     * 2. .env file
     * 3. System properties
     * 
     * @param key Property key
     * @return Property value or null if not found
     */
    public static String getProperty(String key) {
        return getProperty(key, null);
    }
    
    /**
     * Get a property value with a default fallback.
     * 
     * @param key Property key
     * @param defaultValue Default value if property not found
     * @return Property value or default value
     */
    public static String getProperty(String key, String defaultValue) {
        // 1. Check environment variables first
        String value = System.getenv(key);
        if (value != null && !value.trim().isEmpty()) {
            return value.trim();
        }
        
        // 2. Check .env file
        if (dotenv != null) {
            value = dotenv.get(key);
            if (value != null && !value.trim().isEmpty()) {
                return value.trim();
            }
        }
        
        // 3. Check system properties
        value = System.getProperty(key);
        if (value != null && !value.trim().isEmpty()) {
            return value.trim();
        }
        
        // 4. Return default value
        return defaultValue;
    }
    
    /**
     * Get an integer property with default value.
     * @param key Property key
     * @param defaultValue Default value if property not found or invalid
     * @return Property value as integer
     */
    public static int getIntProperty(String key, int defaultValue) {
        String value = getProperty(key);
        if (value != null) {
            try {
                return Integer.parseInt(value);
            } catch (NumberFormatException e) {
                logger.warn("Invalid integer value for {}: {}. Using default: {}", key, value, defaultValue);
            }
        }
        return defaultValue;
    }
    
    /**
     * Get a boolean property with default value.
     * @param key Property key
     * @param defaultValue Default value if property not found
     * @return Property value as boolean
     */
    public static boolean getBooleanProperty(String key, boolean defaultValue) {
        String value = getProperty(key);
        if (value != null) {
            return Boolean.parseBoolean(value);
        }
        return defaultValue;
    }
    
    /**
     * Check if a property exists in any configuration source.
     * @param key Property key
     * @return True if property exists
     */
    public static boolean hasProperty(String key) {
        return getProperty(key) != null;
    }
    
    /**
     * Reload the .env file (useful for testing or dynamic configuration).
     */
    public static void reloadConfig() {
        logger.info("Reloading configuration...");
        initializeDotenv();
    }
    
    /**
     * Display available configuration sources for debugging.
     */
    public static void displayConfigSources() {
        System.out.println("--- Configuration Sources ---");
        
        File envFile = new File(".env");
        System.out.println(".env file:         " + (envFile.exists() ? "Found" : "Not found"));
        System.out.println("Environment vars:  Available");
        System.out.println("System properties: Available");
        
        if (envFile.exists()) {
            System.out.println(".env file path:    " + envFile.getAbsolutePath());
        }
        System.out.println("-----------------------------");
    }
}