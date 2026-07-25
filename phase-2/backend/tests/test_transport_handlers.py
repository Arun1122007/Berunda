import uuid
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
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


@pytest.fixture
def mock_request():
    req = MagicMock(spec=Request)
    req.headers = {}
    return req


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
    async def test_success(self, mock_request, sample_user, sample_fir):
        mock_fir_service = MagicMock()
        mock_fir_service.list_firs = AsyncMock(return_value=([sample_fir], 1))

        with patch("src.transport.handlers.get_current_user", return_value=sample_user):
            with patch("src.transport.handlers.FIRService", return_value=mock_fir_service):
                result = await handle_list_firs(request=mock_request, offset=0, limit=20)

        assert isinstance(result, FIRListResponse)
        assert result.total == 1
        assert len(result.items) == 1
        assert result.items[0].crime_no == "24/001234"

    async def test_empty_list(self, mock_request, sample_user):
        mock_fir_service = MagicMock()
        mock_fir_service.list_firs = AsyncMock(return_value=([], 0))

        with patch("src.transport.handlers.get_current_user", return_value=sample_user):
            with patch("src.transport.handlers.FIRService", return_value=mock_fir_service):
                result = await handle_list_firs(request=mock_request, offset=0, limit=20)

        assert result.total == 0
        assert len(result.items) == 0


class TestHandleGetFir:
    async def test_success(self, mock_request, sample_user, sample_fir):
        mock_fir_service = MagicMock()
        mock_fir_service.get_fir = AsyncMock(return_value=sample_fir)

        with patch("src.transport.handlers.get_current_user", return_value=sample_user):
            with patch("src.transport.handlers.FIRService", return_value=mock_fir_service):
                result = await handle_get_fir(request=mock_request, fir_id=sample_fir.id)

        assert isinstance(result, FIRDetailResponse)
        assert result.crime_no == "24/001234"
        assert result.latitude == Decimal("12.9716")

    async def test_not_found_raises_http(self, mock_request, sample_user):
        mock_fir_service = MagicMock()
        mock_fir_service.get_fir = AsyncMock(side_effect=NotFoundError("FIR not found"))

        with patch("src.transport.handlers.get_current_user", return_value=sample_user):
            with patch("src.transport.handlers.FIRService", return_value=mock_fir_service):
                with pytest.raises(HTTPException) as exc:
                    await handle_get_fir(request=mock_request, fir_id=uuid.uuid4())
                assert exc.value.status_code == 404


class TestHandleCreateFir:
    async def test_success(self, mock_request, sample_user, sample_fir):
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
        mock_fir_service = MagicMock()
        mock_fir_service.create_fir = AsyncMock(return_value=sample_fir)

        with patch("src.transport.handlers.get_current_user", return_value=sample_user):
            with patch("src.transport.handlers.FIRService", return_value=mock_fir_service):
                result = await handle_create_fir(request=mock_request, body=create_body)

        assert isinstance(result, FIRDetailResponse)
        assert result.crime_no == "24/001234"

    async def test_conflict_raises_http(self, mock_request, sample_user):
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
        mock_fir_service = MagicMock()
        mock_fir_service.create_fir = AsyncMock(side_effect=ConflictError("Crime number already exists"))

        with patch("src.transport.handlers.get_current_user", return_value=sample_user):
            with patch("src.transport.handlers.FIRService", return_value=mock_fir_service):
                with pytest.raises(HTTPException) as exc:
                    await handle_create_fir(request=mock_request, body=create_body)
                assert exc.value.status_code == 409


class TestHandleUpdateFir:
    async def test_success(self, mock_request, sample_user, sample_fir):
        update_body = FIRUpdateRequest(brief_facts="Updated facts")
        mock_fir_service = MagicMock()
        mock_fir_service.get_fir = AsyncMock(return_value=sample_fir)
        mock_fir_service.update_fir = AsyncMock(return_value=sample_fir)

        with patch("src.transport.handlers.get_current_user", return_value=sample_user):
            with patch("src.transport.handlers.FIRService", return_value=mock_fir_service):
                result = await handle_update_fir(
                    request=mock_request,
                    fir_id=sample_fir.id,
                    body=update_body,
                )

        assert isinstance(result, FIRDetailResponse)


