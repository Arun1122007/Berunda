import uuid
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from datetime import datetime, timedelta

from src.domain.models import FIR, User, Session
from src.domain.errors import NotFoundError, AuthenticationError, AuthorizationError, ValidationError, ConflictError
from src.application.fir_service import FIRService
from src.application.auth_service import AuthService
from src.persistence.interfaces import FIRRepository, UserRepository, SessionRepository


@pytest.fixture
def mock_fir_repo():
    repo = MagicMock(spec=FIRRepository)
    repo.list = AsyncMock()
    repo.get_by_id = AsyncMock()
    repo.get_by_crime_no = AsyncMock()
    repo.create = AsyncMock()
    repo.update = AsyncMock()
    repo.delete = AsyncMock()
    return repo


@pytest.fixture
def mock_user_repo():
    repo = MagicMock(spec=UserRepository)
    repo.get_by_email = AsyncMock()
    repo.get_by_id = AsyncMock()
    repo.create = AsyncMock()
    return repo


@pytest.fixture
def mock_session_repo():
    repo = MagicMock(spec=SessionRepository)
    repo.create = AsyncMock()
    repo.revoke = AsyncMock()
    repo.find_by_hash = AsyncMock()
    repo.find_active_by_user_id = AsyncMock()
    return repo


@pytest.fixture
def sample_admin():
    return User(
        id=uuid.uuid4(),
        email="admin@example.com",
        password_hash="$2b$12$LJ3m4ys3Lk0TSwHn9kO.cOwVSTz7MqYMQzqBmz5yF5z5z5z5z5z5y",
        full_name="Admin User",
        role="admin",
        district_id="D001",
    )


@pytest.fixture
def sample_officer():
    return User(
        id=uuid.uuid4(),
        email="officer@example.com",
        password_hash="$2b$12$LJ3m4ys3Lk0TSwHn9kO.cOwVSTz7MqYMQzqBmz5yF5z5z5z5z5z5y",
        full_name="Police Officer",
        role="officer",
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
    )


@pytest.fixture
def fir_service(mock_fir_repo, mock_user_repo):
    return FIRService(fir_repo=mock_fir_repo, user_repo=mock_user_repo)


@pytest.fixture
def auth_service(mock_user_repo, mock_session_repo):
    return AuthService(
        user_repo=mock_user_repo,
        session_repo=mock_session_repo,
        jwt_secret="test-secret-key",
    )


