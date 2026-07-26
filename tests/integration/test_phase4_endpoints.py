"""Integration tests for Phase 4 MVP endpoints across Workstreams A-F."""

from datetime import datetime
from unittest.mock import AsyncMock, MagicMock

import jwt
import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_session
from src.dependencies import get_audit_repo, get_auth_repo, get_entity_repo, get_fir_repo
from src.main import app
from src.middleware.auth import JWT_SECRET
from src.repositories.sqlite_adapter import (
    SQLiteAuditRepository,
    SQLiteAuthRepository,
    SQLiteEntityRepository,
    SQLiteFIRRepository,
)

AUTH_HEADER = {
    "Authorization": f"Bearer {jwt.encode({'user_id': 1, 'role': 'admin'}, JWT_SECRET, algorithm='HS256')}"
}


class MockModel:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


@pytest.fixture
def mock_session():
    session = AsyncMock(spec=AsyncSession)
    session.execute = AsyncMock(return_value=_make_result(scalars_all=[], scalar_one_val=0))
    session.get = AsyncMock(return_value=None)
    session.flush = AsyncMock()
    session.commit = AsyncMock()
    session.refresh = AsyncMock()
    session.add = MagicMock()
    session.delete = AsyncMock()
    return session


@pytest.fixture
def client(mock_session):
    async def override_get_session():
        yield mock_session

    def override_get_fir_repo(request=None):
        return SQLiteFIRRepository(mock_session)

    def override_get_auth_repo(request=None):
        return SQLiteAuthRepository(mock_session)

    def override_get_entity_repo(request=None):
        return SQLiteEntityRepository(mock_session)

    def override_get_audit_repo(request=None):
        return SQLiteAuditRepository(mock_session)

    app.dependency_overrides[get_session] = override_get_session
    app.dependency_overrides[get_fir_repo] = override_get_fir_repo
    app.dependency_overrides[get_auth_repo] = override_get_auth_repo
    app.dependency_overrides[get_entity_repo] = override_get_entity_repo
    app.dependency_overrides[get_audit_repo] = override_get_audit_repo
    transport = ASGITransport(app=app)
    client = AsyncClient(transport=transport, base_url="http://test")
    yield client
    app.dependency_overrides.clear()


def _make_result(scalar_one_val=None, scalars_all=None, scalar_one_or_none=None):
    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = scalars_all or []
    mock_result.scalar_one.return_value = scalar_one_val
    mock_result.scalar_one_or_none.return_value = scalar_one_or_none or None
    return mock_result


def _setup_refresh(mock_session):
    def fake_refresh(obj):
        if not hasattr(obj, "NoteID") or obj.NoteID is None:
            setattr(obj, "NoteID", 101)
        if not hasattr(obj, "AssignmentID") or obj.AssignmentID is None:
            setattr(obj, "AssignmentID", 201)
        if not hasattr(obj, "ReviewID") or obj.ReviewID is None:
            setattr(obj, "ReviewID", 301)
        if not hasattr(obj, "SuggestionID") or obj.SuggestionID is None:
            setattr(obj, "SuggestionID", 401)
        if not hasattr(obj, "CreatedAt") or obj.CreatedAt is None:
            setattr(obj, "CreatedAt", datetime.utcnow())
        if not hasattr(obj, "UpdatedAt") or obj.UpdatedAt is None:
            setattr(obj, "UpdatedAt", datetime.utcnow())
        if not hasattr(obj, "AssignedAt") or obj.AssignedAt is None:
            setattr(obj, "AssignedAt", datetime.utcnow())
        if not hasattr(obj, "ReviewedAt") or obj.ReviewedAt is None:
            setattr(obj, "ReviewedAt", datetime.utcnow())
    mock_session.refresh.side_effect = fake_refresh


# ── Workstream A: Investigation Workflow ──

@pytest.mark.asyncio
async def test_create_investigation_note(client, mock_session):
    _setup_refresh(mock_session)
    mock_case = MockModel(CaseMasterID=1, CrimeNo="CR-2026-001", PoliceStationID=10, CaseStatusID=1)
    mock_session.execute = AsyncMock(return_value=_make_result(scalar_one_or_none=mock_case))

    async with client as ac:
        resp = await ac.post(
            "/api/v1/fir/1/notes",
            json={"Content": "Witness interview recorded at station.", "NoteType": "witness_statement", "Visibility": "station"},
            headers=AUTH_HEADER,
        )
    assert resp.status_code == 201
    data = resp.json()
    assert data["content"] == "Witness interview recorded at station."
    assert data["noteType"] == "witness_statement"
    assert data["noteID"] == 101


