import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session as SASession

from src.models import Base, CaseMaster, User, District, Unit
from src.seed.test_fixtures import sample_fir_data, sample_user_data
from src.auth.password import hash_password


@pytest.fixture
def db_session():
    engine = create_engine("sqlite:///:memory:", echo=False)
    Base.metadata.create_all(engine)
    session = SASession(bind=engine)
    session.add_all([
        District(DistrictID=1, DistrictName="Test District 1", StateID=1),
        District(DistrictID=2, DistrictName="Test District 2", StateID=1),
    ])
    session.add_all([
        Unit(UnitID=1, UnitName="Test PS 1", DistrictID=1, TypeID=1),
        Unit(UnitID=2, UnitName="Test PS 2", DistrictID=2, TypeID=1),
    ])
    session.flush()
    yield session
    session.close()
    engine.dispose()


def test_sample_fir_data_has_expected_structure():
    assert len(sample_fir_data) == 2
    for fir in sample_fir_data:
        assert "CrimeNo" in fir
        assert "Complainant" in fir
        assert "Victim" in fir
        assert "Accused" in fir


def test_sample_fir_data_crime_numbers_unique():
    crimes = [f["CrimeNo"] for f in sample_fir_data]
    assert len(crimes) == len(set(crimes))


def test_sample_fir_data_has_required_fields():
    required = ["CrimeNo", "CaseNo", "PoliceStationID", "CaseCategoryID",
                 "GravityOffenceID", "CrimeMajorHeadID", "CaseStatusID",
                 "BriefFacts", "Latitude", "Longitude",
                 "Complainant", "Victim", "Accused"]
    for item in sample_fir_data:
        for field in required:
            assert field in item, f"Missing {field} in {item['CrimeNo']}"


def test_sample_fir_data_complainant_details():
    for item in sample_fir_data:
        c = item["Complainant"]
        assert "Name" in c
        assert "Age" in c
        assert "OccupationID" in c


def test_sample_fir_data_victim_details():
    for item in sample_fir_data:
        v = item["Victim"]
        assert "Name" in v
        assert "Age" in v
        assert "GenderID" in v


def test_sample_fir_data_accused_details():
    for item in sample_fir_data:
        a = item["Accused"]
        assert "Name" in a
        assert "Age" in a
        assert "PersonID" in a


def test_sample_fir_data_geocoded():
    for item in sample_fir_data:
        assert isinstance(item["Latitude"], float)
        assert isinstance(item["Longitude"], float)
        assert -90 <= item["Latitude"] <= 90
        assert -180 <= item["Longitude"] <= 180


def test_sample_user_data_has_expected_count():
    assert len(sample_user_data) == 3


def test_sample_user_data_roles():
    roles = {u["Role"] for u in sample_user_data}
    assert "admin" in roles
    assert "officer" in roles
    assert "viewer" in roles


def test_sample_user_data_emails_unique():
    emails = [u["Email"] for u in sample_user_data]
    assert len(emails) == len(set(emails))


def test_sample_user_data_required_fields():
    required = ["Email", "Password", "Role", "DistrictID", "IsActive"]
    for item in sample_user_data:
        for field in required:
            assert field in item, f"Missing {field} in {item.get('Email', 'unknown')}"


def test_sample_fir_data_can_create_case(db_session):
    from src.repositories import FirRepository
    repo = FirRepository(db_session)
    item = sample_fir_data[0]
    case = repo.create({
        "CrimeNo": item["CrimeNo"],
        "CaseNo": item["CaseNo"],
        "PoliceStationID": item["PoliceStationID"],
        "CaseCategoryID": item["CaseCategoryID"],
        "GravityOffenceID": item["GravityOffenceID"],
        "CrimeMajorHeadID": item["CrimeMajorHeadID"],
        "CrimeMinorHeadID": item["CrimeMinorHeadID"],
        "CaseStatusID": item["CaseStatusID"],
    })
    assert case.CrimeNo == "TEST-FIR-001"


def test_sample_user_data_can_create_user(db_session):
    from src.repositories import UserRepository
    repo = UserRepository(db_session)
    item = sample_user_data[0]
    user = repo.create({
        "Email": item["Email"],
        "HashedPassword": hash_password(item["Password"]),
        "Role": item["Role"],
        "DistrictID": item["DistrictID"],
        "IsActive": item["IsActive"],
    })
    assert user.Email == "test-admin@berunda.gov"
    assert user.Role == "admin"


def test_sample_user_data_password_verifiable(db_session):
    from src.auth.password import verify_password
    for item in sample_user_data:
        hashed = hash_password(item["Password"])
        assert verify_password(item["Password"], hashed) is True
