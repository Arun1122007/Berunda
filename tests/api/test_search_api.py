"""Integration tests for Search API endpoints using mocked session."""

from __future__ import annotations

from datetime import date
from unittest.mock import AsyncMock, MagicMock

import jwt
import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from src.config import settings
from src.database import get_session
from src.dependencies import get_fir_repo
from src.main import app
from src.repositories.sqlite_adapter import SQLiteFIRRepository

JWT_SECRET = settings.JWT_SECRET


def make_token(role: str, user_id: int = 1, **extra) -> str:
    import time
    payload = {
        "id": user_id,
        "user_id": user_id,
        "role": role,
        "district_id": extra.get("district_id", 1),
        "police_station_id": extra.get("police_station_id", 5),
        "sub": f"user-{user_id}",
        "iat": int(time.time()),
        "exp": int(time.time()) + 3600,
    }
    payload.update(extra)
    return jwt.encode(payload, JWT_SECRET, algorithm="HS256")


class MockModel:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


def make_result(scalar_one_val=None, scalars_all=None, scalar_one_or_none=None):
    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = scalars_all or []
    mock_result.scalar_one.return_value = scalar_one_val
    mock_result.scalar_one_or_none.return_value = scalar_one_or_none or None
    return mock_result


@pytest.fixture
def mock_session():
    session = AsyncMock(spec=AsyncSession)
    session.execute = AsyncMock(return_value=make_result(scalars_all=[], scalar_one_val=0))
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

    app.dependency_overrides[get_session] = override_get_session
    app.dependency_overrides[get_fir_repo] = override_get_fir_repo
    transport = ASGITransport(app=app)
    client = AsyncClient(transport=transport, base_url="http://test")
    yield client
    app.dependency_overrides.clear()


