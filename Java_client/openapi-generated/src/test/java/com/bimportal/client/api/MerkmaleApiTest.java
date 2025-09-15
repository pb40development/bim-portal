package com.bimportal.client.api;

import com.bimportal.client.ApiClient;
import com.bimportal.client.model.PropertyDto;
import com.bimportal.client.model.PropertyOrGroupForPublicDto;
import com.bimportal.client.model.PropertyOrGroupForPublicRequest;
import com.bimportal.client.model.TagGroupForPublicDto;
import java.util.UUID;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.BeforeEach;

import java.time.LocalDate;
import java.time.OffsetDateTime;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import jakarta.validation.constraints.*;
import jakarta.validation.Valid;

/**
 * API tests for MerkmaleApi
 */
class MerkmaleApiTest {

    private MerkmaleApi api;

    @BeforeEach
    public void setup() {
        api = new ApiClient().buildClient(MerkmaleApi.class);
    }

    
    /**
     * Liefert alle globalen Filter zurück
     *
     * 
     */
    @Test
    void getGlobalFiltersTest() {
        // List<TagGroupForPublicDto> response = api.getGlobalFilters();

        // TODO: test validations
    }

    
    /**
     * Liefert alle Merkmale, die zu den Suchparametern passen
     *
     * Diese API erlaubt optional eine Authentifizierung mittels &#39;Bearer {accessToken}&#39; über den Authorization-Header, um nicht öffentlich sichtbare Merkmale abrufen zu können.
     */
    @Test
    void getPropertiesForPublicTest() {
        PropertyOrGroupForPublicRequest propertyOrGroupForPublicRequest = null;
        // List<PropertyOrGroupForPublicDto> response = api.getPropertiesForPublic(propertyOrGroupForPublicRequest);

        // TODO: test validations
    }

    
    /**
     * Liefert das Merkmal mit der gesuchten GUID
     *
     * Diese API erlaubt optional eine Authentifizierung mittels &#39;Bearer {accessToken}&#39; über den Authorization-Header, um nicht öffentlich sichtbare Merkmale abrufen zu können.
     */
    @Test
    void getPropertyForPublicTest() {
        UUID guid = null;
        // PropertyDto response = api.getPropertyForPublic(guid);

        // TODO: test validations
    }

    
}
