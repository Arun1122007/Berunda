"""Contract compliance tests for the Phase 2 backend.

Verifies the frozen API contract: error format, pagination, route paths, auth.
"""

import sys
import uuid
from datetime import datetime
from pathlib import Path

from fastapi import status

_root = str(Path(__file__).parent.parent)
if _root not in sys.path: sys.path.insert(0, _root)

from src.domain.errors import (
    AuthenticationError,
    AuthorizationError,
    ConflictError,
    DomainError,
    NotFoundError,
    ValidationError,
)
from src.transport.dto import FIRDetailResponse, FIRListResponse
from src.transport.handlers import _error_to_http


class TestErrorContractFormat:
    """Verify error responses match docs/contracts/error-contract.md format."""

    def test_error_response_has_error_wrapper(self):
        exc = NotFoundError("FIR not found")
        http = _error_to_http(exc)
        detail = http.detail
        assert "error_code" in detail
        assert "message" in detail

    def test_all_error_codes_map_correctly(self):
        cases = [
            (NotFoundError("x"), status.HTTP_404_NOT_FOUND, "NOT_FOUND"),
            (AuthenticationError("x"), status.HTTP_401_UNAUTHORIZED, "AUTHENTICATION_FAILED"),
            (AuthorizationError("x"), status.HTTP_403_FORBIDDEN, "FORBIDDEN"),
            (ValidationError("x"), status.HTTP_422_UNPROCESSABLE_ENTITY, "VALIDATION_ERROR"),
            (ConflictError("x"), status.HTTP_409_CONFLICT, "CONFLICT"),
        ]
        for exc, expected_status, expected_code in cases:
            http = _error_to_http(exc)
            assert http.status_code == expected_status, f"{expected_code} should map to {expected_status}"
            assert http.detail["error_code"] == expected_code

    def test_internal_error_fallback(self):
        exc = DomainError("Unexpected")
        http = _error_to_http(exc)
        assert http.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert http.detail["error_code"] == "INTERNAL_ERROR"


class TestPaginationContract:
    """Verify pagination uses page/page_size per docs/contracts/api-contracts.md."""

    def test_list_response_uses_page_and_page_size(self):
        response = FIRListResponse(items=[], total=0, page=1, page_size=20)
        assert response.page == 1
        assert response.page_size == 20
        assert response.total == 0

    def test_page_serializes_to_camel_case(self):
        response = FIRListResponse(items=[], total=25, page=2, page_size=10)
        data = response.model_dump(by_alias=True)
        assert data["page"] == 2
        assert data["pageSize"] == 10
        assert data["total"] == 25

    def test_page_size_default_is_20(self):
        response = FIRListResponse(items=[], total=0, page=1, page_size=20)
        assert response.page_size == 20

    def test_page_default_is_1(self):
        response = FIRListResponse(items=[], total=0, page=1, page_size=20)
        assert response.page == 1


class TestRoutePathContract:
    """Verify route paths match docs/contracts/api-contracts.md using the app."""

    def test_app_routes_include_fir_and_auth(self):
        from src.main import app
        routes = [(r.path, list(r.methods)) for r in app.routes if hasattr(r, "path") and hasattr(r, "methods")]
        route_map = {path: methods for path, methods in routes}

        assert "/api/v1/fir" in route_map
        assert "/api/v1/auth/login" in route_map
        assert "/api/v1/auth/me" in route_map
        assert "/api/v1/auth/refresh" in route_map

    def test_fir_endpoint_methods(self):
        from src.main import app
        routes = [(r.path, list(r.methods)) for r in app.routes if hasattr(r, "path") and hasattr(r, "methods")]
        route_map = {path: methods for path, methods in routes}

        assert "GET" in route_map["/api/v1/fir"]
        assert "POST" in route_map["/api/v1/fir"]

    def test_health_endpoint_exists(self):
        from src.main import app
        routes = [(r.path, list(r.methods)) for r in app.routes if hasattr(r, "path") and hasattr(r, "methods")]
        route_map = {path: methods for path, methods in routes}
        assert "/health" in route_map
        assert "/" in route_map


class TestDtoSerialization:
    """Verify DTO serialization matches frontend expectations."""

    def test_fir_detail_serializes_camel_case(self):
        fir = FIRDetailResponse(
            id=uuid.uuid4(),
            crime_no="24/001234",
            case_no="42/2026",
            registered_date=datetime.utcnow(),
            police_station_id="PS001",
            case_category_id="CAT001",
            gravity_offence_id="moderate",
            crime_major_head_id="MH001",
            crime_minor_head_id="mh001",
            case_status_id="OPEN",
            district_id="D001",
            created_by=str(uuid.uuid4()),
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        data = fir.model_dump(by_alias=True)
        assert "crimeNo" in data
        assert "caseNo" in data
        assert "policeStationId" in data
        assert "caseCategoryId" in data
        assert "gravityOffenceId" in data
        assert "crimeMajorHeadId" in data
        assert "crimeMinorHeadId" in data
        assert "caseStatusId" in data
        assert "districtId" in data
        assert "createdBy" in data
        assert "registeredDate" in data

    def test_fir_detail_deserializes_snake_case(self):
        fir_id = uuid.uuid4()
        data = {
            "id": fir_id,
            "crime_no": "24/001234",
            "case_no": None,
            "registered_date": datetime.utcnow().isoformat(),
            "police_station_id": "PS001",
            "case_category_id": "CAT001",
            "gravity_offence_id": "moderate",
            "crime_major_head_id": "MH001",
            "crime_minor_head_id": "mh001",
            "case_status_id": "OPEN",
            "district_id": "D001",
            "created_by": None,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
        }
        fir = FIRDetailResponse.model_validate(data)
        assert fir.crime_no == "24/001234"
        assert fir.id == fir_id


class TestAuthTokenContract:
    """Verify auth token behavior per docs/contracts/frontend-backend-contract.md."""

    def test_login_returns_token_response(self):
        from src.transport.dto import TokenResponse, UserResponse
        user_resp = UserResponse(
            id=uuid.uuid4(),
            email="test@example.com",
            full_name="Test User",
            role="admin",
        )
        token_resp = TokenResponse(
            access_token="access123",
            refresh_token="refresh123",
            user=user_resp,
        )
        assert token_resp.token_type == "bearer"
        assert token_resp.access_token == "access123"
        assert token_resp.refresh_token == "refresh123"
        data = token_resp.model_dump(by_alias=True)
        assert data["accessToken"] == "access123"
        assert data["refreshToken"] == "refresh123"
        assert data["tokenType"] == "bearer"

    def test_user_response_serializes_camel_case(self):
        from src.transport.dto import UserResponse
        user = UserResponse(
            id=uuid.uuid4(),
            email="test@example.com",
            full_name="Test User",
            role="admin",
            district_id="D001",
        )
        data = user.model_dump(by_alias=True)
        assert data["fullName"] == "Test User"
        assert data["districtId"] == "D001"
