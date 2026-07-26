from __future__ import annotations

import os
from datetime import datetime, timezone
from typing import Any, List, Optional, Tuple

import zcatalyst_sdk

from src.models.src_models import CaseMaster
from src.repositories.core import (
    AIAssistantRepository,
    AnomalyRepository,
    AuditRepository,
    AuthRepository,
    EntityRepository,
    FairnessRepository,
    FileStorage,
    FIRRepository,
    GraphRepository,
    HotspotRepository,
    IngestionRepository,
    OffenderRepository,
    RAGRepository,
    RiskRepository,
    SocioeconomicRepository,
)


class CatalystFIRRepository(FIRRepository):
    def __init__(self, req: Any):
        self.app = zcatalyst_sdk.initialize(req=req)
        self.zcql = self.app.zcql()
        self.datastore = self.app.datastore()

    async def commit(self) -> None:
        pass

    async def refresh(self, obj: Any) -> None:
        pass

    async def list_firs(
        self, page: int, page_size: int, district_id: Optional[int] = None,
        police_station_id: Optional[int] = None, status_id: Optional[int] = None,
    ) -> Tuple[List[Any], int]:
        query = "SELECT * FROM CaseMaster"
        count_query = "SELECT count(ROWID) FROM CaseMaster"
        conditions = []

        if police_station_id is not None:
            conditions.append(f"PoliceStationID = {police_station_id}")
        if status_id is not None:
            conditions.append(f"CaseStatusID = {status_id}")

        if conditions:
            where_clause = " WHERE " + " AND ".join(conditions)
            query += where_clause
            count_query += where_clause

        offset = (page - 1) * page_size
        query += f" ORDER BY CaseMasterID DESC LIMIT {offset}, {page_size}"

        result = self.zcql.execute_query(query)
        count_result = self.zcql.execute_query(count_query)

        total = 0
        if count_result:
            total = int(list(count_result[0].values())[0].get("count(ROWID)", 0))

        items = []
        for row in result:
            data = row.get("CaseMaster", {})
            items.append(CaseMaster(**data))

        return items, total

    async def get_fir(self, case_master_id: int) -> Optional[Any]:
        query = f"SELECT * FROM CaseMaster WHERE CaseMasterID = {case_master_id}"
        result = self.zcql.execute_query(query)
        if not result:
            return None
        data = result[0].get("CaseMaster", {})
        case = CaseMaster(**data)
        case.complainants = []
        case.victims = []
        case.accused = []
        case.act_sections = []
        return case

    async def create_fir(self, data: Any) -> Any:
        table = self.datastore.table("CaseMaster")
        row_data = data.model_dump(exclude={"BriefFacts", "Latitude", "Longitude"}, exclude_none=True)
        inserted = table.insert_row(row_data)
        return CaseMaster(**inserted)

    async def update_fir(self, case_master_id: int, data: Any) -> Optional[Any]:
        table = self.datastore.table("CaseMaster")
        row_data = data.model_dump(exclude_none=True)
        row_data["CaseMasterID"] = case_master_id
        updated = table.update_row(row_data)
        return CaseMaster(**updated) if updated else None

    async def delete_fir(self, case_master_id: int) -> bool:
        table = self.datastore.table("CaseMaster")
        table.delete_row(case_master_id)
        return True

    async def get_occurrence(self, case_master_id: int) -> Optional[Any]:
        query = f"SELECT * FROM InvOccuranceTime WHERE CaseMasterID = {case_master_id}"
        result = self.zcql.execute_query(query)
        if not result:
            return None
        return result[0]

    async def create_occurrence(self, data: Any) -> Any:
        table = self.datastore.table("InvOccuranceTime")
        inserted = table.insert_row(data.model_dump(exclude_none=True))
        return inserted

    async def delete_occurrence(self, case_master_id: int) -> bool:
        occ = await self.get_occurrence(case_master_id)
        if occ:
            table = self.datastore.table("InvOccuranceTime")
            table.delete_row(occ.get("InvOccuranceTime", {}).get("InvOccuranceTimeID"))
            return True
        return False

    async def create_evidence(self, case_master_id: int, evidence_type: str, description: str, storage_path: str) -> Any:
        table = self.datastore.table("EvidenceMaster")
        row = table.insert_row({
            "CaseMasterID": case_master_id,
            "EvidenceType": evidence_type,
            "Description": description,
            "StoragePath": storage_path,
        })
        return row

    async def list_evidence(self, case_master_id: int) -> list[Any]:
        query = f"SELECT * FROM EvidenceMaster WHERE CaseMasterID = {case_master_id} ORDER BY CreatedAt DESC"
        result = self.zcql.execute_query(query)
        return [row.get("EvidenceMaster", {}) for row in result]

    async def create_audit_entry(self, data: dict) -> Any:
        table = self.datastore.table("AuditLog")
        inserted = table.insert_row(data)
        return inserted

    # ── Phase 4: Investigation Notes ──
    async def create_investigation_note(self, case_master_id: int, author_id: int, content: str, note_type: str = "general", visibility: str = "station", is_amendment: bool = False, original_note_id: Optional[int] = None) -> Any:
        pass

    async def list_investigation_notes(self, case_master_id: int) -> List[Any]:
        return []

    async def get_investigation_note(self, note_id: int) -> Optional[Any]:
        return None

    # ── Phase 4: Case Assignment ──
    async def create_assignment(self, case_master_id: int, assigned_officer_id: int, assigned_by_user_id: int, reason: Optional[str] = None) -> Any:
        pass

    async def list_assignments(self, case_master_id: int) -> List[Any]:
        return []

    async def get_active_assignment(self, case_master_id: int) -> Optional[Any]:
        return None

    # ── Phase 4: Supervisor Review ──
    async def create_supervisor_review(self, case_master_id: int, supervisor_id: int, review_type: str, status: str, comments: Optional[str] = None, action_requested: Optional[str] = None) -> Any:
        pass

    async def list_supervisor_reviews(self, case_master_id: int) -> List[Any]:
        return []

    # ── Phase 4: Related Case Suggestion ──
    async def create_related_case_suggestion(self, source_fir_id: int, candidate_fir_id: int, confidence_score: float, supporting_signals: str, explanation: str, model_version: str = "hybrid-v1.0") -> Any:
        pass

    async def list_related_case_suggestions(self, case_master_id: int) -> List[Any]:
        return []

    async def update_suggestion_review(self, suggestion_id: int, review_status: str, reviewed_by_user_id: int, review_reason: Optional[str] = None) -> Optional[Any]:
        return None

    # ── Phase 4: Timeline ──
    async def get_timeline_events(self, case_master_id: int) -> List[Any]:
        return []

    # ── Phase 3: Analytics Engine ──
    async def calculate_kpi(self, metric_id: str, district_id: Optional[int] = None, police_station_id: Optional[int] = None, start_date: Optional[str] = None, end_date: Optional[str] = None) -> int:
        # Mock Catalyst implementation for MVP
        return 0
        
    async def calculate_trend(self, metric_id: str, grain: str = "daily", district_id: Optional[str] = None, police_station_id: Optional[str] = None) -> List[dict]:
        # Mock Catalyst implementation for MVP
        return []

    async def get_geospatial_clusters(self, district_id: Optional[str] = None, police_station_id: Optional[str] = None) -> List[dict]:
        # Mock Catalyst implementation for MVP
        return []

    # ── Phase 4: AI Intelligence Layer ──
    async def save_ai_task(self, task_data: dict) -> Any:
        return task_data
        
    async def update_ai_review(self, output_id: str, reviewer_id: int, status: str, feedback: Optional[str] = None) -> Optional[Any]:
        return {"output_id": output_id, "status": status, "reviewer_id": reviewer_id}

    # ── Phase 4: Dashboard ──
    async def get_dashboard_metrics(self, district_id: Optional[int] = None, police_station_id: Optional[int] = None) -> dict[str, Any]:
        return {"total_firs": 0, "status_counts": {}, "pending_review_count": 0, "unassigned_count": 0}

    # ── Phase 4: Reports ──
    async def create_report_request(self, report_id: str, requested_by_user_id: int, report_type: str, parameters: Optional[str] = None, file_format: str = "pdf") -> Any:
        pass

    async def list_report_requests(self, user_id: Optional[int] = None) -> List[Any]:
        return []

    async def get_report_request(self, report_id: str) -> Optional[Any]:
        return None

    async def update_report_request(self, report_id: str, status: str, storage_object_ref: Optional[str] = None, error_message: Optional[str] = None) -> Optional[Any]:
        return None

    # ── Phase 4: Vehicles ──
    async def list_vehicles(self, case_master_id: int) -> List[Any]:
        return []

    async def create_vehicle_link(self, case_master_id: int, vehicle_number: str, source: str = "manual", confidence: float = 1.0) -> Any:
        pass

    # ── Phase 4: Locations ──
    async def list_locations(self, case_master_id: int) -> List[Any]:
        return []

    # ── Phase 4: Evidence lifecycle ──
    async def get_evidence_by_id(self, evidence_id: int) -> Optional[Any]:
        return None

    async def update_evidence_status(self, evidence_id: int, status: str) -> Optional[Any]:
        return None



