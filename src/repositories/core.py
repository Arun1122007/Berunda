from abc import ABC, abstractmethod
from typing import Any, List, Optional, Tuple


class FIRRepository(ABC):
    @abstractmethod
    async def list_firs(
        self, page: int, page_size: int, district_id: Optional[int] = None,
        police_station_id: Optional[int] = None, status_id: Optional[int] = None,
        assigned_officer_id: Optional[int] = None,
        date_from: Optional[Any] = None, date_to: Optional[Any] = None,
        crime_major_head_id: Optional[int] = None,
    ) -> Tuple[List[Any], int]:
        pass

    @abstractmethod
    async def get_fir(self, case_master_id: int) -> Optional[Any]:
        pass

    @abstractmethod
    async def create_fir(self, data: Any) -> Any:
        pass

    @abstractmethod
    async def update_fir(self, case_master_id: int, data: Any) -> Optional[Any]:
        pass

    @abstractmethod
    async def delete_fir(self, case_master_id: int) -> bool:
        pass

    @abstractmethod
    async def get_occurrence(self, case_master_id: int) -> Optional[Any]:
        pass

    @abstractmethod
    async def create_occurrence(self, data: Any) -> Any:
        pass

    @abstractmethod
    async def delete_occurrence(self, case_master_id: int) -> bool:
        pass

    @abstractmethod
    async def commit(self) -> None:
        pass

    @abstractmethod
    async def refresh(self, obj: Any) -> None:
        pass

    @abstractmethod
    async def create_audit_entry(self, data: dict) -> Any:
        pass

    @abstractmethod
    async def create_evidence(self, case_master_id: int, evidence_type: str, description: str, storage_path: str) -> Any:
        pass

    @abstractmethod
    async def list_evidence(self, case_master_id: int) -> list[Any]:
        pass

    # ── Phase 4: Investigation Notes ──
    @abstractmethod
    async def create_investigation_note(self, case_master_id: int, author_id: int, content: str, note_type: str = "general", visibility: str = "station", is_amendment: bool = False, original_note_id: Optional[int] = None) -> Any:
        pass

    @abstractmethod
    async def list_investigation_notes(self, case_master_id: int) -> List[Any]:
        pass

    @abstractmethod
    async def get_investigation_note(self, note_id: int) -> Optional[Any]:
        pass

    # ── Phase 4: Case Assignment ──
    @abstractmethod
    async def create_assignment(self, case_master_id: int, assigned_officer_id: int, assigned_by_user_id: int, reason: Optional[str] = None) -> Any:
        pass

    @abstractmethod
    async def list_assignments(self, case_master_id: int) -> List[Any]:
        pass

    @abstractmethod
    async def get_active_assignment(self, case_master_id: int) -> Optional[Any]:
        pass

    # ── Phase 4: Supervisor Review ──
    @abstractmethod
    async def create_supervisor_review(self, case_master_id: int, supervisor_id: int, review_type: str, status: str, comments: Optional[str] = None, action_requested: Optional[str] = None) -> Any:
        pass

    @abstractmethod
    async def list_supervisor_reviews(self, case_master_id: int) -> List[Any]:
        pass

    # ── Phase 4: Related Case Suggestion ──
    @abstractmethod
    async def create_related_case_suggestion(self, source_fir_id: int, candidate_fir_id: int, confidence_score: float, supporting_signals: str, explanation: str, model_version: str = "hybrid-v1.0") -> Any:
        pass

    @abstractmethod
    async def list_related_case_suggestions(self, case_master_id: int) -> List[Any]:
        pass

    @abstractmethod
    async def update_suggestion_review(self, suggestion_id: int, review_status: str, reviewed_by_user_id: int, review_reason: Optional[str] = None) -> Optional[Any]:
        pass

    # ── Phase 4: Timeline ──
    @abstractmethod
    async def get_timeline_events(self, case_master_id: int) -> List[Any]:
        pass

    # ── Phase 4: Dashboard ──
    @abstractmethod
    async def get_dashboard_metrics(self, district_id: Optional[int] = None, police_station_id: Optional[int] = None) -> dict[str, Any]:
        pass

    # ── Phase 3: Analytics Engine ──
    @abstractmethod
    async def calculate_kpi(self, metric_id: str, district_id: Optional[int] = None, police_station_id: Optional[int] = None, start_date: Optional[str] = None, end_date: Optional[str] = None) -> int:
        pass

    @abstractmethod
    async def calculate_trend(self, metric_id: str, grain: str = "daily", district_id: Optional[str] = None, police_station_id: Optional[str] = None) -> List[dict]:
        pass

    @abstractmethod
    async def get_category_distribution(self, district_id: Optional[str] = None, police_station_id: Optional[str] = None) -> List[dict]:
        pass

    @abstractmethod
    async def get_status_distribution(self, district_id: Optional[str] = None, police_station_id: Optional[str] = None) -> List[dict]:
        pass

    @abstractmethod
    async def get_aging_distribution(self, district_id: Optional[str] = None, police_station_id: Optional[str] = None) -> List[dict]:
        pass

    @abstractmethod
    async def get_geospatial_clusters(self, district_id: Optional[str] = None, police_station_id: Optional[str] = None) -> List[dict]:
        pass

    # ── Phase 4: AI Intelligence Layer ──
    @abstractmethod
    async def save_ai_task(self, task_data: dict) -> Any:
        pass

    @abstractmethod
    async def update_ai_review(self, output_id: str, reviewer_id: int, status: str, feedback: Optional[str] = None) -> Optional[Any]:
        pass

    # ── Phase 4: Reports ──
    @abstractmethod
    async def create_report_request(self, report_id: str, requested_by_user_id: int, report_type: str, parameters: Optional[str] = None, file_format: str = "pdf") -> Any:
        pass

    @abstractmethod
    async def list_report_requests(self, user_id: Optional[int] = None) -> List[Any]:
        pass

    @abstractmethod
    async def get_report_request(self, report_id: str) -> Optional[Any]:
        pass

    @abstractmethod
    async def update_report_request(self, report_id: str, status: str, storage_object_ref: Optional[str] = None, error_message: Optional[str] = None) -> Optional[Any]:
        pass

    # ── Phase 4: Vehicles ──
    @abstractmethod
    async def list_vehicles(self, case_master_id: int) -> List[Any]:
        pass

    @abstractmethod
    async def create_vehicle_link(self, case_master_id: int, vehicle_number: str, source: str = "manual", confidence: float = 1.0) -> Any:
        pass

    # ── Phase 4: Locations ──
    @abstractmethod
    async def list_locations(self, case_master_id: int) -> List[Any]:
        pass

    # ── Phase 4: Evidence lifecycle ──
    @abstractmethod
    async def get_evidence_by_id(self, evidence_id: int) -> Optional[Any]:
        pass

    @abstractmethod
    async def update_evidence_status(self, evidence_id: int, status: str) -> Optional[Any]:
        pass


