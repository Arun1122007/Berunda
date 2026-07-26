"""Complete end-to-end user journey for FIR Case Management."""
import sys
from pathlib import Path

_root = str(Path(__file__).parent.parent.parent.parent)
if _root not in sys.path: sys.path.insert(0, _root)

import pytest


@pytest.mark.asyncio
@pytest.mark.e2e
async def test_full_user_journey(async_client):
    # 1. Register a new user
    reg_resp = await async_client.post("/api/v1/auth/register", json={
        "email": "journey@test.com",
        "password": "journey123",
        "role": "admin",
    })
    assert reg_resp.status_code == 201, f"Register failed: {reg_resp.text}"

    # 2. Login
    login_resp = await async_client.post("/api/v1/auth/login", json={
        "email": "journey@test.com",
        "password": "journey123",
    })
    assert login_resp.status_code == 200, f"Login failed: {login_resp.text}"
    token_data = login_resp.json()
    token = token_data["token"]
    auth_headers = {"Authorization": f"Bearer {token}"}

    # 3. Get user profile
    me_resp = await async_client.get("/api/v1/auth/me", headers=auth_headers)
    assert me_resp.status_code == 200
    assert me_resp.json()["email"] == "journey@test.com"

    # 4. List cases (should be empty or contain seeded data)
    list_resp = await async_client.get("/api/v1/fir", headers=auth_headers)
    assert list_resp.status_code == 200
    initial_total = list_resp.json()["total"]

    # 5. Create a new case
    create_resp = await async_client.post("/api/v1/fir", headers=auth_headers, json={
        "crimeNo": "E2E-CR-2026-001",
        "briefFacts": "Test case for end-to-end journey",
    })
    assert create_resp.status_code == 201, f"Create failed: {create_resp.text}"
    case_id = create_resp.json()["caseMasterID"]

    # 6. Get the created case
    get_resp = await async_client.get(f"/api/v1/fir/{case_id}", headers=auth_headers)
    assert get_resp.status_code == 200
    assert get_resp.json()["crimeNo"] == "E2E-CR-2026-001"

    # 7. Verify list includes new case
    list_resp2 = await async_client.get("/api/v1/fir", headers=auth_headers)
    assert list_resp2.json()["total"] > initial_total

    # 8. Invalid login
    bad_login = await async_client.post("/api/v1/auth/login", json={
        "email": "journey@test.com",
        "password": "wrongpassword",
    })
    assert bad_login.status_code == 401

    # 9. Create without auth
    noauth_resp = await async_client.post("/api/v1/fir", json={"crimeNo": "E2E-NOAUTH"})
    assert noauth_resp.status_code == 401
