"""Pydantic schemas for API request/response validation."""

from src.schemas.ai import (
    AIExtractionResponse,
    AIExtractionReviewRequest,
    AISuggestionItem,
    AISuggestionPayload,
)
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
from src.schemas.workflow import (
    CaseAssignmentCreate,
    CaseAssignmentResponse,
    InvestigationNoteCreate,
    InvestigationNoteResponse,
    FIRStatusTransitionRequest,
    FIRStatusTransitionResponse,
    SupervisorReviewCreate,
    SupervisorReviewResponse,
)
from src.schemas.related_case import RelatedCaseSuggestionResponse, RelatedCaseReviewRequest, RelatedCaseReview
from src.schemas.dashboard import DashboardMetrics, SupervisorDashboardMetrics, RecentActivityItem
from src.schemas.report import ReportRequestCreate, ReportRequestResponse
from src.schemas.job import BackgroundJobCreate, BackgroundJobResponse

__all__ = [
    "AIExtractionResponse",
    "AIExtractionReviewRequest",
    "AISuggestionItem",
    "AISuggestionPayload",
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
    "CaseAssignmentCreate",
    "CaseAssignmentResponse",
    "InvestigationNoteCreate",
    "InvestigationNoteResponse",
    "FIRStatusTransitionRequest",
    "FIRStatusTransitionResponse",
    "SupervisorReviewCreate",
    "SupervisorReviewResponse",
    "RelatedCaseSuggestionResponse",
    "RelatedCaseReviewRequest",
    "RelatedCaseReview",
    "DashboardMetrics",
    "SupervisorDashboardMetrics",
    "RecentActivityItem",
    "ReportRequestCreate",
    "ReportRequestResponse",
    "BackgroundJobCreate",
    "BackgroundJobResponse",
]