class CatalystAuthRepository(AuthRepository):
    def __init__(self, req: Any):
        self.app = zcatalyst_sdk.initialize(req=req)
        self.zcql = self.app.zcql()
        self.datastore = self.app.datastore()

    async def get_user_by_email(self, email: str) -> Optional[Any]:
        query = f"SELECT * FROM User WHERE Email = '{email}'"
        result = self.zcql.execute_query(query)
        if not result:
            return None
        data = result[0].get("User", {})
        from src.models.auth_models import User
        return User(**data)

    async def get_user_by_id(self, user_id: int) -> Optional[Any]:
        query = f"SELECT * FROM User WHERE UserID = {user_id}"
        result = self.zcql.execute_query(query)
        if not result:
            return None
        data = result[0].get("User", {})
        from src.models.auth_models import User
        return User(**data)

    async def create_user(self, data: dict) -> Any:
        table = self.datastore.table("User")
        inserted = table.insert_row(data)
        from src.models.auth_models import User
        return User(**inserted)

    async def get_session_by_token(self, token_hash: str) -> Optional[Any]:
        query = f"SELECT * FROM Session WHERE TokenHash = '{token_hash}'"
        result = self.zcql.execute_query(query)
        if not result:
            return None
        return result[0]

    async def revoke_session(self, session_id: int) -> None:
        table = self.datastore.table("Session")
        table.update_row({"SessionID": session_id, "RevokedAt": datetime.now(timezone.utc).isoformat()})

    async def save_session(self, session_data: dict) -> Any:
        table = self.datastore.table("Session")
        inserted = table.insert_row(session_data)
        return inserted

    async def commit(self) -> None:
        pass

    async def get_district(self, district_id: int) -> Optional[Any]:
        query = f"SELECT * FROM District WHERE DistrictID = {district_id}"
        result = self.zcql.execute_query(query)
        if not result:
            return None
        return result[0]


