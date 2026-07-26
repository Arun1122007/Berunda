import uuid
import pytest
from unittest.mock import AsyncMock, MagicMock, PropertyMock
from datetime import datetime
from decimal import Decimal

from fastapi import Request, HTTPException

import sys
from pathlib import Path
_root = str(Path(__file__).parent.parent)
if _root not in sys.path: sys.path.insert(0, _root)

from src.domain.models import FIR, User
from src.domain.errors import NotFoundError, ValidationError, AuthorizationError, ConflictError
from src.transport.handlers import (
    handle_list_firs,
    handle_get_fir,
    handle_create_fir,
    handle_update_fir,
    handle_delete_fir,
    handle_login,
    handle_register,
    handle_refresh,
    handle_logout,
    handle_me,
    _error_to_http,
)
from src.transport.dto import (
    FIRCreateRequest,
    FIRUpdateRequest,
    LoginRequest,
    RegisterRequest,
    RefreshRequest,
    FIRDetailResponse,
    FIRListResponse,
    TokenResponse,
    UserResponse,
)


def _make_request():
    req = MagicMock(spec=Request)
    req.headers = {}
    req.app.state.fir_service = MagicMock()
    req.app.state.fir_service.list_firs = AsyncMock()
    req.app.state.fir_service.get_fir = AsyncMock()
    req.app.state.fir_service.create_fir = AsyncMock()
    req.app.state.fir_service.update_fir = AsyncMock()
    req.app.state.fir_service.delete_fir = AsyncMock()
    req.app.state.auth_service = MagicMock()
    req.app.state.auth_service.authenticate = AsyncMock()
    req.app.state.auth_service.register = AsyncMock()
    req.app.state.auth_service.refresh_token = AsyncMock()
    req.app.state.auth_service.revoke_session = AsyncMock()
    req.app.state.auth_service.get_user_profile = AsyncMock()
    return req


@pytest.fixture
def mock_request():
    return _make_request()


@pytest.fixture
def sample_user():
    return User(
        id=uuid.uuid4(),
        email="test@example.com",
        password_hash="hash",
        full_name="Test User",
        role="admin",
        district_id="D001",
    )


@pytest.fixture
def sample_fir():
    return FIR(
        id=uuid.uuid4(),
        crime_no="24/001234",
        police_station_id="PS001",
        case_category_id="CAT001",
        gravity_offence_id="moderate",
        crime_major_head_id="MH001",
        crime_minor_head_id="mh001",
        case_status_id="OPEN",
        district_id="D001",
        registered_date=datetime.utcnow(),
        incident_from_date=datetime.utcnow().date(),
        incident_to_date=datetime.utcnow().date(),
        brief_facts="Test FIR facts",
        latitude=Decimal("12.9716"),
        longitude=Decimal("77.5946"),
        created_by=str(uuid.uuid4()),
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )


class TestErrorMapping:
    def test_not_found_maps_to_404(self):
        exc = NotFoundError("Resource not found")
        http = _error_to_http(exc)
        assert http.status_code == 404

    def test_authentication_maps_to_401(self):
        exc = NotFoundError.__bases__[0]("Auth failed")
        exc.error_code = "AUTHENTICATION_FAILED"
        exc.status_code = 401
        http = _error_to_http(exc)
        assert http.status_code == 401

    def test_authorization_maps_to_403(self):
        exc = AuthorizationError("Forbidden")
        http = _error_to_http(exc)
        assert http.status_code == 403

    def test_validation_maps_to_422(self):
        exc = ValidationError("Invalid")
        http = _error_to_http(exc)
        assert http.status_code == 422

    def test_conflict_maps_to_409(self):
        exc = ConflictError("Duplicate")
        http = _error_to_http(exc)
        assert http.status_code == 409


class TestHandleListFirs:
    async def test_success(self, sample_user, sample_fir):
        req = _make_request()
        req.app.state.fir_service.list_firs.return_value = ([sample_fir], 1)

        result = await handle_list_firs(
            request=req,
            current_user=sample_user,
            page=1,
            page_size=20,
        )

        assert isinstance(result, FIRListResponse)
        assert result.total == 1
        assert len(result.items) == 1
        assert result.items[0].crime_no == "24/001234"
        assert result.page == 1
        assert result.page_size == 20

    async def test_empty_list(self, sample_user):
        req = _make_request()
        req.app.state.fir_service.list_firs.return_value = ([], 0)

        result = await handle_list_firs(
            request=req,
            current_user=sample_user,
            page=1,
            page_size=20,
        )

        assert result.total == 0
        assert len(result.items) == 0

    async def test_pagination_conversion(self, sample_user, sample_fir):
        req = _make_request()
        req.app.state.fir_service.list_firs.return_value = ([sample_fir] * 5, 25)

        result = await handle_list_firs(
            request=req,
            current_user=sample_user,
            page=3,
            page_size=10,
        )

        assert result.page == 3
        assert result.page_size == 10
        req.app.state.fir_service.list_firs.assert_called_once()
        _, kwargs = req.app.state.fir_service.list_firs.call_args
        assert kwargs["offset"] == 20
        assert kwargs["limit"] == 10


