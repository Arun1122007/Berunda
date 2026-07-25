"""End-to-end test: Login → List cases → View detail → Create case.

Requires: --run-e2e flag and backend running on localhost:8000.
"""

from __future__ import annotations

import pytest
import pytest_asyncio
from httpx import AsyncClient


@pytest.fixture(scope="module")
def base_url() -> str:
    return "http://localhost:8000/api/v1"


@pytest_asyncio.fixture(scope="module")
async def registered_user(base_url: str) -> dict:
    import random
    import string

    suffix = "".join(random.choices(string.ascii_lowercase, k=8))
    email = f"e2e_{suffix}@test.com"
    password = "e2eTestPass123"

    async with AsyncClient(base_url=base_url) as client:
        resp = await client.post(
            "/auth/register",
            json={"email": email, "password": password, "role": "admin"},
        )
        assert resp.status_code == 201, f"Registration failed: {resp.text}"
        return {"email": email, "password": password}


@pytest_asyncio.fixture(scope="module")
async def auth_token(base_url: str, registered_user: dict) -> str:
    async with AsyncClient(base_url=base_url) as client:
        resp = await client.post(
            "/auth/login",
            json={
                "email": registered_user["email"],
                "password": registered_user["password"],
            },
        )
        assert resp.status_code == 200, f"Login failed: {resp.text}"
        data = resp.json()
        return data["token"]


@pytest.mark.e2e
class TestUserJourney:
    """Complete user journey: Login → List → Detail → Create → Verify."""

    async def test_01_login_and_get_profile(self, base_url: str, auth_token: str):
        async with AsyncClient(base_url=base_url) as client:
            resp = await client.get(
                "/auth/me",
                headers={"Authorization": f"Bearer {auth_token}"},
            )
        assert resp.status_code == 200
        data = resp.json()
        assert "email" in data
        assert "role" in data
        assert data["role"] == "admin"

    async def test_02_list_cases(self, base_url: str, auth_token: str):
        async with AsyncClient(base_url=base_url) as client:
            resp = await client.get(
                "/fir",
                headers={"Authorization": f"Bearer {auth_token}"},
            )
        assert resp.status_code == 200
        data = resp.json()
        assert "items" in data
        assert "total" in data
        assert "page" in data

    async def test_03_create_case(self, base_url: str, auth_token: str):
        async with AsyncClient(base_url=base_url) as client:
            resp = await client.post(
                "/fir",
                json={
                    "crimeNo": "CR-2026-E2E-001",
                    "caseNo": "E2E/2026",
                    "briefFacts": "End-to-end test case for verification",
                },
                headers={"Authorization": f"Bearer {auth_token}"},
            )
        assert resp.status_code == 201, f"Create failed: {resp.text}"
        data = resp.json()
        assert data["crimeNo"] == "CR-2026-E2E-001"
        assert "caseMasterId" in data

        # Store case ID for next test
        self._case_id = data["caseMasterId"]

    async def test_04_get_created_case(self, base_url: str, auth_token: str):
        async with AsyncClient(base_url=base_url) as client:
            resp = await client.get(
                f"/fir/{self._case_id}",
                headers={"Authorization": f"Bearer {auth_token}"},
            )
        assert resp.status_code == 200
        data = resp.json()
        assert data["crimeNo"] == "CR-2026-E2E-001"
        assert data["caseMasterId"] == self._case_id
        assert data["briefFacts"] == "End-to-end test case for verification"

    async def test_05_verify_list_includes_new_case(self, base_url: str, auth_token: str):
        async with AsyncClient(base_url=base_url) as client:
            resp = await client.get(
                "/fir",
                headers={"Authorization": f"Bearer {auth_token}"},
            )
        assert resp.status_code == 200
        data = resp.json()
        crime_nos = [item["crimeNo"] for item in data["items"]]
        assert "CR-2026-E2E-001" in crime_nos

    async def test_06_failure_path_invalid_login(self, base_url: str):
        async with AsyncClient(base_url=base_url) as client:
            resp = await client.post(
                "/auth/login",
                json={"email": "nonexistent@test.com", "password": "wrong"},
            )
        assert resp.status_code == 401
        data = resp.json()
        assert "error" in data
        assert data["error"]["code"] == "AUTHENTICATION_ERROR"

    async def test_07_failure_path_create_without_auth(self, base_url: str):
        async with AsyncClient(base_url=base_url) as client:
            resp = await client.post(
                "/fir",
                json={"crimeNo": "CR-2026-UNAUTH"},
            )
        assert resp.status_code == 401