class TestHandleDeleteFir:
    async def test_success(self, mock_request, sample_user, sample_fir):
        mock_fir_service = MagicMock()
        mock_fir_service.delete_fir = AsyncMock()

        with patch("src.transport.handlers.get_current_user", return_value=sample_user):
            with patch("src.transport.handlers.FIRService", return_value=mock_fir_service):
                result = await handle_delete_fir(request=mock_request, fir_id=sample_fir.id)

        assert result == {"message": "FIR deleted successfully"}

    async def test_forbidden_raises_http(self, mock_request, sample_user):
        mock_fir_service = MagicMock()
        mock_fir_service.delete_fir = AsyncMock(side_effect=AuthorizationError("Only administrators can delete FIRs"))

        with patch("src.transport.handlers.get_current_user", return_value=sample_user):
            with patch("src.transport.handlers.FIRService", return_value=mock_fir_service):
                with pytest.raises(HTTPException) as exc:
                    await handle_delete_fir(request=mock_request, fir_id=uuid.uuid4())
                assert exc.value.status_code == 403


class TestHandleLogin:
    async def test_success(self, mock_request, sample_user):
        login_body = LoginRequest(email="test@example.com", password="testpass123")
        mock_auth_service = MagicMock()
        mock_auth_service.authenticate = AsyncMock(return_value=("access123", "refresh123", sample_user))

        with patch("src.transport.handlers.AuthService", return_value=mock_auth_service):
            result = await handle_login(request=mock_request, body=login_body)

        assert isinstance(result, TokenResponse)
        assert result.access_token == "access123"
        assert result.refresh_token == "refresh123"
        assert result.user.email == "test@example.com"


class TestHandleRegister:
    async def test_success(self, mock_request, sample_user):
        register_body = RegisterRequest(
            email="new@example.com",
            password="testpass123",
            full_name="New User",
            role="officer",
            district_id="D001",
        )
        mock_auth_service = MagicMock()
        mock_auth_service.register = AsyncMock(return_value=sample_user)

        with patch("src.transport.handlers.get_current_user", return_value=sample_user):
            with patch("src.transport.handlers.AuthService", return_value=mock_auth_service):
                result = await handle_register(request=mock_request, body=register_body)

        assert isinstance(result, UserResponse)


class TestHandleRefresh:
    async def test_success(self, mock_request, sample_user):
        refresh_body = RefreshRequest(refresh_token="old_refresh_token")
        mock_auth_service = MagicMock()
        mock_auth_service.refresh_token = AsyncMock(return_value=("new_access", "new_refresh", sample_user))

        with patch("src.transport.handlers.AuthService", return_value=mock_auth_service):
            result = await handle_refresh(request=mock_request, body=refresh_body)

        assert result.access_token == "new_access"
        assert result.refresh_token == "new_refresh"


class TestHandleLogout:
    async def test_success(self, mock_request, sample_user):
        mock_auth_service = MagicMock()
        mock_auth_service.revoke_session = AsyncMock()

        with patch("src.transport.handlers.get_current_user", return_value=sample_user):
            with patch("src.transport.handlers.AuthService", return_value=mock_auth_service):
                result = await handle_logout(request=mock_request)

        assert result == {"message": "Logged out successfully"}


class TestHandleMe:
    async def test_success(self, mock_request, sample_user):
        mock_auth_service = MagicMock()
        mock_auth_service.get_user_profile = AsyncMock(return_value=sample_user)

        with patch("src.transport.handlers.get_current_user", return_value=sample_user):
            with patch("src.transport.handlers.AuthService", return_value=mock_auth_service):
                result = await handle_me(request=mock_request)

        assert isinstance(result, UserResponse)
        assert result.email == "test@example.com"