@pytest.mark.asyncio
async def test_list_investigation_notes(client, mock_session):
    mock_note = MockModel(
        NoteID=101,
        CaseMasterID=1,
        AuthorID=1,
        NoteType="general",
        Content="Initial site visit.",
        IsAmendment=False,
        OriginalNoteID=None,
        Visibility="station",
        CreatedAt=datetime.utcnow(),
        UpdatedAt=datetime.utcnow(),
    )
    mock_session.execute = AsyncMock(return_value=_make_result(scalars_all=[mock_note]))

    async with client as ac:
        resp = await ac.get("/api/v1/fir/1/notes", headers=AUTH_HEADER)
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 1
    assert data[0]["noteID"] == 101
    assert data[0]["content"] == "Initial site visit."


@pytest.mark.asyncio
async def test_assign_officer(client, mock_session):
    _setup_refresh(mock_session)
    mock_case = MockModel(CaseMasterID=1, CrimeNo="CR-2026-001", PoliceStationID=10, CaseStatusID=1)
    mock_session.execute = AsyncMock(return_value=_make_result(scalar_one_or_none=mock_case))

    async with client as ac:
        resp = await ac.post(
            "/api/v1/fir/1/assignments",
            json={"AssignedOfficerID": 501, "AssignmentReason": "Specialized cyber crime investigation required."},
            headers=AUTH_HEADER,
        )
    assert resp.status_code == 201
    data = resp.json()
    assert data["assignedOfficerID"] == 501
    assert data["status"] == "active"


@pytest.mark.asyncio
async def test_list_assignments(client, mock_session):
    mock_assign = MockModel(
        AssignmentID=201,
        CaseMasterID=1,
        AssignedOfficerID=501,
        AssignedByUserID=1,
        AssignmentReason="Specialized investigation.",
        Status="active",
        AssignedAt=datetime.utcnow(),
        EndedAt=None,
    )
    mock_session.execute = AsyncMock(return_value=_make_result(scalars_all=[mock_assign]))

    async with client as ac:
        resp = await ac.get("/api/v1/fir/1/assignments", headers=AUTH_HEADER)
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 1
    assert data[0]["assignedOfficerID"] == 501


@pytest.mark.asyncio
async def test_get_active_assignment(client, mock_session):
    mock_assign = MockModel(
        AssignmentID=201,
        CaseMasterID=1,
        AssignedOfficerID=501,
        AssignedByUserID=1,
        AssignmentReason="Specialized investigation.",
        Status="active",
        AssignedAt=datetime.utcnow(),
        EndedAt=None,
    )
    mock_session.execute = AsyncMock(return_value=_make_result(scalar_one_or_none=mock_assign))

    async with client as ac:
        resp = await ac.get("/api/v1/fir/1/assignment/active", headers=AUTH_HEADER)
    assert resp.status_code == 200
    data = resp.json()
    assert data["assignedOfficerID"] == 501


@pytest.mark.asyncio
async def test_update_status(client, mock_session):
    mock_case = MockModel(
        CaseMasterID=1,
        CrimeNo="CR-2026-001",
        PoliceStationID=10,
        CaseStatusID=1,
        BriefFacts="Vehicle theft",
        CrimeRegisteredDate=datetime.utcnow(),
        DistrictID=5,
    )
    mock_session.execute = AsyncMock(return_value=_make_result(scalar_one_or_none=mock_case))
    mock_session.get.return_value = mock_case

    async with client as ac:
        resp = await ac.put(
            "/api/v1/fir/1/status",
            json={"CaseStatusID": 3, "Reason": "Chargesheet filed."},
            headers=AUTH_HEADER,
        )
    assert resp.status_code == 200
    data = resp.json()
    assert data["OldStatusID"] == 1
    assert data["NewStatusID"] == 3


@pytest.mark.asyncio
async def test_create_supervisor_review(client, mock_session):
    _setup_refresh(mock_session)
    mock_case = MockModel(CaseMasterID=1, CrimeNo="CR-2026-001", PoliceStationID=10, CaseStatusID=1)
    mock_session.execute = AsyncMock(return_value=_make_result(scalar_one_or_none=mock_case))

    async with client as ac:
        resp = await ac.post(
            "/api/v1/fir/1/reviews",
            json={"ReviewType": "progress_review", "Status": "approved", "Comments": "Proceed with suspect arrest."},
            headers=AUTH_HEADER,
        )
    assert resp.status_code == 201
    data = resp.json()
    assert data["status"] == "approved"
    assert data["comments"] == "Proceed with suspect arrest."


@pytest.mark.asyncio
async def test_get_timeline(client, mock_session):
    mock_case = MockModel(CaseMasterID=1, CrimeNo="CR-2026-001", CrimeRegisteredDate=datetime.utcnow())
    mock_session.get.return_value = mock_case
    mock_session.execute = AsyncMock(return_value=_make_result(scalars_all=[]))

    async with client as ac:
        resp = await ac.get("/api/v1/fir/1/timeline", headers=AUTH_HEADER)
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) >= 1
    assert data[0]["type"] == "FIR_REGISTERED"


# ── Workstream C: Related Case Discovery ──