class CatalystEntityRepository(EntityRepository):
    def __init__(self, req: Any):
        self.app = zcatalyst_sdk.initialize(req=req)
        self.zcql = self.app.zcql()
        self.datastore = self.app.datastore()

    async def search_entities(
        self, name: Optional[str], district_id: Optional[int],
        page: int, page_size: int,
    ) -> Tuple[List[Any], int]:
        query = "SELECT * FROM PersonEntity"
        conditions = []
        if name:
            conditions.append(f"FullName LIKE '%{name}%'")
        if district_id is not None:
            conditions.append(f"DistrictID = {district_id}")
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        offset = (page - 1) * page_size
        query += f" LIMIT {offset}, {page_size}"
        result = self.zcql.execute_query(query)
        items = [row.get("PersonEntity", {}) for row in result]
        return items, len(items)

    async def get_entity(self, entity_id: int) -> Optional[Any]:
        query = f"SELECT * FROM PersonEntity WHERE PersonEntityID = {entity_id}"
        result = self.zcql.execute_query(query)
        if not result:
            return None
        return result[0].get("PersonEntity", {})

    async def get_entity_links(self, entity_id: int) -> List[Any]:
        query = (
            f"SELECT * FROM RelationshipEdge "
            f"WHERE SourceEntityID = {entity_id} OR TargetEntityID = {entity_id}"
        )
        result = self.zcql.execute_query(query)
        return [row.get("RelationshipEdge", {}) for row in result]

    async def merge_entities(self, source_id: int, target_id: int) -> Optional[Any]:
        table = self.datastore.table("PersonEntity")
        table.delete_row(source_id)
        return await self.get_entity(target_id)


class CatalystAuditRepository(AuditRepository):
    def __init__(self, req: Any):
        self.app = zcatalyst_sdk.initialize(req=req)
        self.zcql = self.app.zcql()
        self.datastore = self.app.datastore()

    async def get_entries(
        self, user_id: Optional[int], action: Optional[str],
        entity_type: Optional[str], start_date: Optional[Any],
        end_date: Optional[Any], page: int, page_size: int,
    ) -> Tuple[List[Any], int]:
        query = "SELECT * FROM AuditLog"
        conditions = []
        if user_id is not None:
            conditions.append(f"ActorUserID = {user_id}")
        if action is not None:
            conditions.append(f"Action = '{action}'")
        if entity_type is not None:
            conditions.append(f"EntityType = '{entity_type}'")
        if start_date is not None:
            conditions.append(f"CreatedAt >= '{start_date}'")
        if end_date is not None:
            conditions.append(f"CreatedAt <= '{end_date}'")
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        offset = (page - 1) * page_size
        query += f" ORDER BY CreatedAt DESC LIMIT {offset}, {page_size}"
        result = self.zcql.execute_query(query)
        items = [row.get("AuditLog", {}) for row in result]
        return items, len(items)

    async def create_entry(self, data: dict) -> Any:
        table = self.datastore.table("AuditLog")
        inserted = table.insert_row(data)
        return inserted

    async def create_audit_entry(self, data: dict) -> Any:
        table = self.datastore.table("AuditLog")
        inserted = table.insert_row(data)
        return inserted


