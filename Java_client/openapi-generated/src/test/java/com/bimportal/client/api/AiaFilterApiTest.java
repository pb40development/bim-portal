package com.bimportal.client.api;

import com.bimportal.client.ApiClient;
import com.bimportal.client.model.FilterGroupForPublicDto;
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
 * API tests for AiaFilterApi
 */
class AiaFilterApiTest {

    private AiaFilterApi api;

    @BeforeEach
    public void setup() {
        api = new ApiClient().buildClient(AiaFilterApi.class);
    }

    
    /**
     * Liefert alle globalen Filter zurück
     *
     * 
     */
    @Test
    void getGlobalFilters1Test() {
        // List<FilterGroupForPublicDto> response = api.getGlobalFilters1();

        // TODO: test validations
    }

    
}