@pytest.mark.asyncio
async def test_list_related_cases(client, mock_session):
    mock_sugg = MockModel(
        SuggestionID=401,
        SourceFIRID=1,
        CandidateFIRID=2,
        ConfidenceScore=0.88,
        SupportingSignals="Matching MO and vehicle number.",
        Explanation="High similarity in vehicle theft pattern.",
        ModelVersion="hybrid-v1.0",
        ReviewStatus="suggested",
        ReviewedByUserID=None,
        ReviewReason=None,
        ReviewedAt=None,
        CreatedAt=datetime.utcnow(),
    )
    mock_session.execute = AsyncMock(return_value=_make_result(scalars_all=[mock_sugg]))

    async with client as ac:
        resp = await ac.get("/api/v1/fir/1/related-cases", headers=AUTH_HEADER)
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 1
    assert data[0]["suggestionID"] == 401
    assert data[0]["confidenceScore"] == 0.88


@pytest.mark.asyncio
async def test_review_related_case(client, mock_session):
    mock_sugg = MockModel(
        SuggestionID=401,
        SourceFIRID=1,
        CandidateFIRID=2,
        ConfidenceScore=0.88,
        SupportingSignals="Matching MO.",
        Explanation="Similarity found.",
        ModelVersion="hybrid-v1.0",
        ReviewStatus="suggested",
        ReviewedByUserID=None,
        ReviewReason=None,
        ReviewedAt=None,
        CreatedAt=datetime.utcnow(),
    )
    mock_session.execute = AsyncMock(return_value=_make_result(scalar_one_or_none=mock_sugg))

    async with client as ac:
        resp = await ac.put(
            "/api/v1/fir/related-cases/401/review",
            json={"ReviewStatus": "accepted", "ReviewReason": "Verified by IO."},
            headers=AUTH_HEADER,
        )
    assert resp.status_code == 200
    data = resp.json()
    assert data["reviewStatus"] == "accepted"


# ── Workstream D: Dashboards & Analytics ──

@pytest.mark.asyncio
async def test_officer_dashboard(client, mock_session):
    mock_session.execute = AsyncMock(return_value=_make_result(scalar_one_val=10))

    async with client as ac:
        resp = await ac.get("/api/v1/dashboard/officer", headers=AUTH_HEADER)
    assert resp.status_code == 200
    data = resp.json()
    assert "totalFirs" in data
    assert "statusCounts" in data


@pytest.mark.asyncio
async def test_supervisor_dashboard(client, mock_session):
    mock_session.execute = AsyncMock(return_value=_make_result(scalar_one_val=25))

    async with client as ac:
        resp = await ac.get("/api/v1/dashboard/supervisor", headers=AUTH_HEADER)
    assert resp.status_code == 200
    data = resp.json()
    assert "totalFirs" in data


# ── Workstream E: Reporting Engine ──

@pytest.mark.asyncio
async def test_create_report_request(client, mock_session):
    _setup_refresh(mock_session)
    async with client as ac:
        resp = await ac.post(
            "/api/v1/reports",
            json={"ReportType": "fir_summary", "Parameters": '{"case_master_id": 1}', "FileFormat": "pdf"},
            headers=AUTH_HEADER,
        )
    assert resp.status_code == 201
    data = resp.json()
    assert data["reportType"] == "fir_summary"
    assert data["status"] == "requested"


@pytest.mark.asyncio
async def test_list_reports(client, mock_session):
    mock_req = MockModel(
        ReportID="RPT-20260726-101",
        RequestedByUserID=1,
        ReportType="fir_summary",
        Parameters='{"case_master_id": 1}',
        Status="completed",
        StorageObjectRef="reports/RPT-20260726-101.pdf",
        FileFormat="pdf",
        ErrorMessage=None,
        CreatedAt=datetime.utcnow(),
        CompletedAt=datetime.utcnow(),
        ExpiresAt=None,
    )
    mock_session.execute = AsyncMock(return_value=_make_result(scalars_all=[mock_req]))

    async with client as ac:
        resp = await ac.get("/api/v1/reports", headers=AUTH_HEADER)
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 1
    assert data[0]["reportID"] == "RPT-20260726-101"


# ── Workstream F: Search Engine ──

@pytest.mark.asyncio
async def test_search_firs(client, mock_session):
    mock_case = MockModel(
        CaseMasterID=1,
        CrimeNo="CR-2026-001",
        CrimeRegisteredDate=datetime.utcnow().date(),
        PoliceStationID=10,
        CaseStatusID=1,
        BriefFacts="Theft reported near MG Road.",
    )
    mock_session.execute = AsyncMock(return_value=_make_result(scalar_one_val=1, scalars_all=[mock_case]))

    async with client as ac:
        resp = await ac.post(
            "/api/v1/search",
            json={"query": "theft", "page": 1, "page_size": 10},
            headers=AUTH_HEADER,
        )
    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] == 1
    assert len(data["items"]) == 1
    assert data["items"][0]["crimeNo"] == "CR-2026-001"