class AuthRepository(ABC):
    @abstractmethod
    async def get_user_by_email(self, email: str) -> Optional[Any]:
        pass

    @abstractmethod
    async def get_user_by_id(self, user_id: int) -> Optional[Any]:
        pass

    @abstractmethod
    async def create_user(self, data: dict) -> Any:
        pass

    @abstractmethod
    async def get_session_by_token(self, token_hash: str) -> Optional[Any]:
        pass

    @abstractmethod
    async def revoke_session(self, session_id: int) -> None:
        pass

    @abstractmethod
    async def save_session(self, session_data: dict) -> Any:
        pass

    @abstractmethod
    async def commit(self) -> None:
        pass


class EntityRepository(ABC):
    @abstractmethod
    async def search_entities(
        self, name: Optional[str], district_id: Optional[int],
        page: int, page_size: int,
    ) -> Tuple[List[Any], int]:
        pass

    @abstractmethod
    async def get_entity(self, entity_id: int) -> Optional[Any]:
        pass

    @abstractmethod
    async def get_entity_links(self, entity_id: int) -> List[Any]:
        pass

    @abstractmethod
    async def merge_entities(self, source_id: int, target_id: int) -> Optional[Any]:
        pass


class AuditRepository(ABC):
    @abstractmethod
    async def get_entries(
        self, user_id: Optional[int], action: Optional[str],
        entity_type: Optional[str], start_date: Optional[Any],
        end_date: Optional[Any], page: int, page_size: int,
    ) -> Tuple[List[Any], int]:
        pass

    @abstractmethod
    async def create_entry(self, data: dict) -> Any:
        pass

    @abstractmethod
    async def create_audit_entry(self, data: dict) -> Any:
        pass


