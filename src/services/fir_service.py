from __future__ import annotations

import contextlib
import json
import uuid
from datetime import datetime
from typing import Any

from src.domain.fir_lifecycle import FIRLifecycle
from src.repositories.core import FileStorage, FIRRepository
from src.schemas.fir import FIRCreate, FIRUpdate
from src.services.audit_service import AuditService
from src.services.base import BaseService


class FIRService(BaseService):
    def __init__(self, repo: FIRRepository, storage: FileStorage | None = None):
        super().__init__()
        self.repo = repo
        self.storage = storage

    async def list_firs(
        self,
        page: int = 1,
        page_size: int = 20,
        district_id: int | None = None,
        police_station_id: int | None = None,
        status_id: int | None = None,
    ) -> tuple[list, int]:
        cache_key = f"fir:list:{page}:{page_size}:{district_id}:{police_station_id}:{status_id}"
        cached = await self._cache.get(cache_key)
        if cached is not None:
            ids, total = cached["ids"], cached["total"]
            if ids:
                items = []
                for cid in ids:
                    case = await self.repo.get_fir(cid)
                    if case:
                        items.append(case)
            else:
                items = []
            return items, total

        items, total = await self.repo.list_firs(
            page=page,
            page_size=page_size,
            district_id=district_id,
            police_station_id=police_station_id,
            status_id=status_id,
        )

        await self._cache.set(cache_key, {"ids": [c.CaseMasterID for c in items], "total": total})
        return items, total

    async def get_fir(self, case_master_id: int):
        cache_key = f"fir:detail:{case_master_id}"
        cached = await self._cache.get(cache_key)
        if cached is not None:
            return await self.repo.get_fir(case_master_id)
        case = await self.repo.get_fir(case_master_id)
        if case is not None:
            await self._cache.set(cache_key, {"id": case_master_id})
        return case

    async def create_fir(self, data: FIRCreate, user_id: int | None = None):
        if data.CaseStatusID is None:
            data.CaseStatusID = 1
        case = await self.repo.create_fir(data)

        from src.models.src_models import InvOccuranceTime

        if any([data.BriefFacts, data.Latitude is not None, data.Longitude is not None]):
            occurrence = InvOccuranceTime(
                CaseMasterID=case.CaseMasterID,
                BriefFacts=data.BriefFacts,
                Latitude=data.Latitude,
                Longitude=data.Longitude,
            )
            await self.repo.create_occurrence(occurrence)

        await self.repo.commit()
        await self.repo.refresh(case)
        await self._cache.invalidate("fir:list:*")

        audit_srv = AuditService(self.repo)
        await audit_srv.log(
            user_id=user_id,
            action="CREATE_FIR",
            entity_type="CaseMaster",
            entity_id=case.CaseMasterID,
            new_value=str(data.model_dump(exclude_none=True)),
        )
        return case

    async def update_fir(self, case_master_id: int, data: FIRUpdate, user_id: int | None = None):
        case = await self.repo.get_fir(case_master_id)
        if case is None:
            return None
        old_val = str(
            {k: getattr(case, k, None) for k in data.model_dump(exclude_none=True).keys()}
        )
        case = await self.repo.update_fir(case_master_id, data)
        await self.repo.commit()
        await self.repo.refresh(case)
        await self._cache.invalidate("fir:list:*")
        await self._cache.invalidate(f"fir:detail:{case_master_id}")

        audit_srv = AuditService(self.repo)
        await audit_srv.log(
            user_id=user_id,
            action="UPDATE_FIR",
            entity_type="CaseMaster",
            entity_id=case_master_id,
            old_value=old_val,
            new_value=str(data.model_dump(exclude_none=True)),
        )
        return case

    async def delete_fir(self, case_master_id: int, user_id: int | None = None) -> bool:
        case = await self.repo.get_fir(case_master_id)
        if case is None:
            return False

        await self.repo.delete_occurrence(case_master_id)
        await self.repo.delete_fir(case_master_id)
        await self.repo.commit()
        await self._cache.invalidate("fir:list:*")
        await self._cache.invalidate(f"fir:detail:{case_master_id}")

        audit_srv = AuditService(self.repo)
        await audit_srv.log(
            user_id=user_id,
            action="DELETE_FIR",
            entity_type="CaseMaster",
            entity_id=case_master_id,
        )
        return True

    async def upload_evidence(
        self,
        case_master_id: int,
        filename: str,
        content: bytes,
        mime_type: str,
        description: str | None = None,
        user_id: int | None = None,
    ) -> dict[str, Any]:
        case = await self.repo.get_fir(case_master_id)
        if case is None:
            raise ValueError("FIR not found")

        if not filename or ".." in filename or "/" in filename or "\\" in filename:
            raise ValueError("Invalid filename — path traversal detected")

        storage_path = filename
        if self.storage:
            storage_path = await self.storage.save_file(filename, content, mime_type)

        evidence = await self.repo.create_evidence(
            case_master_id,
            mime_type,
            description or f"Upload: {filename}",
            storage_path,
        )
        await self.repo.commit()
        await self.repo.refresh(evidence)

        audit_srv = AuditService(self.repo)
        await audit_srv.log(
            user_id=user_id,
            action="EVIDENCE_UPLOADED",
            entity_type="EvidenceMaster",
            entity_id=evidence.EvidenceID,
            new_value=f"Evidence {evidence.EvidenceID} uploaded: {filename} ({mime_type})",
        )

        from src.services.event_bus_service import EventBusService
        await EventBusService.get_instance().publish(
            topic="evidence.uploaded",
            payload={
                "evidence_id": evidence.EvidenceID,
                "case_master_id": case_master_id,
                "mime_type": mime_type,
                "description": evidence.Description,
                "storage_path": storage_path,
                "uploaded_by_user_id": user_id,
            },
        )

        return {
            "evidence_id": evidence.EvidenceID,
            "case_master_id": case_master_id,
            "evidence_type": mime_type,
            "description": evidence.Description,
            "storage_path": storage_path,
            "created_at": (
                evidence.CreatedAt.isoformat()
                if hasattr(evidence.CreatedAt, "isoformat")
                else str(evidence.CreatedAt)
            ),
        }

    async def get_evidence(self, case_master_id: int) -> list[dict[str, Any]]:
        items = await self.repo.list_evidence(case_master_id)
        return [
            {
                "evidence_id": e.EvidenceID if hasattr(e, "EvidenceID") else e.get("EvidenceID"),
                "case_master_id": e.CaseMasterID
                if hasattr(e, "CaseMasterID")
                else e.get("CaseMasterID"),
                "evidence_type": e.EvidenceType
                if hasattr(e, "EvidenceType")
                else e.get("EvidenceType"),
                "description": e.Description if hasattr(e, "Description") else e.get("Description"),
                "storage_path": e.StoragePath
                if hasattr(e, "StoragePath")
                else e.get("StoragePath"),
                "status": e.Status if hasattr(e, "Status") else e.get("Status"),
                "sensitivity": e.Sensitivity if hasattr(e, "Sensitivity") else e.get("Sensitivity"),
                "created_at": (
                    e.CreatedAt.isoformat()
                    if hasattr(e, "CreatedAt") and hasattr(e.CreatedAt, "isoformat")
                    else str(e.get("CreatedAt", ""))
                ),
            }
            for e in items
        ]

    # ── Phase 4: Investigation Notes ──
    async def create_note(self, case_master_id: int, author_id: int, content: str, note_type: str = "general", visibility: str = "station") -> dict[str, Any]:
        case = await self.repo.get_fir(case_master_id)
        if case is None:
            raise ValueError("FIR not found")
        note = await self.repo.create_investigation_note(
            case_master_id=case_master_id,
            author_id=author_id,
            content=content,
            note_type=note_type,
            visibility=visibility,
        )
        await self.repo.commit()
        await self.repo.refresh(note)
        audit_srv = AuditService(self.repo)
        await audit_srv.log(
            user_id=author_id,
            action="CREATE_NOTE",
            entity_type="InvestigationNote",
            entity_id=note.NoteID,
            new_value=f"Note created for FIR {case_master_id}",
        )
        return self._note_to_dict(note)

    async def amend_note(self, note_id: int, author_id: int, new_content: str) -> dict[str, Any]:
        original = await self.repo.get_investigation_note(note_id)
        if original is None:
            raise ValueError("Original note not found")
        amendment = await self.repo.create_investigation_note(
            case_master_id=original.CaseMasterID,
            author_id=author_id,
            content=new_content,
            is_amendment=True,
            original_note_id=note_id,
            visibility=original.Visibility,
        )
        await self.repo.commit()
        await self.repo.refresh(amendment)
        audit_srv = AuditService(self.repo)
        await audit_srv.log(
            user_id=author_id,
            action="AMEND_NOTE",
            entity_type="InvestigationNote",
            entity_id=amendment.NoteID,
            new_value=f"Amendment to note {note_id} for FIR {original.CaseMasterID}",
        )
        return self._note_to_dict(amendment)

    async def list_notes(self, case_master_id: int) -> list[dict[str, Any]]:
        notes = await self.repo.list_investigation_notes(case_master_id)
        return [self._note_to_dict(n) for n in notes]

    def _note_to_dict(self, note: Any) -> dict[str, Any]:
        return {
            "NoteID": note.NoteID,
            "CaseMasterID": note.CaseMasterID,
            "AuthorID": note.AuthorID,
            "NoteType": note.NoteType,
            "Content": note.Content,
            "IsAmendment": note.IsAmendment,
            "OriginalNoteID": note.OriginalNoteID,
            "Visibility": note.Visibility,
            "CreatedAt": note.CreatedAt.isoformat() if hasattr(note.CreatedAt, "isoformat") else str(note.CreatedAt),
            "UpdatedAt": note.UpdatedAt.isoformat() if hasattr(note.UpdatedAt, "isoformat") else str(note.UpdatedAt),
        }

    # ── Phase 4: Case Assignment ──
    async def assign_officer(self, case_master_id: int, assigned_officer_id: int, assigned_by_user_id: int, reason: str | None = None) -> dict[str, Any]:
        case = await self.repo.get_fir(case_master_id)
        if case is None:
            raise ValueError("FIR not found")
        assignment = await self.repo.create_assignment(
            case_master_id=case_master_id,
            assigned_officer_id=assigned_officer_id,
            assigned_by_user_id=assigned_by_user_id,
            reason=reason,
        )
        await self.repo.commit()
        await self.repo.refresh(assignment)
        audit_srv = AuditService(self.repo)
        await audit_srv.log(
            user_id=assigned_by_user_id,
            action="ASSIGN_OFFICER",
            entity_type="CaseAssignment",
            entity_id=assignment.AssignmentID,
            new_value=f"Officer {assigned_officer_id} assigned to FIR {case_master_id}",
        )
        from src.services.event_bus_service import EventBusService
        await EventBusService.get_instance().publish(
            topic="case.assigned",
            payload={
                "assignment_id": assignment.AssignmentID,
                "case_master_id": case_master_id,
                "assigned_officer_id": assigned_officer_id,
                "assigned_by_user_id": assigned_by_user_id,
                "reason": reason,
                "status": assignment.Status,
            },
        )
        return self._assignment_to_dict(assignment)

    async def list_assignments(self, case_master_id: int) -> list[dict[str, Any]]:
        assignments = await self.repo.list_assignments(case_master_id)
        return [self._assignment_to_dict(a) for a in assignments]

    async def get_active_assignment(self, case_master_id: int) -> dict[str, Any] | None:
        a = await self.repo.get_active_assignment(case_master_id)
        return self._assignment_to_dict(a) if a else None

    def _assignment_to_dict(self, a: Any) -> dict[str, Any]:
        return {
            "AssignmentID": a.AssignmentID,
            "CaseMasterID": a.CaseMasterID,
            "AssignedOfficerID": a.AssignedOfficerID,
            "AssignedByUserID": a.AssignedByUserID,
            "AssignmentReason": a.AssignmentReason,
            "Status": a.Status,
            "AssignedAt": a.AssignedAt.isoformat() if hasattr(a.AssignedAt, "isoformat") else str(a.AssignedAt),
            "EndedAt": a.EndedAt.isoformat() if a.EndedAt and hasattr(a.EndedAt, "isoformat") else (str(a.EndedAt) if a.EndedAt else None),
        }

    # ── Phase 4: Status Transitions ──
    async def update_case_status(self, case_master_id: int, new_status_id: int, user_id: int, reason: str | None = None) -> dict[str, Any]:
        case = await self.repo.get_fir(case_master_id)
        if case is None:
            raise ValueError("FIR not found")
        old_status = case.CaseStatusID
        if old_status == new_status_id:
            return {"CaseMasterID": case_master_id, "caseMasterID": case_master_id, "OldStatusID": old_status, "oldStatusID": old_status, "NewStatusID": new_status_id, "newStatusID": new_status_id, "Changed": False, "changed": False}

        active_assign = await self.repo.get_active_assignment(case_master_id)
        has_assignment = active_assign is not None
        is_supervisor = getattr(case, "_supervisor", False)

        result = FIRLifecycle.validate_transition(
            current_status_id=old_status,
            new_status_id=new_status_id,
            has_assignment=has_assignment,
            is_supervisor=is_supervisor,
        )
        if not result.allowed:
            raise ValueError(result.reason or f"Invalid status transition from {old_status} to {new_status_id}")

        case.CaseStatusID = new_status_id
        await self.repo.commit()
        await self._cache.invalidate(f"fir:detail:{case_master_id}")
        await self._cache.invalidate("fir:list:*")
        audit_srv = AuditService(self.repo)
        await audit_srv.log(
            user_id=user_id,
            action="UPDATE_STATUS",
            entity_type="CaseMaster",
            entity_id=case_master_id,
            old_value=str(old_status),
            new_value=str(new_status_id),
        )
        return {"CaseMasterID": case_master_id, "caseMasterID": case_master_id, "OldStatusID": old_status, "oldStatusID": old_status, "NewStatusID": new_status_id, "newStatusID": new_status_id, "Changed": True, "changed": True, "warnings": result.warnings}

    # ── Phase 4: Supervisor Review ──
    async def create_review(self, case_master_id: int, supervisor_id: int, review_type: str, status: str, comments: str | None = None, action_requested: str | None = None) -> dict[str, Any]:
        case = await self.repo.get_fir(case_master_id)
        if case is None:
            raise ValueError("FIR not found")
        review = await self.repo.create_supervisor_review(
            case_master_id=case_master_id,
            supervisor_id=supervisor_id,
            review_type=review_type,
            status=status,
            comments=comments,
            action_requested=action_requested,
        )
        await self.repo.commit()
        await self.repo.refresh(review)
        audit_srv = AuditService(self.repo)
        await audit_srv.log(
            user_id=supervisor_id,
            action="SUPERVISOR_REVIEW",
            entity_type="SupervisorReview",
            entity_id=review.ReviewID,
            new_value=f"Review {status} for FIR {case_master_id}",
        )
        from src.services.event_bus_service import EventBusService
        await EventBusService.get_instance().publish(
            topic="supervisor.review.created",
            payload={
                "review_id": review.ReviewID,
                "case_master_id": case_master_id,
                "supervisor_id": supervisor_id,
                "review_type": review_type,
                "status": status,
                "comments": comments,
                "action_requested": action_requested,
            },
        )
        return self._review_to_dict(review)

    async def list_reviews(self, case_master_id: int) -> list[dict[str, Any]]:
        reviews = await self.repo.list_supervisor_reviews(case_master_id)
        return [self._review_to_dict(r) for r in reviews]

    def _review_to_dict(self, r: Any) -> dict[str, Any]:
        return {
            "ReviewID": r.ReviewID,
            "CaseMasterID": r.CaseMasterID,
            "SupervisorID": r.SupervisorID,
            "ReviewType": r.ReviewType,
            "Status": r.Status,
            "Comments": r.Comments,
            "ActionRequested": r.ActionRequested,
            "ReviewedAt": r.ReviewedAt.isoformat() if hasattr(r.ReviewedAt, "isoformat") else str(r.ReviewedAt),
        }

    # ── Phase 4: Timeline ──
    async def get_timeline(self, case_master_id: int) -> list[dict[str, Any]]:
        return await self.repo.get_timeline_events(case_master_id)

    # ── Phase 4: Related Case Suggestions ──
    async def generate_related_cases(self, case_master_id: int) -> list[dict[str, Any]]:
        case = await self.repo.get_fir(case_master_id)
        if case is None:
            raise ValueError("FIR not found")
        existing = await self.repo.list_related_case_suggestions(case_master_id)
        if existing:
            return [self._suggestion_to_dict(s) for s in existing]

        all_cases, _ = await self.repo.list_firs(page=1, page_size=500)
        suggestions = []
        computed = 0
        signals = []

        for other in all_cases:
            if other.CaseMasterID == case_master_id:
                continue
            signals = []
            score = 0.0

            if case.CrimeMajorHeadID and other.CrimeMajorHeadID and case.CrimeMajorHeadID == other.CrimeMajorHeadID:
                signals.append("Same crime category")
                score += 0.2

            if (case.PoliceStationID and other.PoliceStationID and case.PoliceStationID == other.PoliceStationID):
                signals.append("Same police station")
                score += 0.15

            if signals and score >= 0.15:
                suggestion = await self.repo.create_related_case_suggestion(
                    source_fir_id=case_master_id,
                    candidate_fir_id=other.CaseMasterID,
                    confidence_score=min(score, 0.95),
                    supporting_signals=json.dumps(signals),
                    explanation="; ".join(signals),
                )
                await self.repo.commit()
                await self.repo.refresh(suggestion)
                suggestions.append(suggestion)
                computed += 1
                if computed >= 20:
                    break

        return [self._suggestion_to_dict(s) for s in suggestions]

    async def list_related_cases(self, case_master_id: int) -> list[dict[str, Any]]:
        suggestions = await self.repo.list_related_case_suggestions(case_master_id)
        results = []
        for s in suggestions:
            d = self._suggestion_to_dict(s)
            candidate = await self.repo.get_fir(s.CandidateFIRID if s.SourceFIRID == case_master_id else s.SourceFIRID)
            if candidate:
                d["candidate_crime_no"] = candidate.CrimeNo
                d["candidate_status_id"] = candidate.CaseStatusID
            results.append(d)
        return results

    async def review_related_case(self, suggestion_id: int, review_status: str, reviewed_by_user_id: int, review_reason: str | None = None) -> dict[str, Any]:
        suggestion = await self.repo.update_suggestion_review(
            suggestion_id=suggestion_id,
            review_status=review_status,
            reviewed_by_user_id=reviewed_by_user_id,
            review_reason=review_reason,
        )
        if suggestion is None:
            raise ValueError("Suggestion not found")
        await self.repo.commit()
        audit_srv = AuditService(self.repo)
        await audit_srv.log(
            user_id=reviewed_by_user_id,
            action="REVIEW_RELATED_CASE",
            entity_type="RelatedCaseSuggestion",
            entity_id=suggestion_id,
            new_value=f"Suggestion {review_status} by user {reviewed_by_user_id}",
        )
        from src.services.event_bus_service import EventBusService
        await EventBusService.get_instance().publish(
            topic="supervisor.review.created",
            payload={
                "suggestion_id": suggestion_id,
                "review_status": review_status,
                "reviewed_by_user_id": reviewed_by_user_id,
                "review_reason": review_reason,
                "review_type": "related_case_suggestion",
            },
        )
        return self._suggestion_to_dict(suggestion)

    def _suggestion_to_dict(self, s: Any) -> dict[str, Any]:
        return {
            "SuggestionID": s.SuggestionID,
            "SourceFIRID": s.SourceFIRID,
            "CandidateFIRID": s.CandidateFIRID,
            "ConfidenceScore": s.ConfidenceScore,
            "SupportingSignals": s.SupportingSignals,
            "Explanation": s.Explanation,
            "ModelVersion": s.ModelVersion,
            "ReviewStatus": s.ReviewStatus,
            "ReviewedByUserID": s.ReviewedByUserID,
            "ReviewReason": s.ReviewReason,
            "ReviewedAt": s.ReviewedAt.isoformat() if s.ReviewedAt and hasattr(s.ReviewedAt, "isoformat") else (str(s.ReviewedAt) if s.ReviewedAt else None),
            "CreatedAt": s.CreatedAt.isoformat() if hasattr(s.CreatedAt, "isoformat") else str(s.CreatedAt),
            "CandidateCrimeNo": None,
            "CandidateStatusID": None,
        }

    # ── Phase 4: Vehicles ──
    async def list_vehicles(self, case_master_id: int) -> list[dict[str, Any]]:
        vehicles = await self.repo.list_vehicles(case_master_id)
        return [
            {
                "VehicleLinkID": v.VehicleLinkID,
                "VehicleNumber": v.VehicleNumber,
                "CaseMasterID": v.CaseMasterID,
                "Confidence": v.Confidence,
                "Source": v.Source,
                "CreatedAt": v.CreatedAt.isoformat() if hasattr(v.CreatedAt, "isoformat") else str(v.CreatedAt),
            }
            for v in vehicles
        ]

    async def add_vehicle(self, case_master_id: int, vehicle_number: str, source: str = "manual", confidence: float = 1.0) -> dict[str, Any]:
        case = await self.repo.get_fir(case_master_id)
        if case is None:
            raise ValueError("FIR not found")
        link = await self.repo.create_vehicle_link(
            case_master_id=case_master_id,
            vehicle_number=vehicle_number,
            source=source,
            confidence=confidence,
        )
        await self.repo.commit()
        await self.repo.refresh(link)
        audit_srv = AuditService(self.repo)
        await audit_srv.log(
            user_id=None,
            action="ADD_VEHICLE",
            entity_type="VehicleLink",
            entity_id=link.VehicleLinkID,
            new_value=f"Vehicle {vehicle_number} linked to FIR {case_master_id}",
        )
        return {
            "VehicleLinkID": link.VehicleLinkID,
            "VehicleNumber": link.VehicleNumber,
            "CaseMasterID": link.CaseMasterID,
            "Confidence": link.Confidence,
            "Source": link.Source,
            "CreatedAt": link.CreatedAt.isoformat() if hasattr(link.CreatedAt, "isoformat") else str(link.CreatedAt),
        }

    # ── Phase 4: Dashboard ──
    async def get_dashboard_metrics(self, district_id: int | None = None, police_station_id: int | None = None, user_id: int | None = None) -> dict[str, Any]:
        metrics = await self.repo.get_dashboard_metrics(
            district_id=district_id,
            police_station_id=police_station_id,
        )
        if user_id:
            assigned_firs, _ = await self.repo.list_firs(page=1, page_size=1, assigned_officer_id=user_id)
            metrics["assigned_to_me_count"] = assigned_firs[0] if assigned_firs else 0
        return metrics

    # ── Phase 4: Reports ──
    async def request_report(self, requested_by_user_id: int, report_type: str, parameters: str | None = None, file_format: str = "pdf") -> dict[str, Any]:
        report_id = f"RPT-{uuid.uuid4().hex[:12].upper()}"
        req = await self.repo.create_report_request(
            report_id=report_id,
            requested_by_user_id=requested_by_user_id,
            report_type=report_type,
            parameters=parameters,
            file_format=file_format,
        )
        await self.repo.commit()
        await self.repo.refresh(req)
        audit_srv = AuditService(self.repo)
        await audit_srv.log(
            user_id=requested_by_user_id,
            action="REQUEST_REPORT",
            entity_type="ReportRequest",
            entity_id=report_id,
            new_value=f"Report {report_type} requested",
        )
        return self._report_to_dict(req)

    async def list_reports(self, user_id: int | None = None) -> list[dict[str, Any]]:
        reports = await self.repo.list_report_requests(user_id=user_id)
        return [self._report_to_dict(r) for r in reports]

    async def get_report(self, report_id: str) -> dict[str, Any] | None:
        r = await self.repo.get_report_request(report_id)
        return self._report_to_dict(r) if r else None

    def _report_to_dict(self, r: Any) -> dict[str, Any]:
        return {
            "ReportID": r.ReportID,
            "RequestedByUserID": r.RequestedByUserID,
            "ReportType": r.ReportType,
            "Parameters": r.Parameters,
            "Status": r.Status,
            "StorageObjectRef": r.StorageObjectRef,
            "FileFormat": r.FileFormat,
            "ErrorMessage": r.ErrorMessage,
            "CreatedAt": r.CreatedAt.isoformat() if hasattr(r.CreatedAt, "isoformat") else str(r.CreatedAt),
            "CompletedAt": r.CompletedAt.isoformat() if r.CompletedAt and hasattr(r.CompletedAt, "isoformat") else (str(r.CompletedAt) if r.CompletedAt else None),
            "ExpiresAt": r.ExpiresAt.isoformat() if r.ExpiresAt and hasattr(r.ExpiresAt, "isoformat") else (str(r.ExpiresAt) if r.ExpiresAt else None),
        }

    async def generate_report_content(self, report_id: str) -> dict[str, Any]:
        req = await self.repo.get_report_request(report_id)
        if req is None:
            raise ValueError("Report request not found")
        params = {}
        if req.Parameters:
            with contextlib.suppress(json.JSONDecodeError):
                params = json.loads(req.Parameters)
        content_data: dict[str, Any] = {}
        if req.ReportType == "fir_summary":
            case_id = params.get("case_master_id")
            if case_id:
                case = await self.repo.get_fir(int(case_id))
                if case:
                    content_data = {"crime_no": case.CrimeNo, "status_id": case.CaseStatusID, "station_id": case.PoliceStationID}
        elif req.ReportType == "investigation_progress":
            case_id = params.get("case_master_id")
            if case_id:
                notes = await self.repo.list_investigation_notes(int(case_id))
                content_data = {"notes_count": len(notes), "latest_note": notes[0].Content if notes else None}
        elif req.ReportType == "evidence_inventory":
            case_id = params.get("case_master_id")
            if case_id:
                evs = await self.repo.list_evidence(int(case_id))
                content_data = {"evidence_count": len(evs), "items": [{"id": e.EvidenceID, "type": e.EvidenceType, "status": e.Status} for e in evs]}

        await self.repo.update_report_request(report_id, status="completed", storage_object_ref=f"reports/{report_id}.{req.FileFormat}")
        await self.repo.commit()
        return {
            "report_id": report_id,
            "report_type": req.ReportType,
            "generated_at": datetime.utcnow().isoformat(),
            "generated_by": getattr(req, "RequestedByUserID", 0) or 0,
            "content": content_data,
            "data": content_data,
            "is_synthetic_data": True,
        }
