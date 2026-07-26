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
from src.schemas.dashboard import DashboardMetrics, RecentActivityItem, SupervisorDashboardMetrics
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
from src.schemas.job import BackgroundJobCreate, BackgroundJobResponse
from src.schemas.offender import (
    OffenderProfileResponse,
    OffenderQuery,
    OffenderSummaryResponse,
)
from src.schemas.rag import RAGCitation, RAGQuery, RAGResponse
from src.schemas.related_case import (
    RelatedCaseReview,
    RelatedCaseReviewRequest,
    RelatedCaseSuggestionResponse,
)
from src.schemas.report import ReportRequestCreate, ReportRequestResponse
from src.schemas.risk import RiskScoreQuery, RiskScoreResponse
from src.schemas.socioeconomic import SocioeconomicQuery, SocioeconomicRecord
from src.schemas.workflow import (
    CaseAssignmentCreate,
    CaseAssignmentResponse,
    FIRStatusTransitionRequest,
    FIRStatusTransitionResponse,
    InvestigationNoteCreate,
    InvestigationNoteResponse,
    SupervisorReviewCreate,
    SupervisorReviewResponse,
)
from src.schemas.webhook import (
    WebhookDeliveryLogResponse,
    WebhookRegisterRequest,
    WebhookResponse,
    WebhookTestDispatchRequest,
)

__all__ = [
    "AIExtractionResponse",
    "AIExtractionReviewRequest",
    "AISuggestionItem",
    "AISuggestionPayload",
    "AnomalyAlertResponse",
    "AnomalyQuery",
    "AuditEntryResponse",
    "AuditQuery",
    "BackgroundJobCreate",
    "BackgroundJobResponse",
    "CaseAssignmentCreate",
    "CaseAssignmentResponse",
    "DashboardMetrics",
    "EntityMergeRequest",
    "EntitySearchQuery",
    "EntitySearchResponse",
    "FIRCreate",
    "FIRDetailResponse",
    "FIRListResponse",
    "FIRResponse",
    "FIRStatusTransitionRequest",
    "FIRStatusTransitionResponse",
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
    "InvestigationNoteCreate",
    "InvestigationNoteResponse",
    "LoginRequest",
    "OffenderProfileResponse",
    "OffenderQuery",
    "OffenderSummaryResponse",
    "PersonEntityLinkResponse",
    "PersonEntityResponse",
    "RAGCitation",
    "RAGQuery",
    "RAGResponse",
    "RecentActivityItem",
    "RelatedCaseReview",
    "RelatedCaseReviewRequest",
    "RelatedCaseSuggestionResponse",
    "ReportRequestCreate",
    "ReportRequestResponse",
    "RiskScoreQuery",
    "RiskScoreResponse",
    "SocioeconomicQuery",
    "SocioeconomicRecord",
    "SupervisorDashboardMetrics",
    "SupervisorReviewCreate",
    "SupervisorReviewResponse",
    "TokenResponse",
    "UserResponse",
    "WebhookDeliveryLogResponse",
    "WebhookRegisterRequest",
    "WebhookResponse",
    "WebhookTestDispatchRequest",
]