class FileStorage(ABC):
    @abstractmethod
    async def save_file(self, file_path: str, content: bytes, mime_type: str) -> str:
        pass

    @abstractmethod
    async def get_file(self, file_uri: str) -> Optional[bytes]:
        pass

    @abstractmethod
    async def delete_file(self, file_uri: str) -> bool:
        pass

    @abstractmethod
    async def file_exists(self, file_uri: str) -> bool:
        pass


class AIAssistantRepository(ABC):
    @abstractmethod
    async def get_database_stats(self) -> dict[str, Any]:
        pass


class AnomalyRepository(ABC):
    @abstractmethod
    async def get_alerts(self, *args, **kwargs) -> Any:
        pass


class FairnessRepository(ABC):
    @abstractmethod
    async def get_disparity_metrics(self, *args, **kwargs) -> Any:
        pass


class GraphRepository(ABC):
    @abstractmethod
    async def get_subgraph(self, *args, **kwargs) -> Any:
        pass


class HotspotRepository(ABC):
    @abstractmethod
    async def get_hotspots(self, *args, **kwargs) -> Any:
        pass


class IngestionRepository(ABC):
    @abstractmethod
    async def ingest_batch(self, *args, **kwargs) -> Any:
        pass


class OffenderRepository(ABC):
    @abstractmethod
    async def get_offender_profile(self, *args, **kwargs) -> Any:
        pass


class RAGRepository(ABC):
    @abstractmethod
    async def search_documents(self, *args, **kwargs) -> Any:
        pass


class RiskRepository(ABC):
    @abstractmethod
    async def get_risk_scores(self, *args, **kwargs) -> Any:
        pass


class SocioeconomicRepository(ABC):
    @abstractmethod
    async def get_metrics(self, *args, **kwargs) -> Any:
        pass




class RepositoryFactory(ABC):
    @abstractmethod
    def get_fir_repository(self) -> FIRRepository:
        pass

    @abstractmethod
    def get_auth_repository(self) -> AuthRepository:
        pass

    @abstractmethod
    def get_entity_repository(self) -> EntityRepository:
        pass

    @abstractmethod
    def get_audit_repository(self) -> AuditRepository:
        pass

    @abstractmethod
    def get_file_storage(self) -> FileStorage:
        pass

    @abstractmethod
    def get_ai_assistant_repository(self) -> AIAssistantRepository:
        pass

    @abstractmethod
    def get_anomaly_repository(self) -> AnomalyRepository:
        pass

    @abstractmethod
    def get_fairness_repository(self) -> FairnessRepository:
        pass

    @abstractmethod
    def get_graph_repository(self) -> GraphRepository:
        pass

    @abstractmethod
    def get_hotspot_repository(self) -> HotspotRepository:
        pass

    @abstractmethod
    def get_ingestion_repository(self) -> IngestionRepository:
        pass

    @abstractmethod
    def get_offender_repository(self) -> OffenderRepository:
        pass

    @abstractmethod
    def get_rag_repository(self) -> RAGRepository:
        pass

    @abstractmethod
    def get_risk_repository(self) -> RiskRepository:
        pass

    @abstractmethod
    def get_socioeconomic_repository(self) -> SocioeconomicRepository:
        pass