@pytest.mark.integration
class TestSearchAPI:
    @pytest.mark.asyncio
    async def test_search_empty(self, client, mock_session):
        token = make_token("admin")
        async with client as ac:
            response = await ac.post(
                "/api/v1/search",
                json={},
                headers={"Authorization": f"Bearer {token}"},
            )
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 0
        assert data["items"] == []
        assert data["page"] == 1
        assert data["pageSize"] == 20

    @pytest.mark.asyncio
    async def test_search_all(self, client, mock_session):
        mock_session.execute.return_value = make_result(
            scalars_all=[
                MockModel(CaseMasterID=1, CrimeNo="CR-2026-SRC-001", CaseStatusID=1, PoliceStationID=5, CrimeRegisteredDate=date(2026, 1, 15), occurrence=None),
                MockModel(CaseMasterID=2, CrimeNo="CR-2026-SRC-002", CaseStatusID=2, PoliceStationID=5, CrimeRegisteredDate=date(2026, 2, 10), occurrence=None),
            ],
            scalar_one_val=2,
        )
        token = make_token("admin")
        async with client as ac:
            response = await ac.post(
                "/api/v1/search",
                json={},
                headers={"Authorization": f"Bearer {token}"},
            )
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 2
        assert len(data["items"]) == 2

    @pytest.mark.asyncio
    async def test_search_by_crime_no(self, client, mock_session):
        mock_session.execute.return_value = make_result(
            scalars_all=[
                MockModel(CaseMasterID=1, CrimeNo="CR-2026-SRC-001", CaseStatusID=1, PoliceStationID=5, CrimeRegisteredDate=date(2026, 1, 15), occurrence=None),
            ],
            scalar_one_val=1,
        )
        token = make_token("admin")
        async with client as ac:
            response = await ac.post(
                "/api/v1/search",
                json={"crimeNo": "CR-2026-SRC-001"},
                headers={"Authorization": f"Bearer {token}"},
            )
        assert response.status_code == 200
        data = response.json()
        assert data["total"] >= 1
        matched = [i for i in data["items"] if i.get("matchReason") == "Crime number match"]
        assert len(matched) >= 1
        assert matched[0]["crimeNo"] == "CR-2026-SRC-001"

    @pytest.mark.asyncio
    async def test_search_by_crime_no_partial(self, client, mock_session):
        mock_session.execute.return_value = make_result(
            scalars_all=[
                MockModel(CaseMasterID=1, CrimeNo="CR-2026-SRC-001", CaseStatusID=1, PoliceStationID=5, CrimeRegisteredDate=date(2026, 1, 15), occurrence=None),
            ],
            scalar_one_val=1,
        )
        token = make_token("admin")
        async with client as ac:
            response = await ac.post(
                "/api/v1/search",
                json={"crimeNo": "SRC-001"},
                headers={"Authorization": f"Bearer {token}"},
            )
        assert response.status_code == 200
        data = response.json()
        matched = [i for i in data["items"] if i.get("matchReason")]
        assert any("Crime number match" in (i.get("matchReason") or "") for i in matched)

    @pytest.mark.asyncio
    async def test_search_by_vehicle_number(self, client, mock_session):
        list_exec = MagicMock()
        list_exec.scalars.return_value.all.return_value = [
            MockModel(CaseMasterID=1, CrimeNo="CR-2026-SRC-001", CaseStatusID=1, PoliceStationID=5, CrimeRegisteredDate=date(2026, 1, 15), occurrence=None),
        ]
        count_exec = MagicMock()
        count_exec.scalar_one.return_value = 1
        vehicle_exec = MagicMock()
        vehicle_exec.scalars.return_value.all.return_value = [
            MockModel(VehicleNumber="KA-01-AB-1234", CaseMasterID=1, Confidence=0.95),
        ]

        async def execute_side_effect(query):
            stmt_str = str(query)
            if "VehicleLink" in stmt_str or "vehicle_link" in stmt_str or "vehiclelink" in stmt_str.lower():
                return vehicle_exec
            if "count" in stmt_str.lower():
                return count_exec
            return list_exec

        mock_session.execute = AsyncMock(side_effect=execute_side_effect)

        token = make_token("admin")
        async with client as ac:
            response = await ac.post(
                "/api/v1/search",
                json={"vehicleNumber": "KA-01-AB-1234"},
                headers={"Authorization": f"Bearer {token}"},
            )
        assert response.status_code == 200
        data = response.json()
        matched = [i for i in data["items"] if i.get("matchReason")]
        assert any("Vehicle match" in (i.get("matchReason") or "") for i in matched)

    @pytest.mark.asyncio
    async def test_search_with_status_filter(self, client, mock_session):
        mock_session.execute.return_value = make_result(
            scalars_all=[
                MockModel(CaseMasterID=1, CrimeNo="CR001", CaseStatusID=1, PoliceStationID=5, CrimeRegisteredDate=date(2026, 1, 1), occurrence=None),
            ],
            scalar_one_val=1,
        )
        token = make_token("admin")
        async with client as ac:
            response = await ac.post(
                "/api/v1/search",
                json={"statusId": 1},
                headers={"Authorization": f"Bearer {token}"},
            )
        assert response.status_code == 200
        data = response.json()
        assert all(i["caseStatusID"] == 1 for i in data["items"])

    @pytest.mark.asyncio
    async def test_search_with_police_station_filter(self, client, mock_session):
        mock_session.execute.return_value = make_result(
            scalars_all=[
                MockModel(CaseMasterID=3, CrimeNo="CR003", CaseStatusID=1, PoliceStationID=3, CrimeRegisteredDate=date(2026, 1, 1), occurrence=None),
            ],
            scalar_one_val=1,
        )
        token = make_token("admin")
        async with client as ac:
            response = await ac.post(
                "/api/v1/search",
                json={"policeStationId": 3},
                headers={"Authorization": f"Bearer {token}"},
            )
        assert response.status_code == 200
        data = response.json()
        assert all(i["policeStationID"] == 3 for i in data["items"])

    @pytest.mark.asyncio
    async def test_search_pagination_page_size(self, client, mock_session):
        mock_session.execute.return_value = make_result(
            scalars_all=[
                MockModel(CaseMasterID=1, CrimeNo="CR001", CaseStatusID=1, PoliceStationID=5, CrimeRegisteredDate=date(2026, 1, 1), occurrence=None),
            ],
            scalar_one_val=5,
        )
        token = make_token("admin")
        async with client as ac:
            response = await ac.post(
                "/api/v1/search",
                json={"page": 1, "pageSize": 2},
                headers={"Authorization": f"Bearer {token}"},
            )
        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) <= 2
        assert data["page"] == 1
        assert data["pageSize"] == 2

    @pytest.mark.asyncio
    async def test_search_pagination_second_page(self, client, mock_session):
        mock_session.execute.return_value = make_result(
            scalars_all=[],
            scalar_one_val=5,
        )
        token = make_token("admin")
        async with client as ac:
            response = await ac.post(
                "/api/v1/search",
                json={"page": 2, "pageSize": 2},
                headers={"Authorization": f"Bearer {token}"},
            )
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 5

    @pytest.mark.asyncio
    async def test_search_without_auth(self, client, mock_session):
        async with client as ac:
            response = await ac.post("/api/v1/search", json={})
        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_search_non_admin_sees_filtered(self, client, mock_session):
        mock_session.execute.return_value = make_result(
            scalars_all=[],
            scalar_one_val=0,
        )
        token = make_token("officer", district_id=5)
        async with client as ac:
            response = await ac.post(
                "/api/v1/search",
                json={},
                headers={"Authorization": f"Bearer {token}"},
            )
        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_search_invalid_page_returns_422(self, client, mock_session):
        token = make_token("admin")
        async with client as ac:
            response = await ac.post(
                "/api/v1/search",
                json={"page": 0},
                headers={"Authorization": f"Bearer {token}"},
            )
        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_search_invalid_page_size_returns_422(self, client, mock_session):
        token = make_token("admin")
        async with client as ac:
            response = await ac.post(
                "/api/v1/search",
                json={"pageSize": 200},
                headers={"Authorization": f"Bearer {token}"},
            )
        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_search_semantic_flag(self, client, mock_session):
        mock_session.execute.return_value = make_result(
            scalars_all=[],
            scalar_one_val=0,
        )
        token = make_token("admin")
        async with client as ac:
            response = await ac.post(
                "/api/v1/search",
                json={"semantic": True},
                headers={"Authorization": f"Bearer {token}"},
            )
        assert response.status_code == 200
        data = response.json()
        assert data["semanticUsed"] is True

    @pytest.mark.asyncio
    async def test_search_with_date_range(self, client, mock_session):
        mock_session.execute.return_value = make_result(
            scalars_all=[],
            scalar_one_val=0,
        )
        token = make_token("admin")
        async with client as ac:
            response = await ac.post(
                "/api/v1/search",
                json={"dateFrom": "2026-01-01", "dateTo": "2026-02-28"},
                headers={"Authorization": f"Bearer {token}"},
            )
        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_search_no_match_returns_empty(self, client, mock_session):
        mock_session.execute.return_value = make_result(
            scalars_all=[],
            scalar_one_val=0,
        )
        token = make_token("admin")
        async with client as ac:
            response = await ac.post(
                "/api/v1/search",
                json={"crimeNo": "NONEXISTENT"},
                headers={"Authorization": f"Bearer {token}"},
            )
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 0
