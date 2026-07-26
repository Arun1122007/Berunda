"""Pydantic schemas for API request/response validation."""

from src.schemas.anomaly import AnomalyAlertResponse, AnomalyQuery
from src.schemas.audit import AuditEntryResponse, AuditQuery
from src.schemas.auth import LoginRequest, TokenResponse, UserResponse
from src.schemas.entity import (
    EntityMergeRequest,
    EntitySearchQuery,
    EntitySearchResponse,
    PersonEntityLinkResponse,
    PersonEntityResponse,
)
from src.schemas.fir import (
    FIRCreate,
    FIRDetailResponse,
    FIRListResponse,
    FIRResponse,
    FIRUpdate,
)
from src.schemas.graph import (
    GraphEdgeResponse,
    GraphNodeResponse,
    GraphQuery,
    GraphResponse,
)
from src.schemas.hotspot import HotspotLayerResponse, HotspotQuery
from src.schemas.ingestion import (
    IngestionCommitRequest,
    IngestionPreviewRequest,
    IngestionPreviewResponse,
    IngestionRowDiagnostic,
)
from src.schemas.offender import (
    OffenderProfileResponse,
    OffenderQuery,
    OffenderSummaryResponse,
)
from src.schemas.rag import RAGCitation, RAGQuery, RAGResponse
from src.schemas.risk import RiskScoreQuery, RiskScoreResponse
from src.schemas.socioeconomic import SocioeconomicQuery, SocioeconomicRecord

__all__ = [
    "AnomalyAlertResponse",
    "AnomalyQuery",
    "AuditEntryResponse",
    "AuditQuery",
    "EntityMergeRequest",
    "EntitySearchQuery",
    "EntitySearchResponse",
    "FIRCreate",
    "FIRDetailResponse",
    "FIRListResponse",
    "FIRResponse",
    "FIRUpdate",
    "GraphEdgeResponse",
    "GraphNodeResponse",
    "GraphQuery",
    "GraphResponse",
    "HotspotLayerResponse",
    "HotspotQuery",
    "IngestionCommitRequest",
    "IngestionPreviewRequest",
    "IngestionPreviewResponse",
    "IngestionRowDiagnostic",
    "LoginRequest",
    "OffenderProfileResponse",
    "OffenderQuery",
    "OffenderSummaryResponse",
    "PersonEntityLinkResponse",
    "PersonEntityResponse",
    "RAGCitation",
    "RAGQuery",
    "RAGResponse",
    "RiskScoreQuery",
    "RiskScoreResponse",
    "SocioeconomicQuery",
    "SocioeconomicRecord",
    "TokenResponse",
    "UserResponse",
]
