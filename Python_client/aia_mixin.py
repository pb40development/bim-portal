"""
AIA-related functionality mixin (LOINs, Projects, Templates, Domain Models, Context Info).
"""

from typing import List, Optional
from uuid import UUID
from auth.auth_config import logger
from models import (
    SimpleLoinPublicDto, LoinForPublicRequest, LOINPublicDto,
    SimpleAiaProjectPublicDto, AiaProjectForPublicRequest, AIAProjectPublicDto,
    SimpleDomainSpecificModelPublicDto, AiaDomainSpecificModelForPublicRequest, 
    AIADomainSpecificModelPublicDto, SimpleContextInfoPublicDto, 
    AiaContextInfoPublicRequest, AIAContextInfoPublicDto,
    SimpleAiaTemplatePublicDto, AiaTemplateForPublicRequest, AIATemplatePublicDto,
    FilterGroupForPublicDto
)


class AiaMixin:
    """
    Mixin providing AIA-related methods (LOINs, Projects, Templates, etc.).
    Requires BaseClient functionality to be available.
    """
    
    # === LOINS ===
    
    def search_loins(self, request: Optional[LoinForPublicRequest] = None) -> List[SimpleLoinPublicDto]:
        """Search for LOINs matching the given criteria."""
        request_data = request.model_dump(exclude_none=True) if request else {}
        
        try:
            response = self._make_authenticated_request("POST", "/aia/api/v1/public/loin", request_data)
            data = self._parse_response_json(response)
            loins = self._parse_model(data, SimpleLoinPublicDto)
            return loins if loins else []
        except Exception as e:
            logger.error(f"Error searching LOINs: {e}")
            return []
    
    def get_loin(self, guid: UUID) -> Optional[LOINPublicDto]:
        """Get detailed information about a specific LOIN."""
        try:
            response = self._make_authenticated_request("GET", f"/aia/api/v1/public/loin/{guid}")
            data = self._parse_response_json(response)
            return self._parse_model(data, LOINPublicDto)
        except Exception as e:
            logger.error(f"Error getting LOIN {guid}: {e}")
            return None
    
    def export_loin_pdf(self, guid: UUID) -> Optional[bytes]:
        """Export LOIN as PDF."""
        try:
            response = self._make_authenticated_request("GET", f"/aia/api/v1/public/loin/{guid}/pdf")
            return response.content if response.status_code == 200 else None
        except Exception as e:
            logger.error(f"Error exporting LOIN {guid} to PDF: {e}")
            return None
    
    def export_loin_openoffice(self, guid: UUID) -> Optional[bytes]:
        """Export LOIN as OpenOffice format."""
        try:
            response = self._make_authenticated_request("GET", f"/aia/api/v1/public/loin/{guid}/openOffice")
            return response.content if response.status_code == 200 else None
        except Exception as e:
            logger.error(f"Error exporting LOIN {guid} to OpenOffice: {e}")
            return None
    
    def export_loin_okstra(self, guid: UUID) -> Optional[bytes]:
        """Export LOIN as OKSTRA zip file."""
        try:
            response = self._make_authenticated_request("GET", f"/aia/api/v1/public/loin/{guid}/okstra")
            return response.content if response.status_code == 200 else None
        except Exception as e:
            logger.error(f"Error exporting LOIN {guid} to OKSTRA: {e}")
            return None
    
    def export_loin_xml(self, guid: UUID) -> Optional[bytes]:
        """Export LOIN as LOIN-XML format."""
        try:
            response = self._make_authenticated_request("GET", f"/aia/api/v1/public/loin/{guid}/loinXML")
            return response.content if response.status_code == 200 else None
        except Exception as e:
            logger.error(f"Error exporting LOIN {guid} to XML: {e}")
            return None
    
    def export_loin_ids(self, guid: UUID) -> Optional[bytes]:
        """Export LOIN as IDS-XML format."""
        try:
            response = self._make_authenticated_request("GET", f"/aia/api/v1/public/loin/{guid}/IDS")
            return response.content if response.status_code == 200 else None
        except Exception as e:
            logger.error(f"Error exporting LOIN {guid} to IDS: {e}")
            return None
    
    # === DOMAIN-SPECIFIC MODELS (FACHMODELLE) ===
    
    def search_domain_models(self, request: Optional[AiaDomainSpecificModelForPublicRequest] = None) -> List[SimpleDomainSpecificModelPublicDto]:
        """Search for domain-specific models matching the given criteria."""
        request_data = request.model_dump(exclude_none=True) if request else {}
        
        try:
            response = self._make_authenticated_request(
                "POST", "/aia/api/v1/public/domainSpecificModel", request_data
            )
            data = self._parse_response_json(response)
            models = self._parse_model(data, SimpleDomainSpecificModelPublicDto)
            return models if models else []
        except Exception as e:
            logger.error(f"Error searching domain models: {e}")
            return []
    
    def get_domain_model(self, guid: UUID) -> Optional[AIADomainSpecificModelPublicDto]:
        """Get detailed information about a specific domain-specific model."""
        try:
            response = self._make_authenticated_request("GET", f"/aia/api/v1/public/domainSpecificModel/{guid}")
            data = self._parse_response_json(response)
            return self._parse_model(data, AIADomainSpecificModelPublicDto)
        except Exception as e:
            logger.error(f"Error getting domain model {guid}: {e}")
            return None
    
    def export_domain_model_pdf(self, guid: UUID) -> Optional[bytes]:
        """Export domain-specific model as PDF."""
        try:
            response = self._make_authenticated_request("GET", f"/aia/api/v1/public/domainSpecificModel/{guid}/pdf")
            return response.content if response.status_code == 200 else None
        except Exception as e:
            logger.error(f"Error exporting domain model {guid} to PDF: {e}")
            return None
    
    def export_domain_model_openoffice(self, guid: UUID) -> Optional[bytes]:
        """Export domain-specific model as OpenOffice format."""
        try:
            response = self._make_authenticated_request("GET", f"/aia/api/v1/public/domainSpecificModel/{guid}/openOffice")
            return response.content if response.status_code == 200 else None
        except Exception as e:
            logger.error(f"Error exporting domain model {guid} to OpenOffice: {e}")
            return None
    
    def export_domain_model_okstra(self, guid: UUID) -> Optional[bytes]:
        """Export domain-specific model as OKSTRA zip file."""
        try:
            response = self._make_authenticated_request("GET", f"/aia/api/v1/public/domainSpecificModel/{guid}/okstra")
            return response.content if response.status_code == 200 else None
        except Exception as e:
            logger.error(f"Error exporting domain model {guid} to OKSTRA: {e}")
            return None
    
    def export_domain_model_loin_xml(self, guid: UUID) -> Optional[bytes]:
        """Export domain-specific model as LOIN-XML zip file."""
        try:
            response = self._make_authenticated_request("GET", f"/aia/api/v1/public/domainSpecificModel/{guid}/loinXML")
            return response.content if response.status_code == 200 else None
        except Exception as e:
            logger.error(f"Error exporting domain model {guid} to LOIN XML: {e}")
            return None
    
    def export_domain_model_ids(self, guid: UUID) -> Optional[bytes]:
        """Export domain-specific model as IDS format."""
        try:
            response = self._make_authenticated_request("GET", f"/aia/api/v1/public/domainSpecificModel/{guid}/IDS")
            return response.content if response.status_code == 200 else None
        except Exception as e:
            logger.error(f"Error exporting domain model {guid} to IDS: {e}")
            return None
    
    # === CONTEXT INFORMATION (KONTEXTINFORMATIONEN) ===
    
    def search_context_info(self, request: Optional[AiaContextInfoPublicRequest] = None) -> List[SimpleContextInfoPublicDto]:
        """Search for context information matching the given criteria."""
        request_data = request.model_dump(exclude_none=True) if request else {}
        
        try:
            response = self._make_authenticated_request(
                "POST", "/aia/api/v1/public/contextInfo", request_data
            )
            data = self._parse_response_json(response)
            contexts = self._parse_model(data, SimpleContextInfoPublicDto)
            return contexts if contexts else []
        except Exception as e:
            logger.error(f"Error searching context info: {e}")
            return []
    
    def get_context_info(self, guid: UUID) -> Optional[AIAContextInfoPublicDto]:
        """Get detailed information about specific context information."""
        try:
            response = self._make_authenticated_request("GET", f"/aia/api/v1/public/contextInfo/{guid}")
            data = self._parse_response_json(response)
            return self._parse_model(data, AIAContextInfoPublicDto)
        except Exception as e:
            logger.error(f"Error getting context info {guid}: {e}")
            return None
    
    def export_context_info_pdf(self, guid: UUID) -> Optional[bytes]:
        """Export context information as PDF."""
        try:
            response = self._make_authenticated_request("GET", f"/aia/api/v1/public/contextInfo/{guid}/pdf")
            return response.content if response.status_code == 200 else None
        except Exception as e:
            logger.error(f"Error exporting context info {guid} to PDF: {e}")
            return None
    
    def export_context_info_openoffice(self, guid: UUID) -> Optional[bytes]:
        """Export context information as OpenOffice format."""
        try:
            response = self._make_authenticated_request("GET", f"/aia/api/v1/public/contextInfo/{guid}/openOffice")
            return response.content if response.status_code == 200 else None
        except Exception as e:
            logger.error(f"Error exporting context info {guid} to OpenOffice: {e}")
            return None
    
    # === AIA TEMPLATES (AIA-VORLAGEN) ===
    
    def search_templates(self, request: Optional[AiaTemplateForPublicRequest] = None) -> List[SimpleAiaTemplatePublicDto]:
        """Search for AIA templates matching the given criteria."""
        request_data = request.model_dump(exclude_none=True) if request else {}
        
        try:
            response = self._make_authenticated_request(
                "POST", "/aia/api/v1/public/aiaTemplate", request_data
            )
            data = self._parse_response_json(response)
            templates = self._parse_model(data, SimpleAiaTemplatePublicDto)
            return templates if templates else []
        except Exception as e:
            logger.error(f"Error searching templates: {e}")
            return []
    
    def get_template(self, guid: UUID) -> Optional[AIATemplatePublicDto]:
        """Get detailed information about a specific AIA template."""
        try:
            response = self._make_authenticated_request("GET", f"/aia/api/v1/public/aiaTemplate/{guid}")
            data = self._parse_response_json(response)
            return self._parse_model(data, AIATemplatePublicDto)
        except Exception as e:
            logger.error(f"Error getting template {guid}: {e}")
            return None
    
    def export_template_pdf(self, guid: UUID) -> Optional[bytes]:
        """Export AIA template as PDF."""
        try:
            response = self._make_authenticated_request("GET", f"/aia/api/v1/public/aiaTemplate/{guid}/pdf")
            return response.content if response.status_code == 200 else None
        except Exception as e:
            logger.error(f"Error exporting template {guid} to PDF: {e}")
            return None
    
    def export_template_openoffice(self, guid: UUID) -> Optional[bytes]:
        """Export AIA template as OpenOffice format."""
        try:
            response = self._make_authenticated_request("GET", f"/aia/api/v1/public/aiaTemplate/{guid}/openOffice")
            return response.content if response.status_code == 200 else None
        except Exception as e:
            logger.error(f"Error exporting template {guid} to OpenOffice: {e}")
            return None
    
    # === AIA PROJECTS ===
    
    def search_projects(self, request: Optional[AiaProjectForPublicRequest] = None) -> List[SimpleAiaProjectPublicDto]:
        """Search for projects matching the given criteria."""
        request_data = request.model_dump(exclude_none=True) if request else {}
        
        try:
            response = self._make_authenticated_request("POST", "/aia/api/v1/public/aiaProject", request_data)
            data = self._parse_response_json(response)
            projects = self._parse_model(data, SimpleAiaProjectPublicDto)
            return projects if projects else []
        except Exception as e:
            logger.error(f"Error searching projects: {e}")
            return []
    
    def get_project(self, guid: UUID) -> Optional[AIAProjectPublicDto]:
        """Get detailed information about a specific project."""
        try:
            response = self._make_authenticated_request("GET", f"/aia/api/v1/public/aiaProject/{guid}")
            data = self._parse_response_json(response)
            return self._parse_model(data, AIAProjectPublicDto)
        except Exception as e:
            logger.error(f"Error getting project {guid}: {e}")
            return None
    
    def export_project_pdf(self, guid: UUID) -> Optional[bytes]:
        """Export project as PDF."""
        try:
            response = self._make_authenticated_request("GET", f"/aia/api/v1/public/aiaProject/{guid}/pdf")
            return response.content if response.status_code == 200 else None
        except Exception as e:
            logger.error(f"Error exporting project {guid} to PDF: {e}")
            return None
    
    def export_project_openoffice(self, guid: UUID) -> Optional[bytes]:
        """Export project as OpenOffice format."""
        try:
            response = self._make_authenticated_request("GET", f"/aia/api/v1/public/aiaProject/{guid}/openOffice")
            return response.content if response.status_code == 200 else None
        except Exception as e:
            logger.error(f"Error exporting project {guid} to OpenOffice: {e}")
            return None
    
    def export_project_okstra(self, guid: UUID) -> Optional[bytes]:
        """Export project as OKSTRA zip file."""
        try:
            response = self._make_authenticated_request("GET", f"/aia/api/v1/public/aiaProject/{guid}/okstra")
            return response.content if response.status_code == 200 else None
        except Exception as e:
            logger.error(f"Error exporting project {guid} to OKSTRA: {e}")
            return None
    
    def export_project_loin_xml(self, guid: UUID) -> Optional[bytes]:
        """Export project as LOIN-XML zip file."""
        try:
            response = self._make_authenticated_request("GET", f"/aia/api/v1/public/aiaProject/{guid}/loinXML")
            return response.content if response.status_code == 200 else None
        except Exception as e:
            logger.error(f"Error exporting project {guid} to LOIN XML: {e}")
            return None
    
    def export_project_ids(self, guid: UUID) -> Optional[bytes]:
        """Export project as IDS format."""
        try:
            response = self._make_authenticated_request("GET", f"/aia/api/v1/public/aiaProject/{guid}/IDS")
            return response.content if response.status_code == 200 else None
        except Exception as e:
            logger.error(f"Error exporting project {guid} to IDS: {e}")
            return None
    
    # === AIA FILTERS ===
    
    def get_aia_filters(self) -> List[FilterGroupForPublicDto]:
        """Get all global AIA filters."""
        try:
            response = self._make_authenticated_request("GET", "/aia/api/v1/public/filter")
            data = self._parse_response_json(response)
            filters = self._parse_model(data, FilterGroupForPublicDto)
            return filters if filters else []
        except Exception as e:
            logger.error(f"Error getting AIA filters: {e}")
            return []