"""FastAPI routers for all Phase 2 API endpoints."""

from src.routers.anomaly_router import router as anomaly_router
from src.routers.audit_router import router as audit_router
from src.routers.auth_router import router as auth_router
from src.routers.entity_router import router as entity_router
from src.routers.fairness_router import router as fairness_router
from src.routers.fir_router import router as fir_router
from src.routers.graph_router import router as graph_router
from src.routers.hotspot_router import router as hotspot_router
from src.routers.notification_router import router as notification_router
from src.routers.rag_router import router as rag_router
from src.routers.risk_router import router as risk_router

__all__ = [
    "anomaly_router",
    "audit_router",
    "auth_router",
    "entity_router",
    "fairness_router",
    "fir_router",
    "graph_router",
    "hotspot_router",
    "notification_router",
    "rag_router",
    "risk_router",
]
