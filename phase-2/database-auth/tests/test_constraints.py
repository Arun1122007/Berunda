import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session as SASession
from sqlalchemy.exc import IntegrityError

from src.models import Base, CaseMaster, User, District, Unit


@pytest.fixture
def engine():
    e = create_engine("sqlite:///:memory:", echo=False)
    Base.metadata.create_all(e)
    _seed_lookup(e)
    return e


def _seed_lookup(engine):
    conn = engine.connect()
    conn.execute(text("INSERT INTO src_District (DistrictID, DistrictName) VALUES (1, 'Test Dist')"))
    conn.execute(text("INSERT INTO src_Unit (UnitID, UnitName, DistrictID) VALUES (1, 'Test PS', 1)"))
    conn.execute(text("INSERT INTO auth_User (UserID, Email, HashedPassword, Role, IsActive) VALUES (1, 'u@t.com', 'hash', 'admin', 1)"))
    conn.commit()
    conn.close()


@pytest.fixture
def session(engine):
    s = SASession(bind=engine)
    yield s
    s.close()


def test_unique_constraint_crime_no(session):
    session.add(CaseMaster(CrimeNo="UNQ-CONSTRAINT"))
    session.flush()
    with pytest.raises(IntegrityError):
        session.add(CaseMaster(CrimeNo="UNQ-CONSTRAINT"))
        session.flush()
    session.rollback()


def test_unique_constraint_email(session):
    session.add(User(Email="dup-email@test.com", HashedPassword="h", Role="officer", IsActive=True))
    session.flush()
    with pytest.raises(IntegrityError):
        session.add(User(Email="dup-email@test.com", HashedPassword="h2", Role="admin", IsActive=True))
        session.flush()
    session.rollback()


def test_not_null_crime_no(session):
    with pytest.raises(IntegrityError):
        case = CaseMaster()
        session.add(case)
        session.flush()
    session.rollback()


def test_not_null_email(session):
    with pytest.raises(IntegrityError):
        user = User(HashedPassword="h", Role="admin", IsActive=True)
        session.add(user)
        session.flush()
    session.rollback()


def test_not_null_hashed_password(session):
    with pytest.raises(IntegrityError):
        user = User(Email="nopass@t.com", Role="admin", IsActive=True)
        session.add(user)
        session.flush()
    session.rollback()


def test_not_null_role(session):
    with pytest.raises(IntegrityError):
        user = User(Email="norole@t.com", HashedPassword="h", IsActive=True)
        session.add(user)
        session.flush()
    session.rollback()


def test_not_null_is_active_default(session):
    user = User(Email="default-active@t.com", HashedPassword="h", Role="viewer")
    session.add(user)
    session.flush()
    assert user.IsActive is True


def test_foreign_key_case_violation(session):
    with pytest.raises(IntegrityError):
        session.add(CaseMaster(CrimeNo="FK-TEST", PoliceStationID=99999))
        session.flush()
    session.rollback()


def test_foreign_key_user_district_nullable(session):
    user = User(Email="null-district@t.com", HashedPassword="h", Role="analyst", IsActive=True)
    session.add(user)
    session.flush()
    assert user.DistrictID is None


def test_crime_no_max_length(session):
    long_crime = "A" * 300
    with pytest.raises((IntegrityError, Exception)):
        session.add(CaseMaster(CrimeNo=long_crime))
        session.flush()
    session.rollback()