class TestFIRService:
    async def test_list_firs_success(self, fir_service, mock_fir_repo, mock_user_repo, sample_admin, sample_fir):
        mock_user_repo.get_by_id.return_value = sample_admin
        mock_fir_repo.list.return_value = ([sample_fir], 1)

        items, total = await fir_service.list_firs(user_id=sample_admin.id)

        assert total == 1
        assert len(items) == 1
        assert items[0].crime_no == "24/001234"
        mock_fir_repo.list.assert_awaited_once()

    async def test_list_firs_user_not_found(self, fir_service, mock_user_repo):
        mock_user_repo.get_by_id.return_value = None

        with pytest.raises(NotFoundError) as exc:
            await fir_service.list_firs(user_id=uuid.uuid4())
        assert "User not found" in str(exc.value)

    async def test_get_fir_success(self, fir_service, mock_fir_repo, mock_user_repo, sample_admin, sample_fir):
        mock_user_repo.get_by_id.return_value = sample_admin
        mock_fir_repo.get_by_id.return_value = sample_fir

        result = await fir_service.get_fir(fir_id=sample_fir.id, user_id=sample_admin.id)

        assert result.id == sample_fir.id
        assert result.crime_no == "24/001234"

    async def test_get_fir_not_found(self, fir_service, mock_fir_repo, mock_user_repo, sample_admin):
        mock_user_repo.get_by_id.return_value = sample_admin
        mock_fir_repo.get_by_id.return_value = None

        with pytest.raises(NotFoundError) as exc:
            await fir_service.get_fir(fir_id=uuid.uuid4(), user_id=sample_admin.id)
        assert "FIR not found" in str(exc.value)

    async def test_create_fir_success(self, fir_service, mock_fir_repo, mock_user_repo, sample_admin, sample_fir):
        mock_user_repo.get_by_id.return_value = sample_admin
        mock_fir_repo.get_by_crime_no.return_value = None
        mock_fir_repo.create.return_value = sample_fir

        result = await fir_service.create_fir(fir_data=sample_fir, user_id=sample_admin.id)

        assert result.crime_no == "24/001234"
        mock_fir_repo.create.assert_awaited_once()

    async def test_create_fir_duplicate_crime_no(self, fir_service, mock_fir_repo, mock_user_repo, sample_admin, sample_fir):
        mock_user_repo.get_by_id.return_value = sample_admin
        mock_fir_repo.get_by_crime_no.return_value = sample_fir

        with pytest.raises(ConflictError) as exc:
            await fir_service.create_fir(fir_data=sample_fir, user_id=sample_admin.id)
        assert "already exists" in str(exc.value)

    async def test_create_fir_invalid_gravity(self, fir_service, mock_fir_repo, mock_user_repo, sample_admin, sample_fir):
        invalid_fir = sample_fir.model_copy(update={"gravity_offence_id": "invalid"})
        mock_user_repo.get_by_id.return_value = sample_admin
        mock_fir_repo.get_by_crime_no.return_value = None

        with pytest.raises(ValidationError) as exc:
            await fir_service.create_fir(fir_data=invalid_fir, user_id=sample_admin.id)
        assert "Invalid gravity" in str(exc.value)

    async def test_create_fir_requires_supervisory_approval(self, fir_service, mock_fir_repo, mock_user_repo, sample_officer, sample_fir):
        serious_fir = sample_fir.model_copy(update={"gravity_offence_id": "serious"})
        mock_user_repo.get_by_id.return_value = sample_officer
        mock_fir_repo.get_by_crime_no.return_value = None

        with pytest.raises(AuthorizationError) as exc:
            await fir_service.create_fir(fir_data=serious_fir, user_id=sample_officer.id)
        assert "Supervisory approval" in str(exc.value)

    async def test_update_fir_success(self, fir_service, mock_fir_repo, mock_user_repo, sample_admin, sample_fir):
        mock_user_repo.get_by_id.return_value = sample_admin
        mock_fir_repo.get_by_id.return_value = sample_fir
        mock_fir_repo.update.return_value = sample_fir

        result = await fir_service.update_fir(fir_id=sample_fir.id, fir_data=sample_fir, user_id=sample_admin.id)

        assert result.crime_no == "24/001234"

    async def test_delete_fir_success(self, fir_service, mock_fir_repo, mock_user_repo, sample_admin, sample_fir):
        mock_user_repo.get_by_id.return_value = sample_admin
        mock_fir_repo.get_by_id.return_value = sample_fir

        await fir_service.delete_fir(fir_id=sample_fir.id, user_id=sample_admin.id)
        mock_fir_repo.delete.assert_awaited_once_with(sample_fir.id)

    async def test_delete_fir_not_admin(self, fir_service, mock_fir_repo, mock_user_repo, sample_officer, sample_fir):
        mock_user_repo.get_by_id.return_value = sample_officer
        mock_fir_repo.get_by_id.return_value = sample_fir

        with pytest.raises(AuthorizationError) as exc:
            await fir_service.delete_fir(fir_id=sample_fir.id, user_id=sample_officer.id)
        assert "Only administrators" in str(exc.value)

    async def test_get_fir_forbidden(self, fir_service, mock_fir_repo, mock_user_repo, sample_officer, sample_fir):
        other_district_fir = sample_fir.model_copy(update={"district_id": "D999"})
        mock_user_repo.get_by_id.return_value = sample_officer
        mock_fir_repo.get_by_id.return_value = other_district_fir

        with pytest.raises(AuthorizationError) as exc:
            await fir_service.get_fir(fir_id=other_district_fir.id, user_id=sample_officer.id)


