"""Unit tests for Stage 4: AI Extraction and Suggestion Review Lifecycle."""

import json
from unittest.mock import AsyncMock, MagicMock

import pytest

from src.models.int_models import AIExtractionQueue
from src.models.src_models import CaseMaster
from src.services.ai_assistant_service import AIAssistantService


class AsyncMockSession:
    def __init__(self):
        self.execute = AsyncMock()
        self.get = AsyncMock()
        self.flush = AsyncMock()
        self.commit = AsyncMock()
        self.refresh = AsyncMock()
        self.add = MagicMock()
        self.delete = AsyncMock()

    def _make_scalar_result(self, scalar_one_val=None):
        res = MagicMock()
        res.scalar_one_or_none.return_value = scalar_one_val
        res.scalar_one.return_value = scalar_one_val
        return res


@pytest.mark.asyncio
async def test_ai_extraction_creates_pending_suggestion():
    session = AsyncMockSession()
    # Mock finding CaseMaster
    mock_case = CaseMaster(CaseMasterID=101, CrimeNo="CR-2026-001", CrimeMajorHeadID=10)
    session.execute.return_value = session._make_scalar_result(scalar_one_val=mock_case)

    svc = AIAssistantService(session)
    # First check existing returns None, second check loads case
    session.execute.side_effect = [
        session._make_scalar_result(scalar_one_val=None),
        session._make_scalar_result(scalar_one_val=mock_case),
    ]

    entry = await svc.extract_suggestions(101)
    assert entry.CaseMasterID == 101
    assert entry.Status == "PENDING"
    assert "suggested_crime_head" in entry.RawJSON
    assert session.add.called
    assert session.commit.called


@pytest.mark.asyncio
async def test_apply_suggestion_logs_audit_and_updates_status():
    session = AsyncMockSession()
    mock_entry = AIExtractionQueue(
        ExtractionID=1,
        CaseMasterID=101,
        Status="PENDING",
        RawJSON=json.dumps({"suggested_crime_head": "Cyber Crime"}),
    )
    session.execute.return_value = session._make_scalar_result(scalar_one_val=mock_entry)

    svc = AIAssistantService(session)
    entry = await svc.apply_suggestion(1, reviewer_id=5, comments="Verified accurate")
    assert entry is not None
    assert entry.Status == "APPROVED"
    assert entry.ReviewedBy == 5
    assert session.commit.called


@pytest.mark.asyncio
async def test_reject_suggestion_updates_status():
    session = AsyncMockSession()
    mock_entry = AIExtractionQueue(
        ExtractionID=1,
        CaseMasterID=101,
        Status="PENDING",
        RawJSON=json.dumps({"suggested_crime_head": "Cyber Crime"}),
    )
    session.execute.return_value = session._make_scalar_result(scalar_one_val=mock_entry)

    svc = AIAssistantService(session)
    entry = await svc.reject_suggestion(1, reviewer_id=5, comments="Incorrect entities")
    assert entry is not None
    assert entry.Status == "REJECTED"
    assert entry.ReviewedBy == 5
    assert session.commit.called
