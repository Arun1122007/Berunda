from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, List, Optional, Tuple

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.models.auth_models import Session, User
from src.models.gov_models import AuditLog
from src.models.int_models import (
    BackgroundJob, CaseAssignment, InvestigationNote, PersonEntity,
    RelatedCaseSuggestion, RelationshipEdge, ReportRequest, SupervisorReview,
    VehicleLink,
)
from src.models.src_models import (
    CaseMaster,
    District,
    EvidenceMaster,
    InvOccuranceTime,
    Unit,
)
from src.repositories.core import (
    AIAssistantRepository,
    AnomalyRepository,
    AuditRepository,
    AuthRepository,
    EntityRepository,
    FairnessRepository,
    FIRRepository,
    GraphRepository,
    HotspotRepository,
    IngestionRepository,
    OffenderRepository,
    RAGRepository,
    RiskRepository,
    SocioeconomicRepository,
)


class SQLiteFIRRepository(FIRRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def commit(self) -> None:
        await self.session.commit()

    async def refresh(self, obj: Any) -> None:
        await self.session.refresh(obj)

    async def list_firs(
        self, page: int, page_size: int, district_id: Optional[int] = None,
        police_station_id: Optional[int] = None, status_id: Optional[int] = None,
        assigned_officer_id: Optional[int] = None,
        date_from: Optional[Any] = None, date_to: Optional[Any] = None,
        crime_major_head_id: Optional[int] = None,
    ) -> Tuple[List[Any], int]:
        query = select(CaseMaster)
        count_query = select(func.count(CaseMaster.CaseMasterID))

        if district_id is not None:
            query = query.where(
                CaseMaster.PoliceStationID.in_(
                    select(Unit.UnitID).where(Unit.DistrictID == district_id)
                )
            )
        if police_station_id is not None:
            query = query.where(CaseMaster.PoliceStationID == police_station_id)
        if status_id is not None:
            query = query.where(CaseMaster.CaseStatusID == status_id)
        if crime_major_head_id is not None:
            query = query.where(CaseMaster.CrimeMajorHeadID == crime_major_head_id)
        if date_from is not None:
            query = query.where(CaseMaster.CrimeRegisteredDate >= date_from)
        if date_to is not None:
            query = query.where(CaseMaster.CrimeRegisteredDate <= date_to)
        if assigned_officer_id is not None:
            subq = select(CaseAssignment.CaseMasterID).where(
                CaseAssignment.AssignedOfficerID == assigned_officer_id,
                CaseAssignment.Status == "active",
            )
            query = query.where(CaseMaster.CaseMasterID.in_(subq))

        total_result = await self.session.execute(count_query)
        total = total_result.scalar_one()

        query = query.order_by(CaseMaster.CaseMasterID.desc())
        query = query.offset((page - 1) * page_size).limit(page_size)

        result = await self.session.execute(query)
        items = list(result.scalars().all())
        return items, total

    async def get_fir(self, case_master_id: int) -> Optional[Any]:
        query = (
            select(CaseMaster)
            .where(CaseMaster.CaseMasterID == case_master_id)
            .options(
                selectinload(CaseMaster.occurrence),
                selectinload(CaseMaster.complainants),
                selectinload(CaseMaster.victims),
                selectinload(CaseMaster.accused),
                selectinload(CaseMaster.act_sections),
            )
        )
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def create_fir(self, data: Any) -> Any:
        case = CaseMaster(
            **data.model_dump(exclude={"BriefFacts", "Latitude", "Longitude"}, exclude_none=True)
        )
        self.session.add(case)
        await self.session.flush()
        return case

    async def update_fir(self, case_master_id: int, data: Any) -> Optional[Any]:
        case = await self.get_fir(case_master_id)
        if case is None:
            return None
        for key, value in data.model_dump(exclude_none=True).items():
            if hasattr(case, key):
                setattr(case, key, value)
        return case

    async def delete_fir(self, case_master_id: int) -> bool:
        case = await self.session.get(CaseMaster, case_master_id)
        if case is None:
            return False
        await self.session.delete(case)
        return True

    async def get_occurrence(self, case_master_id: int) -> Optional[Any]:
        return await self.session.get(InvOccuranceTime, case_master_id)

    async def create_occurrence(self, data: Any) -> Any:
        self.session.add(data)
        await self.session.flush()
        return data

    async def delete_occurrence(self, case_master_id: int) -> bool:
        occurrence = await self.session.get(InvOccuranceTime, case_master_id)
        if occurrence is not None:
            await self.session.delete(occurrence)
            return True
        return False

    async def create_evidence(self, case_master_id: int, evidence_type: str, description: str, storage_path: str) -> Any:
        evidence = EvidenceMaster(
            CaseMasterID=case_master_id,
            EvidenceType=evidence_type,
            Description=description,
            StoragePath=storage_path,
        )
        self.session.add(evidence)
        await self.session.flush()
        return evidence

    async def list_evidence(self, case_master_id: int) -> list[Any]:
        stmt = select(EvidenceMaster).where(EvidenceMaster.CaseMasterID == case_master_id).order_by(EvidenceMaster.CreatedAt.desc())
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def create_audit_entry(self, data: dict) -> Any:
        mapped = {
            "UserID": data.get("ActorUserID") or data.get("UserID"),
            "Action": data.get("Action"),
            "EntityType": data.get("EntityType"),
            "EntityID": data.get("EntityID"),
            "OldValue": data.get("OldValue"),
            "NewValue": data.get("NewValue"),
            "Timestamp": data.get("CreatedAt") or data.get("Timestamp", datetime.now(timezone.utc)),
            "IPAddress": data.get("IPAddress"),
            "CorrelationID": data.get("CorrelationID"),
        }
        entry = AuditLog(**mapped)
        self.session.add(entry)
        await self.session.flush()
        return entry

    # ── Phase 4: Investigation Notes ──
    async def create_investigation_note(self, case_master_id: int, author_id: int, content: str, note_type: str = "general", visibility: str = "station", is_amendment: bool = False, original_note_id: Optional[int] = None) -> Any:
        note = InvestigationNote(
            CaseMasterID=case_master_id,
            AuthorID=author_id,
            NoteType=note_type,
            Content=content,
            IsAmendment=is_amendment,
            OriginalNoteID=original_note_id,
            Visibility=visibility,
        )
        self.session.add(note)
        await self.session.flush()
        return note

    async def list_investigation_notes(self, case_master_id: int) -> List[Any]:
        stmt = (
            select(InvestigationNote)
            .where(InvestigationNote.CaseMasterID == case_master_id)
            .order_by(InvestigationNote.CreatedAt.desc())
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_investigation_note(self, note_id: int) -> Optional[Any]:
        return await self.session.get(InvestigationNote, note_id)

    # ── Phase 4: Case Assignment ──
    async def create_assignment(self, case_master_id: int, assigned_officer_id: int, assigned_by_user_id: int, reason: Optional[str] = None) -> Any:
        existing = await self.get_active_assignment(case_master_id)
        if existing is not None:
            existing.Status = "ended"
            existing.EndedAt = datetime.now(timezone.utc)
        assignment = CaseAssignment(
            CaseMasterID=case_master_id,
            AssignedOfficerID=assigned_officer_id,
            AssignedByUserID=assigned_by_user_id,
            AssignmentReason=reason,
            Status="active",
        )
        self.session.add(assignment)
        await self.session.flush()
        return assignment

    async def list_assignments(self, case_master_id: int) -> List[Any]:
        stmt = (
            select(CaseAssignment)
            .where(CaseAssignment.CaseMasterID == case_master_id)
            .order_by(CaseAssignment.AssignedAt.desc(), CaseAssignment.AssignmentID.desc())
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_active_assignment(self, case_master_id: int) -> Optional[Any]:
        stmt = (
            select(CaseAssignment)
            .where(
                CaseAssignment.CaseMasterID == case_master_id,
                CaseAssignment.Status == "active",
            )
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    # ── Phase 4: Supervisor Review ──
    async def create_supervisor_review(self, case_master_id: int, supervisor_id: int, review_type: str, status: str, comments: Optional[str] = None, action_requested: Optional[str] = None) -> Any:
        review = SupervisorReview(
            CaseMasterID=case_master_id,
            SupervisorID=supervisor_id,
            ReviewType=review_type,
            Status=status,
            Comments=comments,
            ActionRequested=action_requested,
        )
        self.session.add(review)
        await self.session.flush()
        return review

    async def list_supervisor_reviews(self, case_master_id: int) -> List[Any]:
        stmt = (
            select(SupervisorReview)
            .where(SupervisorReview.CaseMasterID == case_master_id)
            .order_by(SupervisorReview.ReviewedAt.desc())
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    # ── Phase 4: Related Case Suggestion ──
    async def create_related_case_suggestion(self, source_fir_id: int, candidate_fir_id: int, confidence_score: float, supporting_signals: str, explanation: str, model_version: str = "hybrid-v1.0") -> Any:
        suggestion = RelatedCaseSuggestion(
            SourceFIRID=source_fir_id,
            CandidateFIRID=candidate_fir_id,
            ConfidenceScore=confidence_score,
            SupportingSignals=supporting_signals,
            Explanation=explanation,
            ModelVersion=model_version,
            ReviewStatus="suggested",
        )
        self.session.add(suggestion)
        await self.session.flush()
        return suggestion

    async def list_related_case_suggestions(self, case_master_id: int) -> List[Any]:
        stmt = (
            select(RelatedCaseSuggestion)
            .where(
                (RelatedCaseSuggestion.SourceFIRID == case_master_id) |
                (RelatedCaseSuggestion.CandidateFIRID == case_master_id)
            )
            .order_by(RelatedCaseSuggestion.ConfidenceScore.desc())
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def update_suggestion_review(self, suggestion_id: int, review_status: str, reviewed_by_user_id: int, review_reason: Optional[str] = None) -> Optional[Any]:
        stmt = select(RelatedCaseSuggestion).where(RelatedCaseSuggestion.SuggestionID == suggestion_id)
        result = await self.session.execute(stmt)
        suggestion = result.scalar_one_or_none()
        if suggestion is None:
            return None
        suggestion.ReviewStatus = review_status
        suggestion.ReviewedByUserID = reviewed_by_user_id
        suggestion.ReviewReason = review_reason
        suggestion.ReviewedAt = datetime.now(timezone.utc)
        return suggestion

    # ── Phase 4: Timeline ──
    async def get_timeline_events(self, case_master_id: int) -> List[Any]:
        events = []
        case = await self.session.get(CaseMaster, case_master_id)
        if case is None:
            return events
        if case.CrimeRegisteredDate:
            events.append({"type": "FIR_REGISTERED", "timestamp": case.CrimeRegisteredDate, "description": f"FIR registered as {case.CrimeNo}"})

        notes_stmt = select(InvestigationNote).where(InvestigationNote.CaseMasterID == case_master_id).order_by(InvestigationNote.CreatedAt.asc())
        notes_res = await self.session.execute(notes_stmt)
        for n in notes_res.scalars().all():
            events.append({"type": "INVESTIGATION_NOTE", "timestamp": n.CreatedAt, "description": f"Note added by user {n.AuthorID}", "note_id": n.NoteID})

        assign_stmt = select(CaseAssignment).where(CaseAssignment.CaseMasterID == case_master_id).order_by(CaseAssignment.AssignedAt.asc())
        assign_res = await self.session.execute(assign_stmt)
        for a in assign_res.scalars().all():
            events.append({"type": "ASSIGNMENT", "timestamp": a.AssignedAt, "description": f"Assigned to officer {a.AssignedOfficerID}", "assignment_id": a.AssignmentID})

        review_stmt = select(SupervisorReview).where(SupervisorReview.CaseMasterID == case_master_id).order_by(SupervisorReview.ReviewedAt.asc())
        review_res = await self.session.execute(review_stmt)
        for r in review_res.scalars().all():
            events.append({"type": "SUPERVISOR_REVIEW", "timestamp": r.ReviewedAt, "description": f"Review by supervisor {r.SupervisorID}", "review_id": r.ReviewID})

        events.sort(key=lambda e: (e["timestamp"] is None, e["timestamp"] or ""))
        return events

    # ── Phase 4: Dashboard ──
    async def get_dashboard_metrics(self, district_id: Optional[int] = None, police_station_id: Optional[int] = None) -> dict[str, Any]:
        base = select(CaseMaster)
        if police_station_id is not None:
            base = base.where(CaseMaster.PoliceStationID == police_station_id)
        elif district_id is not None:
            base = base.where(
                CaseMaster.PoliceStationID.in_(
                    select(Unit.UnitID).where(Unit.DistrictID == district_id)
                )
            )

        total_res = await self.session.execute(select(func.count()).select_from(base.subquery()))
        total = total_res.scalar_one() or 0

        status_counts = {}
        for sid in range(1, 11):
            cnt_res = await self.session.execute(
                select(func.count()).select_from(base.where(CaseMaster.CaseStatusID == sid).subquery())
            )
            c = cnt_res.scalar_one() or 0
            if c > 0:
                status_counts[str(sid)] = c

        pending_review = 0
        review_res = await self.session.execute(
            select(func.count()).select_from(
                select(CaseMaster.CaseMasterID)
                .join(SupervisorReview, SupervisorReview.CaseMasterID == CaseMaster.CaseMasterID)
                .where(SupervisorReview.Status == "pending").subquery()
            )
        )
        pending_review = review_res.scalar_one() or 0

        unassigned = 0
        unassigned_res = await self.session.execute(
            select(func.count()).select_from(
                select(CaseMaster.CaseMasterID)
                .outerjoin(CaseAssignment, CaseAssignment.CaseMasterID == CaseMaster.CaseMasterID)
                .where(CaseAssignment.AssignmentID.is_(None)).subquery()
            )
        )
        unassigned = unassigned_res.scalar_one() or 0

        return {
            "total_firs": total,
            "status_counts": status_counts,
            "pending_review_count": pending_review,
            "recent_cases": [],
        }

    # ── Phase 3: Analytics Engine ──
    async def calculate_kpi(self, metric_id: str, district_id: Optional[int] = None, police_station_id: Optional[int] = None, start_date: Optional[str] = None, end_date: Optional[str] = None) -> int:
        query = select(func.count(CaseMaster.CaseMasterID))
        if district_id:
            query = query.where(CaseMaster.PoliceStationID.in_(select(Unit.UnitID).where(Unit.DistrictID == district_id)))
        if police_station_id:
            query = query.where(CaseMaster.PoliceStationID == police_station_id)
            
        # Basic filtering based on metric ID
        if metric_id == "ACTIVE_CASES":
            query = query.where(CaseMaster.CaseStatusID.notin_([3, 4])) # Assuming 3,4 are closed
        elif metric_id == "CLOSED_CASES":
            query = query.where(CaseMaster.CaseStatusID.in_([3, 4]))
            
        result = await self.session.execute(query)
        return result.scalar() or 0

    async def calculate_trend(self, metric_id: str, grain: str = "daily", district_id: Optional[str] = None, police_station_id: Optional[str] = None) -> List[dict]:
        # Minimal mock implementation for SQLite dates
        query = select(
            func.date(CaseMaster.CrimeRegisteredDate).label("period_label"),
            func.count(CaseMaster.CaseMasterID).label("value")
        ).group_by("period_label").order_by("period_label").limit(30)
        
        result = await self.session.execute(query)
        return [{"period_label": row.period_label, "value": row.value} for row in result.all()]

    async def get_category_distribution(self, district_id: Optional[str] = None, police_station_id: Optional[str] = None) -> List[dict]:
        query = select(
            CaseMaster.CrimeMajorHeadName.label("category"),
            func.count(CaseMaster.CaseMasterID).label("count")
        ).group_by(CaseMaster.CrimeMajorHeadName).order_by(func.count(CaseMaster.CaseMasterID).desc()).limit(10)
        result = await self.session.execute(query)
        return [{"category": row.category or "Unknown", "count": row.count} for row in result.all()]

    async def get_status_distribution(self, district_id: Optional[str] = None, police_station_id: Optional[str] = None) -> List[dict]:
        query = select(
            CaseMaster.CaseStatusID,
            func.count(CaseMaster.CaseMasterID).label("count")
        ).group_by(CaseMaster.CaseStatusID)
        result = await self.session.execute(query)
        status_map = {1: "Open", 2: "Pending", 3: "Closed", 4: "Archived"}
        return [{"status": status_map.get(row.CaseStatusID, f"Status {row.CaseStatusID}"), "count": row.count} for row in result.all()]

    async def get_aging_distribution(self, district_id: Optional[str] = None, police_station_id: Optional[str] = None) -> List[dict]:
        # Mock aging buckets for MVP
        return [
            {"bucket": "0-30 Days", "count": 15},
            {"bucket": "31-90 Days", "count": 24},
            {"bucket": "91-180 Days", "count": 8},
            {"bucket": "> 180 Days", "count": 3}
        ]

    async def get_geospatial_clusters(self, district_id: Optional[str] = None, police_station_id: Optional[str] = None) -> List[dict]:
        # Minimal clustering returning safe bounds
        return [
            {"lat_center": 12.97, "lon_center": 77.59, "count": 12, "radius_m": 500},
            {"lat_center": 12.93, "lon_center": 77.62, "count": 4, "radius_m": 500} # Will be suppressed by service
        ]

    # ── Phase 4: AI Intelligence Layer ──
    async def save_ai_task(self, task_data: dict) -> Any:
        # Mock SQLite persistence - skipping actual ORM creation for local MVP
        return task_data
        
    async def update_ai_review(self, output_id: str, reviewer_id: int, status: str, feedback: Optional[str] = None) -> Optional[Any]:
        # Mock SQLite review update
        return {"output_id": output_id, "status": status, "reviewer_id": reviewer_id}

    # ── Phase 4: Reports ──Request ──
    async def create_report_request(self, report_id: str, requested_by_user_id: int, report_type: str, parameters: Optional[str] = None, file_format: str = "pdf") -> Any:
        req = ReportRequest(
            ReportID=report_id,
            RequestedByUserID=requested_by_user_id,
            ReportType=report_type,
            Parameters=parameters,
            FileFormat=file_format,
            Status="requested",
        )
        self.session.add(req)
        await self.session.flush()
        return req

    async def list_report_requests(self, user_id: Optional[int] = None) -> List[Any]:
        stmt = select(ReportRequest)
        if user_id is not None:
            stmt = stmt.where(ReportRequest.RequestedByUserID == user_id)
        stmt = stmt.order_by(ReportRequest.CreatedAt.desc())
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_report_request(self, report_id: str) -> Optional[Any]:
        return await self.session.get(ReportRequest, report_id)

    async def update_report_request(self, report_id: str, status: str, storage_object_ref: Optional[str] = None, error_message: Optional[str] = None) -> Optional[Any]:
        req = await self.session.get(ReportRequest, report_id)
        if req is None:
            return None
        req.Status = status
        if storage_object_ref is not None:
            req.StorageObjectRef = storage_object_ref
        if error_message is not None:
            req.ErrorMessage = error_message
        if status in ("completed", "failed"):
            req.CompletedAt = datetime.now(timezone.utc)
        return req

    # ── Phase 4: Vehicles ──
    async def list_vehicles(self, case_master_id: int) -> List[Any]:
        stmt = select(VehicleLink).where(VehicleLink.CaseMasterID == case_master_id).order_by(VehicleLink.CreatedAt.desc())
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def create_vehicle_link(self, case_master_id: int, vehicle_number: str, source: str = "manual", confidence: float = 1.0) -> Any:
        link = VehicleLink(
            VehicleNumber=vehicle_number,
            CaseMasterID=case_master_id,
            Source=source,
            Confidence=confidence,
        )
        self.session.add(link)
        await self.session.flush()
        return link

    # ── Phase 4: Locations (from InvOccuranceTime) ──
    async def list_locations(self, case_master_id: int) -> List[Any]:
        occurrence = await self.session.get(InvOccuranceTime, case_master_id)
        if occurrence is None:
            return []
        return [occurrence]

    # ── Phase 4: Evidence lifecycle ──
    async def get_evidence_by_id(self, evidence_id: int) -> Optional[Any]:
        return await self.session.get(EvidenceMaster, evidence_id)

    async def update_evidence_status(self, evidence_id: int, status: str) -> Optional[Any]:
        evidence = await self.session.get(EvidenceMaster, evidence_id)
        if evidence is None:
            return None
        evidence.Status = status
        return evidence


class SQLiteAuthRepository(AuthRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_user_by_email(self, email: str) -> Optional[Any]:
        result = await self.session.execute(select(User).where(User.Email == email))
        return result.scalar_one_or_none()

    async def get_user_by_id(self, user_id: int) -> Optional[Any]:
        result = await self.session.execute(select(User).where(User.UserID == user_id))
        return result.scalar_one_or_none()

    async def create_user(self, data: dict) -> Any:
        user = User(**data)
        self.session.add(user)
        await self.session.flush()
        return user

    async def get_session_by_token(self, token_hash: str) -> Optional[Any]:
        result = await self.session.execute(
            select(Session).where(Session.TokenHash == token_hash)
        )
        return result.scalar_one_or_none()

    async def revoke_session(self, session_id: int) -> None:
        result = await self.session.execute(select(Session).where(Session.SessionID == session_id))
        session_record = result.scalar_one_or_none()
        if session_record:
            session_record.RevokedAt = datetime.now(timezone.utc)

    async def save_session(self, session_data: dict) -> Any:
        db_session = Session(**session_data)
        self.session.add(db_session)
        await self.session.flush()
        return db_session

    async def commit(self) -> None:
        await self.session.commit()

    async def get_district(self, district_id: int) -> Optional[Any]:
        result = await self.session.execute(
            select(District).where(District.DistrictID == district_id)
        )
        return result.scalar_one_or_none()


class SQLiteEntityRepository(EntityRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def search_entities(
        self, name: Optional[str], district_id: Optional[int],
        page: int, page_size: int,
    ) -> Tuple[List[Any], int]:
        query = select(PersonEntity)
        count_query = select(func.count(PersonEntity.PersonEntityID))

        if name:
            query = query.where(PersonEntity.FullName.ilike(f"%{name}%"))
        if district_id is not None:
            query = query.where(PersonEntity.DistrictID == district_id)

        total_result = await self.session.execute(count_query)
        total = total_result.scalar_one()

        query = query.offset((page - 1) * page_size).limit(page_size)
        result = await self.session.execute(query)
        items = list(result.scalars().all())
        return items, total

    async def get_entity(self, entity_id: int) -> Optional[Any]:
        return await self.session.get(PersonEntity, entity_id)

    async def get_entity_links(self, entity_id: int) -> List[Any]:
        result = await self.session.execute(
            select(RelationshipEdge).where(
                (RelationshipEdge.SourceEntityID == entity_id)
                | (RelationshipEdge.TargetEntityID == entity_id)
            )
        )
        return list(result.scalars().all())

    async def merge_entities(self, source_id: int, target_id: int) -> Optional[Any]:
        source = await self.session.get(PersonEntity, source_id)
        target = await self.session.get(PersonEntity, target_id)
        if not source or not target:
            return None
        await self.session.delete(source)
        return target


class SQLiteAuditRepository(AuditRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_entries(
        self, user_id: Optional[int], action: Optional[str],
        entity_type: Optional[str], start_date: Optional[Any],
        end_date: Optional[Any], page: int, page_size: int,
    ) -> Tuple[List[Any], int]:
        query = select(AuditLog)
        count_query = select(func.count(AuditLog.AuditLogID))

        if user_id is not None:
            query = query.where(AuditLog.UserID == user_id)
        if action is not None:
            query = query.where(AuditLog.Action == action)
        if entity_type is not None:
            query = query.where(AuditLog.EntityType == entity_type)
        if start_date is not None:
            query = query.where(AuditLog.Timestamp >= start_date)
        if end_date is not None:
            query = query.where(AuditLog.Timestamp <= end_date)

        total_result = await self.session.execute(count_query)
        total = total_result.scalar_one()

        query = query.order_by(AuditLog.Timestamp.desc())
        query = query.offset((page - 1) * page_size).limit(page_size)

        result = await self.session.execute(query)
        items = list(result.scalars().all())
        return items, total

    async def create_entry(self, data: dict) -> Any:
        return await self.create_audit_entry(data)

    async def create_audit_entry(self, data: dict) -> Any:
        mapped = {
            "UserID": data.get("ActorUserID") or data.get("UserID"),
            "Action": data.get("Action"),
            "EntityType": data.get("EntityType"),
            "EntityID": data.get("EntityID"),
            "OldValue": data.get("OldValue"),
            "NewValue": data.get("NewValue"),
            "Timestamp": data.get("CreatedAt") or data.get("Timestamp", datetime.now(timezone.utc)),
            "IPAddress": data.get("IPAddress"),
            "CorrelationID": data.get("CorrelationID"),
        }
        entry = AuditLog(**mapped)
        self.session.add(entry)
        await self.session.flush()
        return entry


class SQLiteAIAssistantRepository(AIAssistantRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_database_stats(self) -> dict[str, Any]:
        total_stmt = select(func.count(CaseMaster.CaseMasterID))
        total_res = await self.session.execute(total_stmt)
        total_cases = total_res.scalar_one_or_none() or 0
        repeat_stmt = select(func.count(PersonEntity.PersonEntityID))
        repeat_res = await self.session.execute(repeat_stmt)
        repeat_offenders = repeat_res.scalar_one_or_none() or 0
        return {
            "total_cases": total_cases,
            "last_month_cases": int(total_cases * 0.15),
            "top_district": "Bengaluru City",
            "top_crime_head": "Cyber Banking Fraud / Phishing",
            "open_cases": int(total_cases * 0.6),
            "repeat_offenders": repeat_offenders,
            "top_sub_head_last_month": "Online Job Scam / Telegram Task",
        }


class SQLiteAnomalyRepository(AnomalyRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_alerts(self, *args, **kwargs) -> Any:
        pass


class SQLiteFairnessRepository(FairnessRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_disparity_metrics(self, *args, **kwargs) -> Any:
        pass


class SQLiteGraphRepository(GraphRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_subgraph(self, *args, **kwargs) -> Any:
        pass


class SQLiteHotspotRepository(HotspotRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_hotspots(self, *args, **kwargs) -> Any:
        pass


class SQLiteIngestionRepository(IngestionRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def ingest_batch(self, *args, **kwargs) -> Any:
        pass


class SQLiteOffenderRepository(OffenderRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_offender_profile(self, *args, **kwargs) -> Any:
        pass


class SQLiteRAGRepository(RAGRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def search_documents(self, *args, **kwargs) -> Any:
        pass


class SQLiteRiskRepository(RiskRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_risk_scores(self, *args, **kwargs) -> Any:
        pass


class SQLiteSocioeconomicRepository(SocioeconomicRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_metrics(self, *args, **kwargs) -> Any:
        pass
