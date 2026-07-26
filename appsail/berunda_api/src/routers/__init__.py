"""FastAPI routers for all Phase 2 API endpoints."""

from src.routers.admin_router import router as admin_router
from src.routers.ai_assistant_router import router as ai_assistant_router
from src.routers.ai_intelligence_router import router as ai_intelligence_router
from src.routers.analytics_router import router as analytics_router
from src.routers.anomaly_router import router as anomaly_router
from src.routers.audit_router import router as audit_router
from src.routers.auth_router import router as auth_router
from src.routers.dashboard_router import router as dashboard_router
from src.routers.entity_router import router as entity_router
from src.routers.fairness_router import router as fairness_router
from src.routers.fir_router import router as fir_router
from src.routers.geospatial_router import router as geospatial_router
from src.routers.graph_router import router as graph_router
from src.routers.hotspot_router import router as hotspot_router
from src.routers.ingestion_router import router as ingestion_router
from src.routers.investigation_router import router as investigation_router
from src.routers.notification_router import router as notification_router
from src.routers.offender_router import router as offender_router
from src.routers.persons_router import router as persons_router
from src.routers.police_stations_router import router as police_stations_router
from src.routers.rag_router import router as rag_router
from src.routers.related_cases_router import router as related_cases_router
from src.routers.report_router import router as report_router
from src.routers.risk_router import router as risk_router
from src.routers.search_router import router as search_router
from src.routers.socioeconomic_router import router as socioeconomic_router
from src.routers.webhook_router import router as webhook_router

__all__ = [
    "admin_router",
    "ai_assistant_router",
    "ai_intelligence_router",
    "analytics_router",
    "anomaly_router",
    "audit_router",
    "auth_router",
    "dashboard_router",
    "entity_router",
    "fairness_router",
    "fir_router",
    "geospatial_router",
    "graph_router",
    "hotspot_router",
    "ingestion_router",
    "investigation_router",
    "notification_router",
    "offender_router",
    "persons_router",
    "police_stations_router",
    "rag_router",
    "related_cases_router",
    "report_router",
    "risk_router",
    "search_router",
    "socioeconomic_router",
    "webhook_router",
]