class CatalystAIAssistantRepository(AIAssistantRepository):
    def __init__(self, req: Any):
        self.req = req

    async def get_database_stats(self) -> dict[str, Any]:
        return {
            "total_cases": 100,
            "last_month_cases": 15,
            "top_district": "Bengaluru City",
            "top_crime_head": "Cyber Banking Fraud / Phishing",
            "open_cases": 60,
            "repeat_offenders": 10,
            "top_sub_head_last_month": "Online Job Scam / Telegram Task",
        }


class CatalystAnomalyRepository(AnomalyRepository):
    def __init__(self, req: Any):
        self.req = req

    async def get_alerts(self, *args, **kwargs) -> Any:
        pass


class CatalystFairnessRepository(FairnessRepository):
    def __init__(self, req: Any):
        self.req = req

    async def get_disparity_metrics(self, *args, **kwargs) -> Any:
        pass


class CatalystGraphRepository(GraphRepository):
    def __init__(self, req: Any):
        self.req = req

    async def get_subgraph(self, *args, **kwargs) -> Any:
        pass


class CatalystHotspotRepository(HotspotRepository):
    def __init__(self, req: Any):
        self.req = req

    async def get_hotspots(self, *args, **kwargs) -> Any:
        pass


class CatalystIngestionRepository(IngestionRepository):
    def __init__(self, req: Any):
        self.req = req

    async def ingest_batch(self, *args, **kwargs) -> Any:
        pass


class CatalystOffenderRepository(OffenderRepository):
    def __init__(self, req: Any):
        self.req = req

    async def get_offender_profile(self, *args, **kwargs) -> Any:
        pass


class CatalystRAGRepository(RAGRepository):
    def __init__(self, req: Any):
        self.req = req

    async def search_documents(self, *args, **kwargs) -> Any:
        pass


class CatalystRiskRepository(RiskRepository):
    def __init__(self, req: Any):
        self.req = req

    async def get_risk_scores(self, *args, **kwargs) -> Any:
        pass


class CatalystSocioeconomicRepository(SocioeconomicRepository):
    def __init__(self, req: Any):
        self.req = req

    async def get_metrics(self, *args, **kwargs) -> Any:
        pass


class CatalystFileStorage(FileStorage):
    def __init__(self, req: Any, bucket_name: str | None = None):
        self.app = zcatalyst_sdk.initialize(req=req)
        self.bucket_name = bucket_name or os.environ.get("STRATUS_BUCKET", "berunda-dev-docs")

    async def save_file(self, file_path: str, content: bytes, mime_type: str) -> str:
        import hashlib
        bucket = self.app.get_stratus().bucket(self.bucket_name)
        file_hash = hashlib.sha256(content).hexdigest()
        ext = os.path.splitext(file_path)[1] or ".bin"
        key = f"evidence/{file_hash}{ext}"
        bucket.put_object(key, body=content)
        return f"stratus://{self.bucket_name}/{key}"

    async def get_file(self, file_uri: str) -> bytes | None:
        if not file_uri.startswith("stratus://"):
            return None
        parts = file_uri.replace("stratus://", "").split("/", 1)
        if len(parts) != 2:
            return None
        bucket_name, key = parts
        bucket = self.app.get_stratus().bucket(bucket_name)
        obj = bucket.get_object(key)
        return obj.read() if hasattr(obj, "read") else obj

    async def delete_file(self, file_uri: str) -> bool:
        if not file_uri.startswith("stratus://"):
            return False
        parts = file_uri.replace("stratus://", "").split("/", 1)
        if len(parts) != 2:
            return False
        bucket_name, key = parts
        bucket = self.app.get_stratus().bucket(bucket_name)
        bucket.delete_object(key)
        return True

    async def file_exists(self, file_uri: str) -> bool:
        if not file_uri.startswith("stratus://"):
            return False
        parts = file_uri.replace("stratus://", "").split("/", 1)
        if len(parts) != 2:
            return False
        bucket_name, key = parts
        bucket = self.app.get_stratus().bucket(bucket_name)
        return bucket.head_object(key)