class TestAuthService:
    async def test_authenticate_success(self, auth_service, mock_user_repo, sample_admin):
        email = "admin@example.com"
        password = "testpass123"
        hashed = "$2b$12$LJ3m4ys3Lk0TSwHn9kO.cOwVSTz7MqYMQzqBmz5yF5z5z5z5z5z5y"

        user = sample_admin.model_copy(update={"password_hash": hashed})
        mock_user_repo.get_by_email.return_value = user

        with patch("bcrypt.checkpw", return_value=True):
            access_token, refresh_token, result = await auth_service.authenticate(email=email, password=password)

        assert access_token is not None
        assert refresh_token is not None
        assert result.email == email

    async def test_authenticate_invalid_email(self, auth_service, mock_user_repo):
        mock_user_repo.get_by_email.return_value = None

        with pytest.raises(AuthenticationError) as exc:
            await auth_service.authenticate(email="nonexistent@example.com", password="testpass123")
        assert "Invalid email or password" in str(exc.value)

    async def test_authenticate_wrong_password(self, auth_service, mock_user_repo, sample_admin):
        mock_user_repo.get_by_email.return_value = sample_admin

        with patch("bcrypt.checkpw", return_value=False):
            with pytest.raises(AuthenticationError) as exc:
                await auth_service.authenticate(email="admin@example.com", password="wrongpass")
            assert "Invalid email or password" in str(exc.value)

    async def test_register_success(self, auth_service, mock_user_repo):
        mock_user_repo.get_by_email.return_value = None
        mock_user_repo.create.return_value = User(
            id=uuid.uuid4(),
            email="new@example.com",
            password_hash="hash",
            full_name="New User",
            role="officer",
            district_id="D001",
        )

        result = await auth_service.register(
            email="new@example.com",
            password="securepass123",
            full_name="New User",
            role="officer",
            district_id="D001",
        )

        assert result.email == "new@example.com"
        assert result.role == "officer"

    async def test_register_duplicate_email(self, auth_service, mock_user_repo):
        existing = User(
            id=uuid.uuid4(),
            email="dup@example.com",
            password_hash="hash",
            full_name="Existing",
            role="officer",
        )
        mock_user_repo.get_by_email.return_value = existing

        with pytest.raises(ConflictError) as exc:
            await auth_service.register(
                email="dup@example.com",
                password="securepass123",
                full_name="New User",
            )
        assert "already exists" in str(exc.value)

    async def test_register_short_password(self, auth_service, mock_user_repo):
        mock_user_repo.get_by_email.return_value = None

        with pytest.raises(ValidationError) as exc:
            await auth_service.register(
                email="new@example.com",
                password="short",
                full_name="New User",
            )
        assert "at least 8 characters" in str(exc.value)

    async def test_get_user_profile_success(self, auth_service, mock_user_repo, sample_admin):
        mock_user_repo.get_by_id.return_value = sample_admin

        result = await auth_service.get_user_profile(user_id=sample_admin.id)

        assert result.id == sample_admin.id
        assert result.email == sample_admin.email

    async def test_get_user_profile_not_found(self, auth_service, mock_user_repo):
        mock_user_repo.get_by_id.return_value = None

        with pytest.raises(NotFoundError) as exc:
            await auth_service.get_user_profile(user_id=uuid.uuid4())
        assert "User not found" in str(exc.value)

    async def test_revoke_session(self, auth_service, mock_session_repo):
        user_id = uuid.uuid4()
        session = Session(
            id=uuid.uuid4(),
            user_id=user_id,
            token_hash="hash",
            expires_at=datetime.utcnow() + timedelta(hours=1),
        )
        mock_session_repo.find_active_by_user_id.return_value = session

        await auth_service.revoke_session(user_id=user_id)

        mock_session_repo.revoke.assert_awaited_once_with(session.id)
