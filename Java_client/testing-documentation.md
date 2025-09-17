# Performance Measurements (Infrastructure):

getAllOrganisations() took 914.318015 ms and delivers expected results.

# Notes (Infrastructure):

getAllOrganisations(UUID) cannot be tested for there are no known valid User IDs.

The message: 

```bash
11:40:02.228 [main] INFO com.pb40.bimportal.auth.AuthServiceImpl -- Token is missing or expiring. Attempting to refresh.  
11:40:02.348 [main] INFO com.pb40.bimportal.auth.TokenManager -- Tokens stored successfully. Expires at: 2025-09-15T11:41:02  
11:40:02.349 [main] INFO com.pb40.bimportal.auth.AuthServiceImpl -- Token refresh successful  
11:40:02.350 [main] INFO com.pb40.bimportal.auth.AuthServiceImpl -- Token refresh successful 
```

shows a Token Refresh log 2x. This is always the case. Elsewhise the login, logout and refresh work as expected.

---

# Performance Measurements (PropertyGroups):

searchPropertyGroups() took 16875.197366 ms and delivers expected results.  

searchPropertyGroups(PropertyOrGroupForPublicRequest), with PropertyOrGroupForPublicRequest only not deprecated, took 13117.345452 ms and delivers expected results.   

# Notes (PropertyGroups): 

In getPropertyGroup(9d9648b1...) the PropertyGroup cannot be found, despite the GUID being listed in the results of the PropertyGroupSearch.

# Other (PropertyGroups):

getPropertyGroup(null, expect empty result), getPropertyGroup(random UUID, expect 404) have been verified as well and is functioning as expected.  
searchPropertyGroups(PropertyOrGroupForPublicRequest), with PropertyOrGroupForPublicRequest only non deprecated, with random orgGuid (expect empty), works as expected.  
getPropertyGroup(null, expect empty result) works as expected.

---

# Performance Measurements (Properties):

searchProperties() took 19141.883202 ms and delivers expected results.  
searchProperties(PropertyOrGroupForPublicRequest), with PropertyOrGroupForPublicRequest only non deprecated, took 17745.515889 ms and delivers expected results.  

getProperty(dda6b4cd...) took 477.951839 ms and delivers expected results.  
getPropertyFilters() took 129.182138 ms  and delivers expected results.  

# Other (Properties):

getProperty('', expect empty result) works as expected.  
getProperty(random UUID, expect 404) works as expected.  
searchProperties(PropertyOrGroupForPublicRequest, expect empty result), with PropertyOrGroupForPublicRequest only non deprecated, with empty orgGuids, works as expected.  

---

# Performance Measurements (Loins):

searchLoins() took 29469.540062 ms and delivers expected results.  
getLoin(ceaed84f-e815-4d3a-8494-7552cdb38797) took 10363.972213 ms and delivers expected results.  

exportLoinPdf() took 202.24832 ms, present=false // suspicious    
exportLoinOpenOffice() took 155.221564 ms, present=true    
exportLoinOkstra() took 116.740979 ms, present=true   
exportLoinXml() took 14647.105433 ms, present=true   
exportLoinIds() took 15274.434908 ms, present=true  

# Notes (Loins):

searchLoins(loinForPublicRequest) funktionert nicht, weil die Datenstruktur nicht mit den Loins übereinstimmt.

# Other (Loins):

getLoin(null, expect empty result), works as expected.  
getLoin(random UUID, expect 404), works as expected.

---

# Performance Measurements (DomainModels):

searchDomainModels() took 11128.665639 ms and delivers expected results.  
getDomainModel(7c5f3b67-6237-426a-9002-fcfae4e00a38) took 11547.101344 ms and delivers expected results.   

exportDomainModelPdf() took 689.367036 ms, present=false // suspicious   
exportDomainModelOpenOffice() took 561.199167 ms, present=true  
exportDomainModelOkstra() took 145.518044 ms, present=true  
exportDomainModelLoinXml() took 15624.835858 ms, present=true   
exportDomainModelIds() took 17624.784698 ms, present=true  

# Notes (DomainModels):

searchDomainModels(aiaDomainSpecificModelForPublicRequest) funktioniert nicht, weil die Datenstruktur der Request nicht übereinstimmt mit den DomainModels.

# Other (DomainModels):

getDomainModel(null, expect empty result), works as expected.  
getDomainModel(random UUID, expect 404), works as expected.

---

# Errors:

04:34:28.593 [main] ERROR com.pb40.bimportal.client.EnhancedBimPortalClient -- Error searching context information:  
[500 ] during [POST] to [https://via.bund.de/bmdv/bim-portal/edu/bim/aia/api/v1/public/contextInfo] [KontextinformationenApi#getContextInfosForPublic(AiaContextInfoPublicRequest)]:  
```json
{
  "timestamp": "2025-09-17T02:34:28.036+00:00",
  "status": 500,
  "error": "Internal Server Error",
  "path": "/bim/aia/api/v1/public/contextInfo"
}
```

# Miscellaneous Notes:
Working with Caching of results could drastically improve runtimes of longer operations at the expense of memory. But it's implementation
is also optional, especially since the Hackathon is approaching soon.  

The API operations on the AiaTemplates and AiaProjects do not as of yet exist.
