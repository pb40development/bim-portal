package com.bimportal.client.api;

import com.bimportal.client.ApiClient;
import com.bimportal.client.model.PropertyGroupDto;
import com.bimportal.client.model.PropertyOrGroupForPublicDto;
import com.bimportal.client.model.PropertyOrGroupForPublicRequest;
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
 * API tests for MerkmalsgruppenApi
 */
class MerkmalsgruppenApiTest {

    private MerkmalsgruppenApi api;

    @BeforeEach
    public void setup() {
        api = new ApiClient().buildClient(MerkmalsgruppenApi.class);
    }

    
    /**
     * Liefert die Merkmalsgruppe mit der gesuchten GUID
     *
     * Diese API erlaubt optional eine Authentifizierung mittels &#39;Bearer {accessToken}&#39; über den Authorization-Header, um nicht öffentlich sichtbare Merkmalsgruppen abrufen zu können.
     */
    @Test
    void getPropertyGroupForPublicTest() {
        UUID guid = null;
        // PropertyGroupDto response = api.getPropertyGroupForPublic(guid);

        // TODO: test validations
    }

    
    /**
     * Liefert alle Merkmalsgruppen, die zu den Suchparametern passen
     *
     * Diese API erlaubt optional eine Authentifizierung mittels &#39;Bearer {accessToken}&#39; über den Authorization-Header, um nicht öffentlich sichtbare Merkmalsgruppen abrufen zu können.
     */
    @Test
    void getProperyGroupsForPublicTest() {
        PropertyOrGroupForPublicRequest propertyOrGroupForPublicRequest = null;
        // List<PropertyOrGroupForPublicDto> response = api.getProperyGroupsForPublic(propertyOrGroupForPublicRequest);

        // TODO: test validations
    }

    
}
