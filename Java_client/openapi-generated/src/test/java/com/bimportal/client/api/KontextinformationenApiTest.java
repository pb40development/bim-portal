package com.bimportal.client.api;

import com.bimportal.client.ApiClient;
import com.bimportal.client.model.AIAContextInfoPublicDto;
import com.bimportal.client.model.AiaContextInfoPublicRequest;
import com.bimportal.client.model.SimpleContextInfoPublicDto;
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
 * API tests for KontextinformationenApi
 */
class KontextinformationenApiTest {

    private KontextinformationenApi api;

    @BeforeEach
    public void setup() {
        api = new ApiClient().buildClient(KontextinformationenApi.class);
    }

    
    /**
     * Liefert die Kontextinformation mit der übergebenen GUID im OpenOffice-Format zurück
     *
     * Diese API erlaubt optional eine Authentifizierung mittels &#39;Bearer {accessToken}&#39; über den Authorization-Header, um nicht öffentlich sichtbare Informationselemente abrufen zu können.
     */
    @Test
    void exportOdt2Test() {
        UUID guid = null;
        // byte[] response = api.exportOdt2(guid);

        // TODO: test validations
    }

    
    /**
     * Liefert die Kontextinformation mit der übergebenen GUID im PDF-Format zurück
     *
     * Diese API erlaubt optional eine Authentifizierung mittels &#39;Bearer {accessToken}&#39; über den Authorization-Header, um nicht öffentlich sichtbare Informationselemente abrufen zu können.
     */
    @Test
    void exportPdf2Test() {
        UUID guid = null;
        // byte[] response = api.exportPdf2(guid);

        // TODO: test validations
    }

    
    /**
     * Liefert die Kontextinformation mit der gesuchten GUID
     *
     * Diese API erlaubt optional eine Authentifizierung mittels &#39;Bearer {accessToken}&#39; über den Authorization-Header, um nicht öffentlich sichtbare Informationselemente abrufen zu können.
     */
    @Test
    void getContextInfoForPublicTest() {
        UUID guid = null;
        // AIAContextInfoPublicDto response = api.getContextInfoForPublic(guid);

        // TODO: test validations
    }

    
    /**
     * Liefert alle Kontextinformationen, die zu den Suchparametern passen
     *
     * Diese API erlaubt optional eine Authentifizierung mittels &#39;Bearer {accessToken}&#39; über den Authorization-Header, um nicht öffentlich sichtbare Informationselemente abrufen zu können.
     */
    @Test
    void getContextInfosForPublicTest() {
        AiaContextInfoPublicRequest aiaContextInfoPublicRequest = null;
        // List<SimpleContextInfoPublicDto> response = api.getContextInfosForPublic(aiaContextInfoPublicRequest);

        // TODO: test validations
    }

    
}