class TestHandleGetFir:
    async def test_success(self, sample_user, sample_fir):
        req = _make_request()
        req.app.state.fir_service.get_fir.return_value = sample_fir

        result = await handle_get_fir(
            request=req,
            fir_id=sample_fir.id,
            current_user=sample_user,
        )

        assert isinstance(result, FIRDetailResponse)
        assert result.crime_no == "24/001234"
        assert result.latitude == Decimal("12.9716")

    async def test_not_found_raises_http(self, sample_user):
        req = _make_request()
        req.app.state.fir_service.get_fir.side_effect = NotFoundError("FIR not found")

        with pytest.raises(HTTPException) as exc:
            await handle_get_fir(
                request=req,
                fir_id=uuid.uuid4(),
                current_user=sample_user,
            )
        assert exc.value.status_code == 404


class TestHandleCreateFir:
    async def test_success(self, sample_user, sample_fir):
        req = _make_request()
        req.app.state.fir_service.create_fir.return_value = sample_fir

        create_body = FIRCreateRequest(
            crime_no="24/001234",
            police_station_id="PS001",
            case_category_id="CAT001",
            gravity_offence_id="moderate",
            crime_major_head_id="MH001",
            crime_minor_head_id="mh001",
            case_status_id="OPEN",
            district_id="D001",
            brief_facts="Test FIR facts",
        )

        result = await handle_create_fir(
            request=req,
            body=create_body,
            current_user=sample_user,
        )

        assert isinstance(result, FIRDetailResponse)
        assert result.crime_no == "24/001234"

    async def test_conflict_raises_http(self, sample_user):
        req = _make_request()
        req.app.state.fir_service.create_fir.side_effect = ConflictError("Crime number already exists")

        create_body = FIRCreateRequest(
            crime_no="24/001234",
            police_station_id="PS001",
            case_category_id="CAT001",
            gravity_offence_id="moderate",
            crime_major_head_id="MH001",
            crime_minor_head_id="mh001",
            case_status_id="OPEN",
            district_id="D001",
        )

        with pytest.raises(HTTPException) as exc:
            await handle_create_fir(
                request=req,
                body=create_body,
                current_user=sample_user,
            )
        assert exc.value.status_code == 409


class TestHandleUpdateFir:
    async def test_success(self, sample_user, sample_fir):
        req = _make_request()
        req.app.state.fir_service.get_fir.return_value = sample_fir
        req.app.state.fir_service.update_fir.return_value = sample_fir

        update_body = FIRUpdateRequest(brief_facts="Updated facts")

        result = await handle_update_fir(
            request=req,
            fir_id=sample_fir.id,
            body=update_body,
            current_user=sample_user,
        )

        assert isinstance(result, FIRDetailResponse)


class TestHandleDeleteFir:
    async def test_success(self, sample_user, sample_fir):
        req = _make_request()

        result = await handle_delete_fir(
            request=req,
            fir_id=sample_fir.id,
            current_user=sample_user,
        )

        assert result == {"message": "FIR deleted successfully"}

    async def test_forbidden_raises_http(self, sample_user):
        req = _make_request()
        req.app.state.fir_service.delete_fir.side_effect = AuthorizationError("Only administrators can delete FIRs")

        with pytest.raises(HTTPException) as exc:
            await handle_delete_fir(
                request=req,
                fir_id=uuid.uuid4(),
                current_user=sample_user,
            )
        assert exc.value.status_code == 403


class TestHandleLogin:
    async def test_success(self, sample_user):
        req = _make_request()
        req.app.state.auth_service.authenticate.return_value = ("access123", "refresh123", sample_user)

        login_body = LoginRequest(email="test@example.com", password="testpass123")

        result = await handle_login(
            request=req,
            body=login_body,
        )

        assert isinstance(result, TokenResponse)
        assert result.access_token == "access123"
        assert result.refresh_token == "refresh123"
        assert result.user.email == "test@example.com"


class TestHandleRegister:
    async def test_success(self, sample_user):
        req = _make_request()
        req.app.state.auth_service.register.return_value = sample_user

        register_body = RegisterRequest(
            email="new@example.com",
            password="testpass123",
            full_name="New User",
            role="officer",
            district_id="D001",
        )

        result = await handle_register(
            request=req,
            body=register_body,
            current_user=sample_user,
        )

        assert isinstance(result, UserResponse)


class TestHandleRefresh:
    async def test_success(self, sample_user):
        req = _make_request()
        req.app.state.auth_service.refresh_token.return_value = ("new_access", "new_refresh", sample_user)

        refresh_body = RefreshRequest(refresh_token="old_refresh_token")

        result = await handle_refresh(
            request=req,
            body=refresh_body,
        )

        assert result.access_token == "new_access"
        assert result.refresh_token == "new_refresh"


class TestHandleLogout:
    async def test_success(self, sample_user):
        req = _make_request()

        result = await handle_logout(
            request=req,
            current_user=sample_user,
        )

        assert result == {"message": "Logged out successfully"}


class TestHandleMe:
    async def test_success(self, sample_user):
        req = _make_request()
        req.app.state.auth_service.get_user_profile.return_value = sample_user

        result = await handle_me(
            request=req,
            current_user=sample_user,
        )

        assert isinstance(result, UserResponse)
        assert result.email == "test@example.com"
