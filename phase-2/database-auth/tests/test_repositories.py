import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session as SASession
from src.auth.password import hash_password

from src.models import Base, District, Unit
from src.repositories import FirRepository, SessionRepository, UserRepository


@pytest.fixture
def db_session():
    engine = create_engine("sqlite:///:memory:", echo=False)
    Base.metadata.create_all(engine)
    session = SASession(bind=engine)
    _seed_minimal(session)
    yield session
    session.close()
    engine.dispose()


def _seed_minimal(session):
    session.add_all([
        District(DistrictID=1, DistrictName="Test District", StateID=1),
        Unit(UnitID=1, UnitName="Test PS", DistrictID=1, TypeID=1),
    ])
    session.flush()


def test_fir_create(db_session):
    repo = FirRepository(db_session)
    case = repo.create({
        "CrimeNo": "REPO-TEST-001",
        "CaseNo": "REPO/001",
        "PoliceStationID": 1,
    })
    assert case.CrimeNo == "REPO-TEST-001"
    assert case.CaseMasterID is not None


def test_fir_get_by_id(db_session):
    repo = FirRepository(db_session)
    case = repo.create({"CrimeNo": "GET-TEST-001", "CaseNo": "GET/001"})
    found = repo.get_by_id(case.CaseMasterID)
    assert found is not None
    assert found.CrimeNo == "GET-TEST-001"


def test_fir_list_with_pagination(db_session):
    repo = FirRepository(db_session)
    for i in range(5):
        repo.create({"CrimeNo": f"PAGE-TEST-{i:03d}"})
    results = repo.list(offset=0, limit=3)
    assert len(results) == 3
    results2 = repo.list(offset=3, limit=3)
    assert len(results2) == 2


def test_fir_filter_by_status(db_session):
    repo = FirRepository(db_session)
    repo.create({"CrimeNo": "FILTER-001", "CaseStatusID": 1})
    repo.create({"CrimeNo": "FILTER-002", "CaseStatusID": 2})
    results = repo.list(case_status_id=1)
    assert len(results) == 1
    assert results[0].CrimeNo == "FILTER-001"


def test_fir_filter_by_police_station(db_session):
    repo = FirRepository(db_session)
    repo.create({"CrimeNo": "PS-FILTER-001", "PoliceStationID": 1})
    results = repo.list(police_station_id=1)
    assert len(results) == 1


def test_fir_update(db_session):
    repo = FirRepository(db_session)
    case = repo.create({"CrimeNo": "UPD-TEST", "CaseNo": "OLD"})
    updated = repo.update(case.CaseMasterID, {"CaseNo": "NEW"})
    assert updated is not None
    assert updated.CaseNo == "NEW"


def test_fir_delete(db_session):
    repo = FirRepository(db_session)
    case = repo.create({"CrimeNo": "DEL-TEST"})
    assert repo.delete(case.CaseMasterID) is True
    assert repo.get_by_id(case.CaseMasterID) is None


def test_fir_delete_nonexistent(db_session):
    repo = FirRepository(db_session)
    assert repo.delete(99999) is False


def test_user_create(db_session):
    repo = UserRepository(db_session)
    user = repo.create({
        "Email": "new@test.com",
        "HashedPassword": hash_password("pass"),
        "Role": "analyst",
        "IsActive": True,
    })
    assert user.Email == "new@test.com"
    assert user.UserID is not None


def test_user_get_by_email(db_session):
    repo = UserRepository(db_session)
    repo.create({
        "Email": "find@test.com",
        "HashedPassword": "hash",
        "Role": "officer",
        "IsActive": True,
    })
    found = repo.get_by_email("find@test.com")
    assert found is not None
    assert found.Role == "officer"


def test_user_get_by_email_not_found(db_session):
    repo = UserRepository(db_session)
    assert repo.get_by_email("nobody@test.com") is None


def test_user_list_filter_role(db_session):
    repo = UserRepository(db_session)
    repo.create({"Email": "a@t.com", "HashedPassword": "h", "Role": "admin", "IsActive": True})
    repo.create({"Email": "b@t.com", "HashedPassword": "h", "Role": "officer", "IsActive": True})
    admins = repo.list(role="admin")
    assert len(admins) == 1


def test_user_update(db_session):
    repo = UserRepository(db_session)
    user = repo.create({"Email": "upd@t.com", "HashedPassword": "h", "Role": "viewer", "IsActive": True})
    updated = repo.update(user.UserID, {"Role": "analyst"})
    assert updated.Role == "analyst"


def test_user_delete(db_session):
    repo = UserRepository(db_session)
    user = repo.create({"Email": "del@t.com", "HashedPassword": "h", "Role": "viewer", "IsActive": True})
    assert repo.delete(user.UserID) is True
    assert repo.get_by_id(user.UserID) is None


def test_session_create(db_session):
    from datetime import datetime, timedelta, timezone
    repo = SessionRepository(db_session)
    session_obj = repo.create({
        "UserID": 1,
        "TokenHash": "abc123hash",
        "ExpiresAt": datetime.now(timezone.utc) + timedelta(hours=1),
    })
    assert session_obj.SessionID is not None
    assert session_obj.RevokedAt is None


def test_session_find_by_hash(db_session):
    from datetime import datetime, timedelta, timezone
    repo = SessionRepository(db_session)
    repo.create({
        "UserID": 1,
        "TokenHash": "findmehash",
        "ExpiresAt": datetime.now(timezone.utc) + timedelta(hours=1),
    })
    found = repo.find_by_hash("findmehash")
    assert found is not None


def test_session_revoke(db_session):
    from datetime import datetime, timedelta, timezone
    repo = SessionRepository(db_session)
    session_obj = repo.create({
        "UserID": 1,
        "TokenHash": "revokeme",
        "ExpiresAt": datetime.now(timezone.utc) + timedelta(hours=1),
    })
    revoked = repo.revoke(session_obj.SessionID)
    assert revoked is not None
    assert revoked.RevokedAt is not None


def test_session_find_by_hash_revoked_excluded(db_session):
    from datetime import datetime, timedelta, timezone
    repo = SessionRepository(db_session)
    session_obj = repo.create({
        "UserID": 1,
        "TokenHash": "revokedhash",
        "ExpiresAt": datetime.now(timezone.utc) + timedelta(hours=1),
    })
    repo.revoke(session_obj.SessionID)
    found = repo.find_by_hash("revokedhash")
    assert found is None


def test_fir_count(db_session):
    repo = FirRepository(db_session)
    for i in range(3):
        repo.create({"CrimeNo": f"CNT-{i:03d}", "CaseStatusID": 1})
    assert repo.count(case_status_id=1) == 3


def test_fir_eager_loading(db_session):
    from src.relationships import InvOccuranceTime
    repo = FirRepository(db_session)
    case = repo.create({"CrimeNo": "EAGER-TEST"})
    db_session.add(InvOccuranceTime(CaseMasterID=case.CaseMasterID, BriefFacts="Eager test"))
    db_session.flush()
    found = repo.get_by_id(case.CaseMasterID)
    assert found is not None
    assert found.occurrence_time is not None
    assert found.occurrence_time.BriefFacts == "Eager test"
